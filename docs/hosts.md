# Hosts that run the wave sheets

Tickets: INF-11, INF-10, CAP-11

Why this file exists: the number of wave jobs that can run at once is set by Docker's memory and the core count, and the
last digits of some engine numbers depend on the CPU family (AVX-512 or not), which decides the BLAS kernel. The wave
runner's preflight records both on every sheet; this file keeps the per-machine facts in one place for sizing.

| | Laptop 1 (until 30 Oct 2026) | Laptop 2 (from 30 Oct 2026) |
|---|---|---|
| CPU | not recorded by model; 16 logical cores (sheet A preflight, 20 Oct) | Intel Core Ultra 7 155U (Meteor Lake, a 15 W U-series part) |
| Cores | 16 logical | 12 cores (2 performance, 8 efficient, 2 low-power efficient), 14 threads: Intel's spec; `manifests/hosts/laptop2.json` confirms |
| AVX-512 | no | no (checked: `/proc/cpuinfo` flags on this machine, 30 Oct) |
| AVX2 | yes | yes |
| BLAS kernel the runner uses | HASWELL (`OPENBLAS_CORETYPE` override, wave A preflight) | HASWELL, by the same rule |
| RAM | not recorded | `manifests/hosts/laptop2.json` (`tools/host_probe.ps1`) |
| Docker memory | 6.2 GB, job budget 4.3 GB (0.7 x) | `manifests/hosts/laptop2.json`; the runner budgets 0.7 x |
| Causal-Copilot base image | 33d383... (BND-08), then 92c6b2... (21 Oct; BLD-06 live) | 4f9ba5... (31 Oct 01:26 UTC) |

The cloud sandbox where the engine cache was built ran both SKYLAKEX (AVX-512) and HASWELL.

## What the move changes in numerical results

1. **CPU family: nothing.** Both laptops lack AVX-512, so both run OpenBLAS's HASWELL kernels and NumPy's AVX2 code paths.
   Laptop 2 should reproduce laptop 1's numbers to the bit. Against the sandbox's SKYLAKEX runs the last digits of test
   statistics still differ, as before (CAP-11: full ledger hashes are per CPU family; claim structure, `claims_sha256`,
   is not). The canary checks this on the first sheet; nothing needs re-running for the papers.
2. **Hybrid cores: nothing.** Performance and efficient cores have the same instruction set, so the core a job lands on does
   not change its arithmetic. Every engine script pins one BLAS thread, so the core count does not change the order of
   sums either.
3. **The rebuilt Causal-Copilot base image: possibly.** `Dockerfile.cpu` downloads unpinned packages, so each rebuild is a
   new environment (third base so far). Recorded live runs are unaffected, but any new live comparison needs its own main
   control on this image, as LIVE_06M did on 21-22 Oct. The kernel, bench and X5 images pin their packages
   (`docker/requirements_*.txt`), so rebuilding them should give the same environment; `jobs/waves/images/*.id` hold
   laptop 1's image ids until the builds rewrite them.

## Sizing (to fill from `manifests/hosts/laptop2.json`)

- Parallel engine jobs = min(cores the runner may use, 0.7 x Docker memory / memory per job). The 155U sustains less work per
  core than laptop 1 (a 15 W part, and 10 of its 12 cores are efficient cores), so expect longer wall time for the same
  core-hours (for example the family-2 fill, about 5.5 core-hours on sheet A).
- Docker memory is set in `%UserProfile%\.wslconfig` (`[wsl2]` then `memory=...`), then `wsl --shutdown`.
