"""Out-of-repo recording layer for Causal-Copilot runs.

Observation only: every hook calls the original function with the original arguments and
returns (or re-raises) exactly what the original produced. Nothing is seeded, reordered or retried.
The one deliberate interaction is answering the final interactive "any questions?" prompt with "no".
"""
import builtins
import copy
import datetime
import functools
import hashlib
import inspect
import json
import os
import pickle
import sys
import time
import traceback
from pathlib import Path

from cc_common import REPO, safe_copy, to_jsonable

_REPO_PREFIX = str(REPO) + os.sep


def _utc():
    return datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="milliseconds")


def is_state(x):
    return all(hasattr(x, a) for a in ("user_data", "statistics", "results", "algorithm"))


class Tee:
    """Mirror a text stream into a log file (secrets scrubbed in the file copy)."""

    def __init__(self, stream, fh, scrub):
        self._stream, self._fh, self._scrub = stream, fh, scrub

    def write(self, s):
        try:
            self._fh.write(self._scrub(s))
        except Exception:
            pass
        return self._stream.write(s)

    def flush(self):
        try:
            self._fh.flush()
        except Exception:
            pass
        return self._stream.flush()

    def __getattr__(self, name):
        return getattr(self._stream, name)


class Recorder:
    def __init__(self, run_dir, scrub):
        self.run_dir = Path(run_dir)
        self.scrub = scrub
        self.llm_path = self.run_dir / "llm_calls.jsonl"
        self.events_path = self.run_dir / "events.jsonl"
        self.art_dir = self.run_dir / "artifacts"
        self.state_dir = self.run_dir / "state"
        for d in (self.art_dir, self.state_dir):
            d.mkdir(parents=True, exist_ok=True)
        self.seq = 0
        self.stage_stack = []
        self.stage_times = []
        self.llm_depth = 0
        self.api_buf = []
        self.last_state = None
        self.state_index = 0
        self.snapshots = []
        self.captures = {}
        self.auto_inputs = 0

    # ---------------------------------------------------------------- basics
    @property
    def stage(self):
        return self.stage_stack[-1] if self.stage_stack else "unstaged"

    def next_seq(self):
        self.seq += 1
        return self.seq

    def _append(self, path, rec):
        line = self.scrub(json.dumps(rec, default=repr, ensure_ascii=False))
        with open(path, "a", encoding="utf-8") as fh:
            fh.write(line + "\n")

    def event(self, rec):
        rec = {"seq": rec.pop("seq", None) or self.next_seq(), "t": _utc(), "stage": self.stage, **rec}
        self._append(self.events_path, rec)

    def caller_chain(self, limit=8):
        """Repo frames (outside llm/) leading to the current call, innermost first."""
        frames, f = [], sys._getframe(2)
        while f is not None and len(frames) < limit:
            fn = os.path.realpath(f.f_code.co_filename)
            if fn.startswith(_REPO_PREFIX):
                rel = fn[len(_REPO_PREFIX):].replace(os.sep, "/")
                if not rel.startswith("llm/"):
                    frames.append("%s:%d:%s" % (rel, f.f_lineno, f.f_code.co_name))
            f = f.f_back
        return frames

    # ------------------------------------------------------------- LLM hooks
    def install_llm_hooks(self):
        rec = self
        # low level: the OpenAI SDK call (captures what was actually sent and the raw response)
        from openai.resources.chat.completions import Completions
        orig_create = Completions.create

        @functools.wraps(orig_create)
        def create(self_, *a, **k):
            t = time.time()
            entry = {"t": _utc(), "request": to_jsonable(copy.deepcopy(k)), "n_positional": len(a),
                     "base_url": str(getattr(getattr(self_, "_client", None), "base_url", "")),
                     "response": None, "error": None}
            try:
                resp = orig_create(self_, *a, **k)
                try:
                    entry["response"] = resp.model_dump()
                except Exception:
                    entry["response"] = to_jsonable(resp)
                return resp
            except BaseException as e:
                entry["error"] = {"type": type(e).__name__, "message": str(e)[:4000]}
                raise
            finally:
                entry["duration_s"] = round(time.time() - t, 3)
                if rec.llm_depth > 0:
                    rec.api_buf.append(entry)
                else:
                    rec._append(rec.llm_path, {"seq": rec.next_seq(), "level": "api_only", "t": entry["t"],
                                               "stage": rec.stage, "caller": rec.caller_chain(), "api": [entry]})

        Completions.create = create

        # high level: the repo's single LLM choke point
        import llm.llm_client as lc
        orig_cc = lc.LLMClient.chat_completion
        sig = inspect.signature(orig_cc)

        @functools.wraps(orig_cc)
        def chat_completion(client_self, *a, **k):
            seq = rec.next_seq()
            try:
                bound = sig.bind(client_self, *a, **k)
                bound.apply_defaults()
                argd = dict(bound.arguments)
                argd.pop("self", None)
            except TypeError as e:
                argd = {"_bind_error": str(e), "args": list(a), "kwargs": dict(k)}
            rf = argd.pop("response_format", None)
            rf_desc = None
            if rf is not None:
                rf_desc = {"name": getattr(rf, "__name__", repr(rf))}
                try:
                    rf_desc["json_schema"] = rf.model_json_schema()
                except Exception:
                    pass
            record = {"seq": seq, "level": "client", "t": _utc(), "stage": rec.stage,
                      "caller": rec.caller_chain(),
                      "provider": getattr(client_self, "provider", None),
                      "client_default_model": getattr(client_self, "model", None),
                      "args": to_jsonable(copy.deepcopy(argd)), "response_format": rf_desc,
                      "result": None, "result_type": None, "error": None}
            start = len(rec.api_buf)
            rec.llm_depth += 1
            t = time.time()
            try:
                result = orig_cc(client_self, *a, **k)
                record["result"] = to_jsonable(result)
                record["result_type"] = type(result).__name__
                return result
            except BaseException as e:
                record["error"] = {"type": type(e).__name__, "message": str(e)[:4000],
                                   "traceback": traceback.format_exc()[-4000:]}
                raise
            finally:
                rec.llm_depth -= 1
                record["duration_s"] = round(time.time() - t, 3)
                record["api"] = rec.api_buf[start:]
                del rec.api_buf[start:]
                try:
                    canon = json.dumps([record["api"][0]["request"]] if record["api"] else record["args"],
                                       sort_keys=True, default=repr)
                    record["request_sha256"] = hashlib.sha256(canon.encode("utf-8")).hexdigest()
                except Exception:
                    record["request_sha256"] = None
                rec._append(rec.llm_path, record)

        lc.LLMClient.chat_completion = chat_completion

    # ------------------------------------------------------- state snapshots
    def snapshot(self, label, state):
        self.last_state = state
        self.state_index += 1
        base = self.state_dir / ("%02d_%s" % (self.state_index, label))
        mode, nbytes = None, 0
        try:
            data = pickle.dumps(state, protocol=4)
            mode = "pickle"
        except Exception as e1:
            try:
                import dill
                data = dill.dumps(state)
                mode = "dill"
            except Exception as e2:
                data, mode = None, "failed: %r / %r" % (e1, e2)
        if data is not None:
            Path(str(base) + ".pkl").write_bytes(data)
            nbytes = len(data)
        try:
            text = self.scrub(json.dumps(to_jsonable(state), indent=1, default=repr, ensure_ascii=False))
            Path(str(base) + ".json").write_text(text, encoding="utf-8")
        except Exception as e:
            Path(str(base) + ".json").write_text(json.dumps({"summary_error": repr(e)}), encoding="utf-8")
        self.snapshots.append({"index": self.state_index, "label": label, "pickle_mode": mode, "bytes": nbytes})
        self.event({"type": "state_snapshot", "label": label, "pickle_mode": mode, "bytes": nbytes})

    def wrap_stage(self, owner, attr, label, snapshot=True):
        """Label everything that happens inside owner.attr as `label`; snapshot the state afterwards."""
        rec = self
        orig = getattr(owner, attr)

        @functools.wraps(orig)
        def wrapped(*a, **k):
            rec.stage_stack.append(label)
            t = time.time()
            ok, ret = False, None
            try:
                ret = orig(*a, **k)
                ok = True
                return ret
            finally:
                rec.stage_stack.pop()
                rec.stage_times.append({"stage": label, "duration_s": round(time.time() - t, 3), "ok": ok})
                if snapshot:
                    state = ret if is_state(ret) else None
                    if state is None:
                        for x in list(a) + list(k.values()):
                            if is_state(x):
                                state = x
                                break
                            gs = getattr(x, "global_state", None)
                            if gs is not None and is_state(gs):
                                state = gs
                                break
                    if state is not None:
                        try:
                            rec.snapshot(label if ok else label + "__FAILED", state)
                        except Exception as e:
                            rec.event({"type": "snapshot_error", "label": label, "error": repr(e)})

        setattr(owner, attr, wrapped)

    # ------------------------------------------------------ function capture
    def wrap_capture(self, owner, attr, label=None, drop_first=False):
        """Record arguments (before and after the call) and the return value of owner.attr."""
        rec = self
        orig = getattr(owner, attr)
        label = label or attr

        @functools.wraps(orig)
        def wrapped(*a, **k):
            seq = rec.next_seq()
            shown = a[1:] if drop_first else a
            before = safe_copy({"args": list(shown), "kwargs": dict(k)})
            t = time.time()
            err, ret, ok = None, None, False
            try:
                ret = orig(*a, **k)
                ok = True
                return ret
            except BaseException as e:
                err = {"type": type(e).__name__, "message": str(e)[:4000]}
                raise
            finally:
                dur = round(time.time() - t, 3)
                name = "%05d_%s.pkl" % (seq, label)
                try:
                    art = {"name": label, "seq": seq, "stage": rec.stage, "duration_s": dur,
                           "args_before": before,
                           "args_after": safe_copy({"args": list(shown), "kwargs": dict(k)}),
                           "ret": safe_copy(ret) if ok else None, "error": err}
                    with open(rec.art_dir / name, "wb") as fh:
                        pickle.dump(art, fh, protocol=4)
                except Exception as e:
                    name = "unwritable: %r" % (e,)
                rec.captures[label] = rec.captures.get(label, 0) + 1
                rec.event({"seq": seq, "type": "capture", "name": label, "duration_s": dur,
                           "ok": ok, "error": err, "artifact": name})

        setattr(owner, attr, wrapped)

    # ----------------------------------------------------------------- misc
    def record_rng_states(self):
        """Observe (never set) the global RNG states at run start, so a run can be replayed later."""
        import random
        states = {"python_random": random.getstate()}
        try:
            import numpy as np
            states["numpy_global"] = np.random.get_state()
        except Exception as e:
            states["numpy_global_error"] = repr(e)
        try:
            import torch
            states["torch"] = torch.random.get_rng_state().tolist()
        except Exception as e:
            states["torch_error"] = repr(e)
        with open(self.run_dir / "rng_initial_states.pkl", "wb") as fh:
            pickle.dump(states, fh, protocol=4)

    def auto_answer_input(self, answer="no"):
        rec = self

        def _input(prompt=""):
            rec.auto_inputs += 1
            rec.event({"type": "auto_input", "prompt": str(prompt)[:500], "answer": answer})
            print("%s%s   [harness auto-answer]" % (prompt, answer))
            return answer

        builtins.input = _input
