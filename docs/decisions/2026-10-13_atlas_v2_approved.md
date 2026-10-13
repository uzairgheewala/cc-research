# Decision record: Atlas v2 approved; reliability before features (2026-10-13)

Tickets: DEC-06 (done), TEAM-08 (unblocked), DEC-05 (context for the wedge decision).

Uzair, in chat on 2026-10-13 (Pacific), replying to `analysis/reports/site_flow_design.md` and `analysis/reports/ab14_market.md`:

> "I also approve of the site structure it looks much better you're just renovating the existing github pages site right?
> [...] Home page should probably lead with a research but also mention the market/product/wedge with a link to that as
> well. I also agree auditing is definitely more valuable but hey we need a reliable and strong system [...] in things as
> sensitive as these you really need to iron out reliability before anything else becomes remotely worthwhile"

| Decision | What it approves |
|---|---|
| **The site sequence** | The design's four acts and thirteen pages, built in bundles S1-S5. |
| **Where it is built** | The existing GitHub Pages site: same repository, same `site/build.py` and `pages.yml`, publishing `site/_build/`. No second site. The old single page's level links (`#space`, `#bounds`, ...) redirect to the new pages. |
| **The home page** | Leads with the research. It also says where the market, product and wedge stand, with a link to the market page. |
| **The market page** | Public, on the site, with every figure keeping its label from `ab14_market.md`. This follows from the home page linking to it. |
| **The wedge** | Auditing other agents' causal claims is the more valuable product. A reliable, strong system comes first. |

## What "reliability before features" binds

This is the same standard the SAL work holds. It applies to the AB-16 wedge decision and to every build after it. The ledger's guarantees come before any product surface:

- **Invariants I1-I7 hold by construction and are tested:**
  - shuffling columns changes nothing;
  - the same inputs give the same ledger;
  - with no knowledge given, the result equals the data-only result;
  - every claim has evidence, which the checker verifies;
  - knowledge never creates or removes a connection;
  - an intervention outranks a stated name;
  - malformed model output cannot crash a run.
- **The system is never below its own data-only output.**
- **Harm from wrong knowledge is bounded.**
- **Calibration and abstention are measured on held-out data before anyone is asked to trust them.**

An audit product, or any "fun stuff" built on top, waits until those pass. The commercial evidence (AB-14) is context for that choice, not a reason to build features early.
