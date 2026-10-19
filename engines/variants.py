"""Engine variants for kernel v3 experiments (K1). engines/core.py is not changed: v2's engines stay byte-identical.

  run_ges_pen(X, lam_scale)   GES with the Gaussian L0 penalty lambda = lam_scale * log(n) / 2 on column z-scores
                              (lam_scale = 1 is exactly ges.fit_bic, the v2 engine). A smaller penalty keeps weaker edges:
                              the lever for links the default BIC drops at n = 1,000 (K1, docs/design/q2_kernel_v3_design.md).
"""
import contextlib, io, time

import numpy as np

from engines.core import EngineResult, _alarm, _classify, cpdag_to_marks


def run_ges_pen(X, lam_scale=1.0, timeout_s=0):
    t0 = time.time()
    try:
        import ges as ges_pkg
        from ges.scores.gauss_obs_l0_pen import GaussObsL0Pen
    except ImportError as e:
        return EngineResult("ges_pen", False, failure={"type": "environment", "message": str(e)})
    try:
        with _alarm(timeout_s), contextlib.redirect_stdout(io.StringIO()):
            X = np.asarray(X, dtype=float)
            Z = (X - X.mean(0)) / X.std(0)
            lam = lam_scale * 0.5 * np.log(Z.shape[0])
            C, score = ges_pkg.fit(GaussObsL0Pen(Z, lmbda=lam))
    except Exception as e:  # noqa: BLE001
        return EngineResult("ges_pen", False, seconds=time.time() - t0, failure=_classify(e))
    return EngineResult("ges_pen", True, marks=cpdag_to_marks(C), score=float(score), seconds=time.time() - t0)
