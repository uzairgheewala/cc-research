# AB-14 market hypotheses: how the two vertical briefs will be built

Ticket: AUD-45 (bundle AB-14). Scaffolding written 2026-10-12. **No market size is stated here, and none will be stated
without the inputs it is computed from.** The briefs are built after AB-10's interviews exist, from public pricing
(AB-11) and the regulation map (AB-13).

## Where we are now

The audit DAG makes AB-14 depend on AB-10 (interviews) and AB-13 (regulation map). Its gate is "no number without its
inputs", and its must-show is "two one-page vertical briefs":
- **IT incident analysis** (AIOps root-cause analysis);
- **marketing measurement** (incrementality and MMM).

So far there are price points, but no buyer counts and no adoption evidence:
- AU5 and AB-11 hold public price points, almost all vendor claims or second-hand.
- AU5 flags the only market-size figures found ("causal AI" USD 56.2M in 2024 to 456.8M by 2030) as second-hand, from
  a paid report whose method was not read. They define the category to exclude experimentation and MMM spend.

**Those figures are not inputs to these briefs.** They may be quoted once, labelled second-hand, as context.

## Inputs

### From AB-11: `analysis/audits/AB11_vendor_claims.json`, key `pricing_signals`

Each row has `vertical`, `vendor`, `price_point`, `unit`, `url` and `label`. Index numbers below are positions in the
list as of 2026-10-12. Cite rows by vendor, not by index, because the list may grow.

| Vertical | Rows | Price unit | Use in the brief |
|---|---|---|---|
| IT incident analysis | Causely (flat, per account-month, up to 500 services); Datadog Bits Investigation (per credit, about 6.5 credits per investigation); Dynatrace (per host-month including RCA; per AI unit, about 30 per investigation); AWS DevOps Agent (per agent-second); CloudWatch investigations (quota, no price); PagerDuty AIOps (from a monthly fee); Datadog Watchdog (bundled); causaLens decisionOS (per licence-year, via AU5) | per investigation **or** flat platform fee | price inputs `p_inv` (per investigation) and `p_flat` (per buyer-year) |
| Marketing measurement | Haus (ACV, second-hand, sample size unstated); Recast (internally inconsistent, **do not use**, per AB-11); Lifesight and Mutinex (no price); Meridian and Robyn (free: price floor); Haus funding; EMARKETER/TransUnion survey (second-hand) | annual contract value | price input `p_acv`; the survey shares are context only, not adoption rates (see the rules below) |

AB-11's own guidance stands:
- Size AIOps from about USD 3-8.45 per investigation, plus flat platform fees.
- For marketing, use Haus's ACV as one labelled second-hand point.
- Do not use Recast's aggregator figure.

### From AB-13: `analysis/audits/AB13_regulation_map.json` (rows) and `AB13_regulation_map.md`

AB-13 supplies **budget-line and buyer arguments, not numbers**. Use each row's `instrument`, `status`, `locator`,
`gap` and `label`.

- **IT incident analysis.**
  - AB-13 finds the EU AI Act is not a near-term driver: Annex III duties start 2 Dec 2027, and RCA is not an Annex
    III area as such.
  - Arts. 12-14 (logging, transparency, human oversight) are design targets only.
  - The brief must say regulation is **not** the buying reason here; speed and cost per investigation are (AU5 F5).
- **Marketing measurement.** No row in AB-13 applies directly, and the brief must say so. For financial services,
  the SR 26-2 row (generative and agentic AI out of scope) is a footnote on why an LLM-fronted tool has no ready
  validation route in banks.
- **Not a brief here, but recorded.** RWE has the strongest regulatory hooks (AB-13 rows 1-30). AB-14 covers only
  the two verticals the DAG names. If AB-10 interviews show RWE demand, that becomes a note for AB-16, not a third
  brief.

### From AB-10: `analysis/results/interviews/synthesis.json`, after interviews

**Interviews are qualitative inputs only.** With 5-8 people, they cannot give an adoption rate.

