"""Engine wrappers with typed results and typed failures (D0.1).

Every engine is called as run_<engine>(X, ...) on columns in the order given and returns an EngineResult:
  ok        True, or False with failure = {"type": "singular" | "timeout" | "error", "message": ...}
  marks     causal-learn endpoint matrix over the given column order (M[i, j] = mark at i on the i-j edge:
            -1 tail, 1 arrowhead; i -> j is M[i, j] = -1, M[j, i] = 1)
  stages    engine-specific intermediate graphs (PC: skeleton and after-maxP marks)
  tests     PC only: every CI test the engine ran, in call order, as (phase, i, j, S, p) with i < j and S sorted
  score     GES/GIES: the final penalised log-likelihood reported by the package
  seconds   wall time
No engine reads the column order for anything but its own bookkeeping; order invariance is enforced one level up by
canonical_order() (kernel) and tested in B0.1.

Timeouts use SIGALRM (main thread only); a worker process sets thread counts to 1 before importing NumPy
(engines.runner).
"""
import contextlib, hashlib, io, os, signal, sys, time
from dataclasses import dataclass, field

if os.environ.get("CC_CAUSAL_LEARN") and os.environ["CC_CAUSAL_LEARN"] not in sys.path:
    sys.path.insert(0, os.environ["CC_CAUSAL_LEARN"])          # the pinned causal-learn tree (engines/MANIFEST.json)

import numpy as np


@dataclass
class EngineResult:
    engine: str
    ok: bool
    marks: object = None
    stages: dict = field(default_factory=dict)
    tests: list = field(default_factory=list)
    score: float = None
    seconds: float = 0.0
    failure: dict = None


class _Timeout(Exception):
    pass


@contextlib.contextmanager
def _alarm(seconds):
    if not seconds:
        yield
        return

    def h(signum, frame):
        raise _Timeout("exceeded %ss" % seconds)
    old = signal.signal(signal.SIGALRM, h)
    signal.alarm(int(seconds))
    try:
        yield
    finally:
        signal.alarm(0)
        signal.signal(signal.SIGALRM, old)


def _classify(e):
    msg = "%s: %s" % (type(e).__name__, str(e)[:300])
    if isinstance(e, _Timeout):
        return {"type": "timeout", "message": msg}
    if "singular" in str(e).lower() or isinstance(e, np.linalg.LinAlgError):
        return {"type": "singular", "message": msg}
    return {"type": "error", "message": msg}


def column_ids(X):
    """sha256 of each column's float64 little-endian bytes: the identity used for canonical ordering."""
    X = np.ascontiguousarray(np.asarray(X, dtype="<f8"))
    return [hashlib.sha256(np.ascontiguousarray(X[:, j]).tobytes()).hexdigest() for j in range(X.shape[1])]


def canonical_order(X=None, ids=None, tiebreak=None):
    """Permutation `order` such that X[:, order] is in canonical order: sorted by column id (sha256 of the values); columns
    with identical values (same id) are ordered by `tiebreak` (the kernel passes var_id = sha256(values + name)), never by
    position, so the column order a caller passes cannot reach the engines or the name-to-index assignment."""
    ids = ids if ids is not None else column_ids(X)
    tb = tiebreak if tiebreak is not None else [""] * len(ids)
    if tiebreak is None and len(set(ids)) < len(ids):
        raise ValueError("identical columns need a tie-break (variable names); pass tiebreak=")
    return sorted(range(len(ids)), key=lambda j: (ids[j], tb[j]))


# ---------------------------------------------------------------- PC with maxP, recording every CI test
def run_pc_maxp(X=None, alpha=0.05, ci=None, p=None, timeout_s=0):
    """causal-learn PC (stable, Fisher-z) + maxP (priority 3) + Meek, through causal-learn's own components.
    ci: optional callable (i, j, S) -> p-value replacing Fisher-z (the d-separation oracle in B0.1); then p = #variables."""
    t0 = time.time()
    try:
        from causallearn.utils.cit import CIT
        from causallearn.utils.PCUtils import Meek, SkeletonDiscovery, UCSepset
    except ImportError as e:
        return EngineResult("pc_maxp", False, failure={"type": "environment", "message": str(e)})
    log = []
    phase = ["skeleton"]
    try:
        with _alarm(timeout_s), contextlib.redirect_stdout(io.StringIO()):
            data = np.asarray(X, dtype=float) if X is not None else np.zeros((20, p))
            base = CIT(data, "fisherz") if ci is None else None

            class Recorder:
                method = "fisherz"

                def __deepcopy__(self, memo):          # UCSepset.maxp and Meek.meek deep-copy the graph; keep one log
                    return self

                def __call__(self, i, j, S=None):
                    S = tuple(sorted(int(s) for s in (S or ())))
                    pv = base(i, j, S) if base is not None else ci(int(i), int(j), S)
                    a, b = (int(i), int(j)) if i < j else (int(j), int(i))
                    log.append((phase[0], a, b, S, float(pv)))
                    return pv
            cg1 = SkeletonDiscovery.skeleton_discovery(data, alpha, Recorder(), stable=True, show_progress=False)
            skel = cg1.G.graph.copy()
            phase[0] = "maxp"
            cg2 = UCSepset.maxp(cg1, 3)
            after_maxp = cg2.G.graph.copy()
            phase[0] = "meek"
            cg = Meek.meek(cg2)
            M = cg.G.graph.copy()
    except Exception as e:  # noqa: BLE001 - typed failure
        return EngineResult("pc_maxp", False, tests=log, seconds=time.time() - t0, failure=_classify(e))
    return EngineResult("pc_maxp", True, marks=M, stages={"skeleton": skel, "after_maxp": after_maxp}, tests=log,
                        seconds=time.time() - t0)


