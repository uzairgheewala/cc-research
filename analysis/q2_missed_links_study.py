"""Dev-only study of the true links the v2 skeleton missed: for each, a held-out R2 gain from adding the missed parent to a
gradient-boosting fit on the true parents (nonlinear conditional signal), plain correlation on the scenario's 5 pooled
replicates, and whether a discrete column is involved. Reads dev files and the v2 dev ledgers only.

  python analysis/q2_missed_links_study.py semantic 10   -> analysis/results/q2_diag/missed_links_semantic.json
"""
import json, glob, gzip, numpy as np, sys
sys.path.insert(0,'.'); sys.path.insert(0,'ledger')
from score import bench
from kernel import views
from sklearn.ensemble import HistGradientBoostingRegressor as HGB
def r2(Xm, y):
    if Xm.shape[1]==0: return 0.0
    n=len(y); idx=np.arange(n); tr, te = idx[:700], idx[700:]
    m=HGB(max_iter=100).fit(Xm[tr],y[tr]); p=m.predict(Xm[te]); return float(1-((y[te]-p)**2).sum()/((y[te]-y[te].mean())**2).sum())
rows=[]
fam=sys.argv[1]; nf=int(sys.argv[2])
files=sorted(glob.glob(f"/home/claude/work/q2/runs/q2_b1_dev/{fam}/C3/*rep000*.gz"))[:nf]
byname={p.name:p for p in bench.files(fam,split="dev")}
allfiles={p.name:p for p in bench.files(fam)}
for f in files:
    led=json.load(gzip.open(f)); name=f.split("/")[-1].replace(".ledger.json.gz","")
    I=bench.truth_info(fam,name); X=bench.load(byname[name])["values"]; n=X.shape[1]
    pool=np.vstack([bench.load(allfiles[name.replace('rep000','rep%03d'%k)])["values"] for k in range(5) if name.replace('rep000','rep%03d'%k) in allfiles])
    D,U=views.graph_sets(led); adj={frozenset(e) for e in D}|{frozenset(u) for u in U}
    parents={j:[i for i,jj in I["T"] if jj==j] for j in range(n)}
    nuniq=[len(np.unique(X[:,j])) for j in range(n)]
    for (a,b) in I["T"]:
        if frozenset((a,b)) in adj: continue
        pa=parents[b]; others=[p for p in pa if p!=a]
        gain=r2(X[:,pa],X[:,b]) - r2(X[:,others],X[:,b])
        r1=abs(np.corrcoef(X[:,a],X[:,b])[0,1]); rp=abs(np.corrcoef(pool[:,a],pool[:,b])[0,1])
        rows.append(dict(corr=r1, corr_pooled=rp, n_pooled=pool.shape[0], r2_gain=gain, discrete=min(nuniq[a],nuniq[b])<=10, z_pooled=rp*np.sqrt(pool.shape[0]-3)))
g=np.array([r['r2_gain'] for r in rows]); z=np.array([r['z_pooled'] for r in rows]); d=np.array([r['discrete'] for r in rows])
print(fam, "missed true edges examined:", len(rows), "files", len(files))
print("  conditional nonlinear signal (held-out R2 gain from adding the missed parent, oracle parents): median %.3f; >0.02: %.0f%%; >0.05: %.0f%%" % (np.median(g), 100*(g>0.02).mean(), 100*(g>0.05).mean()))
print("  pooled 5 replicates (n=%d): detectable by plain correlation z>3: %.0f%%; z>2: %.0f%%" % (rows[0]['n_pooled'], 100*(z>3).mean(), 100*(z>2).mean()))
print("  involving a discrete column: %.0f%%" % (100*d.mean()))
print("  neither (gain<0.02 and z<3): %.0f%%" % (100*((g<0.02)&(z<3)).mean()))
json.dump(rows, open(f"analysis/results/q2_diag/missed_links_{fam}.json","w"))