| Interview field | Feeds |
|---|---|
| `adoption_signals.budget_owner_named` + paraphrases | the **buyer** and **budget line** in each brief (who signs; which budget the money comes from) |
| `adoption_signals.current_spend_band` | a **sanity range** for `p_flat` / `p_acv` (do the public prices fall in the band practitioners report?) |
| `artefacts.*` scores and `would_try` | which product shape the brief describes (provenance layer, abstaining answers, name-swap audit) |
| H1 / H3 verdicts | whether the brief's value proposition is "supported", "inconclusive" or "refuted" by the interviews; printed as is |
| `consent.path` | path (a) interview content may feed the internal briefs but not any paper (`docs/interviews/human_subjects_check.md`) |

## The bottom-up formula

For each vertical:

```
annual_revenue_potential = buyers x adoption x price_per_buyer_year

  IT incident analysis:   price_per_buyer_year = investigations_per_buyer_year x p_inv
                                                 (or p_flat, for flat-fee products; report both, never add them)
  Marketing measurement:  price_per_buyer_year = p_acv
```

| Symbol | Meaning | Where it must come from |
|---|---|---|
| `buyers` | organisations in the segment that have the problem and a budget line for it (for example, companies running an on-call SRE function above a size band; advertisers above a media-spend band running MMM or lift tests) | a cited public count (census or industry dataset, vendor customer counts, survey with stated n), with the segment definition written out |
| `adoption` | share of `buyers` that would adopt a product like this within a stated horizon | **a scenario parameter**, given as low/mid/high with a stated rationale; cite an external analogue if one exists. Never computed from interview counts. |
| `investigations_per_buyer_year` | how many RCA investigations a buyer runs per year | a cited source (vendor quota or usage disclosure, incident-volume survey); an interview band can bound it but not set it |
| `p_inv`, `p_flat`, `p_acv` | price points | AB-11 `pricing_signals` rows as above, with their labels |

Report all three scenarios. Show the multiplication, not just the product.

## Rules every number follows

1. **Every number carries its inputs.** Each figure in a brief is a row in a table of quantity, value, unit, formula
   (if derived), inputs (row ids of other figures), source (file and row, or URL and access date), and label. A figure
   without inputs or a source is not printed.
2. **Every derived number is labelled `estimate`.** Inputs keep their original labels: `claim (vendor)`,
   `second-hand`, `read (primary)`, `assumption (scenario)` or `interview (qualitative)`. A product of inputs takes the
   weakest label among them, plus `estimate`.
3. **No invented market sizes.**
   - If a required input has no source, the brief prints `missing` in that cell, and the derived figures stay
     `not computed`.
   - Do not fill gaps with round guesses.
   - Third-party "market size" figures (AU5 F1 and section 3) are context only and never enter the formula.
4. **Interviews never become rates.** "3 of 7 would try" is reported as that sentence, not as "43% adoption".
5. **Ranges, not points, for scenario inputs.** The output is a range across low/mid/high, and the brief says which
   input moves it most.
6. **Dates.** Every web source carries the date it was read, since prices change.

## Brief layout (one page each)

1. **Buyer and budget line**: from interviews (role, never person) plus AU5 F5.
2. **The decision the product serves**: from the AB-10 decisions typed `rca` or `intervention`.
3. **Price anchors**: the AB-11 rows, with labels.
4. **Regulatory pull**: AB-13 rows, or "none found".
5. **Bottom-up table**: buyers x adoption x price, for low/mid/high, with every input row.
6. **What would change the estimate**: the input with the widest range, and how to narrow it.
7. **Status of H1/H3 for this vertical**: verdicts copied from `synthesis.json` (sector counts only; no per-sector
   verdict).

Output: `analysis/reports/ab14_market.md`, as named in `plans/audit_dag.json`, holding both briefs.

## Where we're going

AB-14's window opens 27 Oct. Before then, the open inputs are `buyers` and `investigations_per_buyer_year`. Each needs
a cited public source per vertical, found in a desk pass. The interview-derived buyer and budget-line rows wait for
AB-10's synthesis.