def run_pc_reference(X, alpha=0.05, timeout_s=0):
    """The plain library call, for the equality check in B1 rung R1 (no recording)."""
    t0 = time.time()
    try:
        from causallearn.search.ConstraintBased.PC import pc
        with _alarm(timeout_s), contextlib.redirect_stdout(io.StringIO()):
            M = pc(np.asarray(X, dtype=float), alpha, "fisherz", stable=True, uc_rule=1, uc_priority=3, show_progress=False).G.graph
    except Exception as e:  # noqa: BLE001
        return EngineResult("pc_maxp_reference", False, seconds=time.time() - t0, failure=_classify(e))
    return EngineResult("pc_maxp_reference", True, marks=M.copy(), seconds=time.time() - t0)


# ---------------------------------------------------------------- GES (BIC) and GIES
def cpdag_to_marks(C):
    C = (np.asarray(C) != 0).astype(int)
    d = C.shape[0]
    M = np.zeros((d, d), dtype=int)
    for i in range(d):
        for j in range(d):
            if C[i, j] and not C[j, i]:
                M[i, j], M[j, i] = -1, 1
            elif C[i, j] and C[j, i]:
                M[i, j] = M[j, i] = -1
    return M


def run_ges_bic(X, timeout_s=0):
    t0 = time.time()
    try:
        import ges as ges_pkg
    except ImportError as e:
        return EngineResult("ges_bic", False, failure={"type": "environment", "message": str(e)})
    try:
        with _alarm(timeout_s), contextlib.redirect_stdout(io.StringIO()):
            X = np.asarray(X, dtype=float)
            Z = (X - X.mean(0)) / X.std(0)
            C, score = ges_pkg.fit_bic(Z)
    except Exception as e:  # noqa: BLE001
        return EngineResult("ges_bic", False, seconds=time.time() - t0, failure=_classify(e))
    return EngineResult("ges_bic", True, marks=cpdag_to_marks(C), score=float(score), seconds=time.time() - t0)


def environments(intervened):
    """Rows split by intervened-cell pattern: [(target columns, row indices)], observational rows first."""
    pats = {}
    for r in range(intervened.shape[0]):
        pats.setdefault(tuple(int(k) for k in np.where(intervened[r])[0]), []).append(r)
    keys = sorted(pats, key=lambda k: (len(k) > 0, k))
    return [(list(k), pats[k]) for k in keys]


def run_gies(X, intervened, timeout_s=0):
    t0 = time.time()
    try:
        import gies
    except ImportError as e:
        return EngineResult("gies", False, failure={"type": "environment", "message": str(e)})
    try:
        with _alarm(timeout_s), contextlib.redirect_stdout(io.StringIO()):
            envs = environments(np.asarray(intervened))
            data = [np.asarray(X, dtype=float)[rows] for _, rows in envs]
            targets = [tg for tg, _ in envs]
            C, score = gies.fit_bic(data, targets)
    except Exception as e:  # noqa: BLE001
        return EngineResult("gies", False, seconds=time.time() - t0, failure=_classify(e))
    return EngineResult("gies", True, marks=cpdag_to_marks(C), score=float(score), seconds=time.time() - t0)


# ---------------------------------------------------------------- marks <-> sets
def marks_to_sets(M):
    """(directed {(i, j)}, undecided {(i, j), i < j}) from causal-learn marks; any non-(tail, arrow) pair is undecided."""
    M = np.asarray(M)
    d = M.shape[0]
    D, U = set(), set()
    for i in range(d):
        for j in range(i + 1, d):
            a, b = int(M[i, j]), int(M[j, i])
            if a == 0 and b == 0:
                continue
            if a == -1 and b == 1:
                D.add((i, j))
            elif a == 1 and b == -1:
                D.add((j, i))
            else:
                U.add((i, j))
    return D, U


def map_back(D, U, order):
    """Sets over permuted columns (column k is original variable order[k]) -> sets over original indices."""
    D2 = {(order[i], order[j]) for i, j in D}
    U2 = {tuple(sorted((order[i], order[j]))) for i, j in U}
    return D2, U2
