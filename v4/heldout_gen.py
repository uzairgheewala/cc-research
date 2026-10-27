"""The fresh held-out family for kernel v4 (BLD-18, wave B): replicate 1 of every family-2 configuration.

Tickets: BLD-18, TGT-18

    python -m v4.heldout_gen [--out external/b2_heldout_v4] [--rep 1]

Every v3 held-out read is spent (CausalArena test twice, family 2 replicate 0 once), so a v4 read needs data no kernel has
scored. This writes replicate `rep` (default 1) of each (source scenario, track, rho) with analysis/b2_generator.py's own
make_file, unchanged: same graphs G_D and mechanisms recipe, new noise and mechanism draws (the replicate index is in
every seed). The 50 source scenarios are the same as replicate 0's, so a v4 read on these files is a claim about new draws
of known systems, not about new systems.

Sealed until the v4 freeze: nothing may score these files before plans/v4_freeze.json exists (plans/v4_prereg.json,
'held_out'). The script writes MANIFEST.json (sha256 of every file) and analysis/results/v4/heldout_seal.json (the
manifest's sha256), and refuses to overwrite an existing manifest.
"""
import argparse, hashlib, json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "analysis"))


def main(argv=None):
    import b2_generator as G
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=str(ROOT / "external" / "causalarena"))
    ap.add_argument("--out", default=str(ROOT / "external" / "b2_heldout_v4"))
    ap.add_argument("--rep", type=int, default=1)
    ap.add_argument("--seed", type=int, default=20261012)
    ap.add_argument("--slugs", nargs="*", default=None)
    ap.add_argument("--seal", default=str(ROOT / "analysis" / "results" / "v4" / "heldout_seal.json"))
    a = ap.parse_args(argv)
    if a.rep < 1:
        raise SystemExit("replicate 0 is family 2's read set; the v4 held-out family starts at replicate 1")
    out = Path(a.out)
    if (out / "MANIFEST.json").exists():
        raise SystemExit("%s already holds a manifest: the held-out family is written once" % out)
    CA, SA = G._ensure_imports(a.root)
    gen_sha = G.script_sha256()
    splits = str(Path(a.root).resolve().parents[1] / "plans" / "splits.json")
    files = {}
    for slug, split, src in G.sources(a.root, splits):
        if a.slugs and slug not in a.slugs:
            continue
        for track in G.TRACKS:
            for rho in G.RHOS:
                sub = out / track / G.rho_tag(rho)
                sub.mkdir(parents=True, exist_ok=True)
                arrays, meta = G.make_file(SA, src, slug, split, rho, track, a.rep, a.seed, gen_sha)
                name = "b2_%s_%s_%s__rep%03d.npz" % (track, G.rho_tag(rho), slug, a.rep)
                files["%s/%s/%s" % (track, G.rho_tag(rho), name)] = G.write_npz(sub / name, arrays)
        print("done", slug, flush=True)
    man = {"benchmark": "b2_heldout_v4", "tickets": ["BLD-18", "TGT-18"], "generator": "analysis/b2_generator.py (make_file, unchanged)",
           "generator_sha256": gen_sha, "wrapper": "v4/heldout_gen.py", "replicate": a.rep, "seed": a.seed,
           "sealed_until": "plans/v4_freeze.json exists (plans/v4_prereg.json held_out)", "files": dict(sorted(files.items()))}
    G.write_json(man, out / "MANIFEST.json")
    msha = hashlib.sha256((out / "MANIFEST.json").read_bytes()).hexdigest()
    seal = Path(a.seal)
    seal.parent.mkdir(parents=True, exist_ok=True)
    seal.write_text(json.dumps({"tickets": ["BLD-18"], "folder": str(out.relative_to(ROOT)) if out.is_relative_to(ROOT) else str(out),
                                "files": len(files), "manifest_sha256": msha, "replicate": a.rep,
                                "scored_by_any_kernel": False}, indent=1))
    print(json.dumps({"files": len(files), "manifest_sha256": msha}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
