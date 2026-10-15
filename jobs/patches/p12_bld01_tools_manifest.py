"""2026-10-14: BLD-01's tools manifest re-issued after harness/cc_common.py gained the EIO write retry (INF-08). Same file
list as the 2026-10-12 manifest, fresh hashes. Refuses to run twice."""
from pathlib import Path

p = Path(__file__).resolve().parents[2] / "tracker" / "catalogue.py"
c = p.read_text(encoding="utf-8")
assert "# ---- overrides p11" in c, "apply p11 first"
assert "# ---- overrides p12" not in c, "already applied"
block = r'''
# ---- overrides p12 (2026-10-14): BLD-01 tools manifest re-issued (cc_common EIO retry, INF-08)
for _i in ITEMS:
    if _i["id"] == "BLD-01":
        _i["evidence"] = ["manifests/evidence/BLD-01_tools_2026-10-14.sha256" if e == "manifests/evidence/BLD-01_tools_2026-10-12.sha256" else e
                          for e in _i["evidence"]]
        _i["checks"] = [dict(ck, path="manifests/evidence/BLD-01_tools_2026-10-14.sha256")
                        if ck.get("t") == "manifest" and ck.get("path") == "manifests/evidence/BLD-01_tools_2026-10-12.sha256" else ck
                        for ck in _i["checks"]]
        _i["note"] = ((_i.get("note") or "") + " Tools manifest re-issued 2026-10-14 (harness/cc_common.py: EIO write retry, INF-08); "
                      "the 2026-10-12 manifest stays as the record of the earlier state.").strip()
'''
p.write_text(c.rstrip("\n") + "\n" + block, encoding="utf-8")
print("p12 applied")
