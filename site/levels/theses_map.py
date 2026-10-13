from common import *

QN = ["Experiments", "Effects", "Orientation", "Skeleton"]   # top to bottom
RN = ["D", "D+I", "D+K", "D+I+K"]
SK, OR, EF, EX = "Skeleton", "Orientation", "Effects", "Experiments"

MAP = [
    ("T1", "P1", "Order source explains accuracy", "Partly refuted", "dec",
     [(SK, "D"), (OR, "D"), (SK, "D+I"), (OR, "D+I")],
     "R = D and D+I, every method we can run",
     "explains a system's q (and c) by where its order came from; does not move anyone"),
    ("T2", "P1", "Agents take order from names and layout", "Supported on S2", "done",
     [(SK, "D+K"), (OR, "D+K"), (OR, "D")],
     "the K column, controlled by name arm; the layout leak in D",
     "measures the shift in (S, c, q) between real, neutral and swapped names with columns shuffled"),
    ("T3", "P2", "A typed, sourced partial order", "In progress", "prog",
     [(SK, "D+K"), (OR, "D+K"), (SK, "D+I+K"), (OR, "D+I+K"), (OR, "D+I")],
     "rungs 1–2 in the K columns; interventions as order evidence",
     "moves a system straight up: c and q rise, S is untouched by knowledge (I5) and never below data-only (I3)"),
    ("T4", "P2", "Calibrated claims that can abstain", "Not started", "todo",
     [(SK, "D+K"), (OR, "D+K"), (SK, "D+I+K"), (OR, "D+I+K")],
     "same cells as T3, scored by a fourth view: precision at a stated coverage",
     "chooses c claim by claim: commit only where calibrated q exceeds ½ (∂F1/∂c = S(q − ½))"),
    ("T5", "P3", "What-if answers with identification status", "Surveyed", "p3",
     [(EF, r) for r in RN],
     "rung 3, every regime",
     "turns a into answers: each direction fixed shrinks the set of possible effects toward one value"),
    ("T6", "P3", "Experiments that beat random", "Data ready", "p3",
     [(EX, "D+I"), (EX, "D+I+K")],
     "rung 4; moves a problem from the D column to the D+I column",
     "picks the target that raises κ most: the experiment that settles the most open directions"),
]


def mini(cells, colour, tint):
    on = set(cells)
    rows = []
    for q in QN:
        rows.append(f'<span style="font-size: 10px; line-height: 14px; color: #4E5751; text-align: right; padding-right: 4px">{q}</span>')
        for r in RN:
            hit = (q, r) in on
            st = f"background: {tint}; border: 1.5px solid {colour}" if hit else "background: #FFFFFF; border: 1px solid #DADDD6"
            rows.append(f'<span style="height: 14px; border-radius: 3px; {st}"></span>')
    head = '<span></span>' + "".join(f'<span style="font-size: 10px; line-height: 12px; color: #4E5751; text-align: center">{r}</span>' for r in RN)
    return f'<div style="display: grid; grid-template-columns: 76px repeat(4, 30px); gap: 3px; align-items: center">{"".join(rows)}{head}</div>'


def spacemap():
    cards = []
    for tid, pid, title, st_text, st, cells, region, moves in MAP:
        col, tint, _ = PILLAR[pid]
        cards.append(f"""<div style="padding: 14px 16px; background: #FFFFFF; border: 1px solid #C9CEC6; border-top: 4px solid {col}; border-radius: 10px; display: flex; flex-direction: column; gap: 10px">
<div style="display: flex; flex-wrap: wrap; align-items: center; gap: 8px"><span style="font-family: {MONO}; font-weight: 600; color: {col}">{tid}</span><span style="font-weight: 600">{title}</span>{pill(st_text, st)}</div>
<div style="display: flex; flex-wrap: wrap; gap: 14px; align-items: flex-start">
{mini(cells, col, tint)}
<div style="flex: 1 1 200px; font-size: 13px; line-height: 18px; display: flex; flex-direction: column; gap: 6px">
<span><b>Region:</b> {region}</span>
<span><b>What it does there:</b> {moves}</span>
</div></div></div>""")
    # coverage overlay
    cov = {}
    for tid, pid, *_rest in MAP:
        for cell in _rest[3]:
            cov.setdefault(cell, []).append((tid, PILLAR[pid][0]))
    grid = ['<span></span>'] + [f'<span style="font-size: 13px; font-weight: 600; text-align: center">{r}</span>' for r in RN]
    for q in QN:
        grid.append(f'<span style="font-size: 13px; font-weight: 600; text-align: right; padding-right: 6px">{q}</span>')
        for r in RN:
            ts = cov.get((q, r), [])
            inner = " ".join(f'<span style="font-family: {MONO}; font-size: 12px; font-weight: 600; color: {c}">{t}</span>' for t, c in ts) or '<span style="font-size: 12px; color: #8E2A2A">no thesis</span>'
            bd = "2.5px solid #B85A12" if (q, r) == (OR, "D+K") else ("1.5px dashed #8E2A2A" if not ts else "1px solid #C9CEC6")
            grid.append(f'<span style="min-height: 40px; padding: 6px 8px; background: #FFFFFF; border: {bd}; border-radius: 6px; display: flex; flex-wrap: wrap; gap: 4px 8px; align-items: center">{inner}</span>')
    overlay = f'<div style="display: grid; grid-template-columns: 110px repeat(4, minmax(90px, 1fr)); gap: 6px; align-items: stretch">{"".join(grid)}</div>'
    return f"""<section style="display: flex; flex-direction: column; gap: 14px">
{h2("Which part of the space each thesis addresses")}
<p style="margin: 0; max-width: 980px; color: #2C3631">Each thesis owns a region of the Q × R grid from Level 1 and does one thing in the performance space (S, c, q) from Level 2. The small grids mark the region; the overlay shows how the six cover the whole slice. The thick cell is the thesis cell. Two cells have no thesis: experiments in D and D+K, where no experiment can be run; T6 starts once interventions are on the table.</p>
<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(400px, 1fr)); gap: 12px">{''.join(cards)}</div>
<div style="padding: 16px 18px; background: #FFFFFF; border: 1px solid #C9CEC6; border-radius: 12px; display: flex; flex-direction: column; gap: 10px; overflow-x: auto">
{tag("Overlay · theses per cell, Q1 setting", "#17201B")}
{overlay}
</div>
</section>"""
