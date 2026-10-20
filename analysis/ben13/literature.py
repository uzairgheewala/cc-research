"""BEN-13: the literature pair sets causalbench scores against (and which serve as names-only predicted networks).

Tickets: BEN-13

Same construction as causalbench 1.1.2 `CreateEvaluationDatasets` (STRING v11.5 links and physical links, CORUM
complexes, ChIP-seq pairs shipped in the package), with one change: the gene-name -> Ensembl map comes from the
preprocessing sidecars (name/id pairs of both lines, kept to ids perturbed in either line) instead of
`GeneNameMapLoader`, which reads both full files into memory. Where a name maps to more than one id the original's
choice depends on Python's string-hash order; here the last id in sorted order wins (deterministic). Ligand-receptor
pairs are left out (no published row uses them). A missing source file is reported, not fatal.
"""
import gzip, io, json, zipfile
from pathlib import Path


def name_map(sidecars):
    pairs, ids = set(), set()
    for s in sidecars:
        d = json.loads(Path(s).read_text())
        pairs |= {tuple(p) for p in d["name_to_id_pairs"]}
        ids |= set(d["intervened_ids_all"])
    m = dict(sorted(pairs))
    return {k: v for k, v in m.items() if v in ids}


def string_sets(links_gz, physical_gz, info_gz, nmap):
    import pandas as pd
    info = pd.read_csv(info_gz, sep="\t", compression="gzip")
    p2n = dict(zip(info["#string_protein_id"], info["preferred_name"]))
    out = []
    for f in (links_gz, physical_gz):
        s = set()
        with gzip.open(f, "rt") as fh:
            next(fh)
            for line in fh:
                p1, p2 = line.split(" ", 2)[:2]
                n1, n2 = p2n[p1], p2n[p2]
                if n1 in nmap and n2 in nmap:
                    s.add((nmap[n1], nmap[n2]))
                    s.add((nmap[n2], nmap[n1]))
        out.append(s)
    return out


def corum_set(path, nmap):
    import pandas as pd
    with zipfile.ZipFile(path) as z:
        name = [n for n in z.namelist() if n.endswith(".txt")][0]
        df = pd.read_csv(io.BytesIO(z.read(name)), sep="\t")
    col = "subunits(Gene name)" if "subunits(Gene name)" in df.columns else "subunits_gene_name"
    s = set()
    for row in df[col].astype(str):
        members = [nmap[g] for g in row.split(";") if g in nmap]
        for i in range(len(members)):
            for other in members[:i] + members[i + 1:]:
                s.add((members[i], other))
    return s


def chipseq_set(line, nmap):
    import pandas as pd
    import causalscbench.data_access as da
    f = Path(da.__file__).parent / "data" / ("K562_ChipSeq.csv" if line == "k562" else "Hep_G2_ChipSeq.csv")
    df = pd.read_csv(f)
    s = set()
    for a, b in df[["source", "target"]].values:
        if isinstance(a, str) and isinstance(b, str) and a in nmap and b in nmap:
            s.add((nmap[a], nmap[b]))
    return s


def load_all(data_dir, line, sidecars):
    """-> ({name: set of pairs}, {name: reason it is missing})."""
    data_dir = Path(data_dir)
    nmap = name_map(sidecars)
    sets, missing = {}, {}
    try:
        sets["string_network"], sets["string_physical"] = string_sets(
            data_dir / "protein.links.txt.gz", data_dir / "protein.physical.links.txt.gz", data_dir / "protein.info.txt.gz", nmap)
    except Exception as e:
        missing["string"] = "%s: %s" % (type(e).__name__, str(e)[:160])
    try:
        sets["corum"] = corum_set(data_dir / "corum_complexes.txt.zip", nmap)
    except Exception as e:
        missing["corum"] = "%s: %s" % (type(e).__name__, str(e)[:160])
    try:
        sets["chipseq"] = chipseq_set(line, nmap)
    except Exception as e:
        missing["chipseq"] = "%s: %s" % (type(e).__name__, str(e)[:160])
    return sets, missing


def restrict(pairs, genes):
    """The predicted-network form causalbench's literature 'models' return: pairs among the dataset's genes, no self pairs."""
    g = set(genes)
    return sorted((a, b) for a, b in pairs if a in g and b in g and a != b)
