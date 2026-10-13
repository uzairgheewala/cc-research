"""Run PC from upstream causal-learn (PyPI) through the same runner as every other baseline, on released and shuffled
columns, so the scoreboard's PC row can be compared without Causal-Copilot's modified copy (AUD-27 found that copy
returns the wrong skeleton even with a perfect independence oracle).

  python analysis/pc_upstream_run.py --causal-learn PATH_TO_UPSTREAM_COPY [--families semantic formula]

PATH must contain the `causallearn` package (for example an unpacked causal_learn-0.1.4.8 wheel). The runner
(analysis/causalarena_methods.py, unchanged) reads causal-learn from $CC_REPO/externals/causal-learn, so this script
builds a temporary folder with that layout pointing at PATH, runs the released and shuffled arms (shuffle seed 20261010,
the BND-06 seed), and records the true engine in each output header. No model calls.
Outputs: analysis/results/methods/pc_upstream_<family>_obs_{rel,shuf}.json
Tickets: AUD-28, BEN-07, REP-07
"""
import argparse, json, os, subprocess, sys, tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--causal-learn", required=True)
    ap.add_argument("--families", nargs="+", default=["semantic", "formula"])
    ap.add_argument("--label", default="upstream causal-learn (PyPI)")
    a = ap.parse_args()
    src = Path(a.causal_learn).resolve()
    import importlib.util
    spec = importlib.util.spec_from_file_location("cl_init", src / "causallearn" / "__init__.py")
    assert spec is not None, "no causallearn package under %s" % src
    version = next((p.name.split("-")[1].replace(".dist-info", "") for p in src.glob("causal_learn-*.dist-info")), "unknown")
    tmp = Path(tempfile.mkdtemp())
    (tmp / "externals").mkdir()
    os.symlink(src, tmp / "externals" / "causal-learn")
    env = dict(os.environ, CC_REPO=str(tmp))
    for fam in a.families:
        for arm, seed in (("rel", None), ("shuf", "20261010")):
            out = HERE / "results" / "methods" / ("pc_upstream_%s_obs_%s.json" % (fam, arm))
            cmd = [sys.executable, str(HERE / "causalarena_methods.py"), "--method", "pc", "--family", fam,
                   "--regime", "obs_only", "--out", str(out)] + (["--shuffle-seed", seed] if seed else [])
            subprocess.run(cmd, check=True, env=env)
            d = json.load(open(out))
            d["header"]["causal_learn"] = "%s %s (%s)" % (a.label, version, "loaded from $CC_REPO/externals/causal-learn")
            d["header"]["ticket"] = "AUD-28"
            json.dump(d, open(out, "w"), indent=1)
            print("wrote", out.relative_to(HERE.parent))


if __name__ == "__main__":
    main()
