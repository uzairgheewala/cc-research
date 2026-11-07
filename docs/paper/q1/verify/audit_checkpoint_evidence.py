"""DLV-05/DLV-07: bounded recorded-evidence audit; never runs a live system.

Writes only to --out. Source readback, retained-edge recalculation and raw/native
execution are separate levels. Missing inputs remain gaps, not negative results.
"""
import argparse
from collections import defaultdict
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import statistics
import subprocess
import zlib

import numpy as np

PAPER = Path(__file__).resolve().parents[1]
ROOT = PAPER.parents[2]


def digest(data):
    return hashlib.sha256(data).hexdigest()


def read(root, name, inputs):
    data = (root / name).read_bytes()
    inputs[name] = digest(data)
    return json.loads(data)


def f1(predicted, truth):
    return 2 * len(predicted & truth) / (len(predicted) + len(truth)) if predicted or truth else 0.0


def scoring_audit(root, inputs):
    name = 'analysis/results/methods/fci_semantic_obs.json'
    saved = read(root, name, inputs)
    scores = []
    mismatches = []
    raw_references, missing = 0, []
    for row in saved['rows']:
        if row.get('failed'):
            continue
        rel = 'external/causalarena/scm/semantic/data/semantic_obs_only/' + row['file']
        path = root / rel
        if not path.exists():
            missing.append(rel)
            continue
        inputs[rel] = digest(path.read_bytes())
        with np.load(path, allow_pickle=False) as source:
            truth = {tuple(map(int, pair)) for pair in np.argwhere(source['g'] != 0)}
        if len(truth) != row['true_edges']:
            mismatches.append('reference-count:' + row['file'])
        raw_references += 1
        arrows = {tuple(x) for x in row['directed_edges']}
        pairs = sorted({tuple(sorted(x[:2])) for x in row['undecided_pairs']})
        rng = np.random.default_rng(zlib.crc32(row['file'].encode()))
        random = set(arrows)
        lower = set(arrows)
        for a, b in pairs:
            random.add((a, b) if rng.integers(2) == 0 else (b, a))
            lower.add((a, b))
        rs, ls = f1(random, truth), f1(lower, truth)
        if abs(rs - row['scores']['random']['f1']) > 1e-9 or abs(ls - row['scores']['lower']['f1']) > 1e-9:
            mismatches.append(row['file'])
        scores.append((rs, ls))
    board = read(root, 'analysis/results/rescore_v2/leaderboard_controlled.json', inputs)
    expected = next(x for x in board['table'] if x['method'] == 'FCI' and x['family'] == 'semantic')
    random_mean = round(statistics.mean(x[0] for x in scores), 4) if scores else None
    lower_mean = round(statistics.mean(x[1] for x in scores), 4) if scores else None
    if not missing and (random_mean != expected['ours_released_expectation'] or
            lower_mean != expected['ours_released_authors_rule']):
        mismatches.append('frozen FCI summary differs from retained-edge calculation')
    return {'level': 'retained-edge recalculation plus available public reference bytes',
            'retained_rows': len(saved['rows']),
            'failed_rows_excluded_by_original_analysis': sum(bool(row.get('failed')) for row in saved['rows']),
            'eligible_graphs': len(scores), 'mismatches': mismatches,
            'reference_files_checked': raw_references, 'reference_files_missing': missing,
            'random_mean': random_mean, 'lower_mean': lower_mean,
            'full_reference_cohort_available': not missing,
            'gain_at_paper_precision': format(lower_mean-random_mean, '.3f') if scores and not missing else None,
            'limitation': 'Same retained graphs and per-file seed; no fresh FCI fit or native pipeline run.'}


def name_audit(root, inputs):
    source = read(root, 'analysis/results/ab06/ab06.json', inputs)
    grouped = defaultdict(dict)
    for row in source['rows']:
        if row.get('status') == 'ok' and row.get('f1') is not None:
            grouped[row['agent'], row['scenario']][row['arm']] = row['f1']
    values = {}
    mismatches = []
    for agent, summary in source['agents'].items():
        pairs = [arms['real']-arms['swapped'] for (name, _), arms in grouped.items()
                 if name == agent and 'real' in arms and 'swapped' in arms]
        expected = summary['name_reliance_real_minus_swapped']
        actual = round(statistics.mean(pairs), 4) if pairs else None
        if actual != expected['mean'] or len(pairs) != expected['paired_scenarios']:
            mismatches.append(agent)
        values[agent] = {'paired_scenarios': len(pairs), 'mean_from_retained_scores': actual}
    # Preserve the heterogeneous historical Causal-Copilot entry as such.
    entries = {name: rec['name_reliance_real_minus_swapped'] for name, rec in source['agents'].items()}
    entries.update({name: rec['name_reliance_real_minus_swapped'] for name, rec in source['causal_copilot'].items()
                    if rec.get('counted_in_P9')})
    entered = sorted(name for name, rec in entries.items() if rec['paired_scenarios'] >= source['P9']['min_paired_scenarios'])
    losing = sorted(name for name in entered if entries[name]['mean'] >= 0.10)
    if entered != sorted(source['P9']['systems_entered']) or losing != sorted(source['P9']['losing_ge_0.10']):
        mismatches.append('P9 tally')
    return {'level': 'reaggregation of retained per-scenario scores; heterogeneous tally readback',
            'entries': values, 'entered': entered, 'losing': losing, 'mismatches': mismatches,
            'limitation': 'Does not rerun model queries or re-score every native response. Historical Causal-Copilot stage/cohort/scorer differs; no common-condition ranking.'}


def differences(actual, expected, path=''):
    if isinstance(actual, dict) and isinstance(expected, dict):
        return [item for key in sorted(set(actual) | set(expected)) for item in
                ([path+'/'+key] if key not in actual or key not in expected else differences(actual[key], expected[key], path+'/'+key))]
    if isinstance(actual, list) and isinstance(expected, list) and len(actual) == len(expected):
        return [item for i, (a, e) in enumerate(zip(actual, expected)) for item in differences(a, e, path+'/'+str(i))]
    if isinstance(actual, (int, float)) and isinstance(expected, (int, float)) and not isinstance(actual, bool) and not isinstance(expected, bool):
        return [] if abs(actual-expected) <= 1e-9 else [path]
    return [] if actual == expected else [path]


def causalbench_audit(root, inputs):
    producer = root / 'analysis/ben13/run.py'
    inputs['analysis/ben13/run.py'] = digest(producer.read_bytes())
    spec = importlib.util.spec_from_file_location('retained_ben13_producer', producer)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.OUT = root / 'analysis/results/ben13'
    pre = read(root, 'plans/ben13_prereg.json', inputs)
    saved = read(root, 'analysis/results/ben13/summary.json', inputs)
    for line in ('k562', 'rpe1'):
        for path in (module.OUT / line).glob('*.json'):
            inputs[path.relative_to(root).as_posix()] = digest(path.read_bytes())
    actual = {line: module.summarise_line(line, pre) for line in ('k562', 'rpe1')}
    mismatch = differences(actual, saved['lines'], 'lines')
    prediction_mismatch = differences(module.predictions(actual), saved['predictions'], 'predictions')
    return {'level': 'original summary producer rerun from retained per-cell JSON; not an independent evaluator',
            'mismatches': mismatch + prediction_mismatch,
            'reproduction_rows_within_tolerance': sum(bool(row['within_tolerance']) for line in actual.values() for row in line.get('reproduction', {}).values()),
            'cells_read': sum(line.get('cells', 0) for line in actual.values()),
            'limitation': 'The retained-cell merge checks reported aggregates, controls and predictions. It does not recompute interventions or revalidate the statistical evaluator from raw expression arrays.'}


def inventory(root, inputs):
    relative = 'docs/paper/q1/report.tex'
    data = (root / relative).read_bytes()
    inputs[relative] = digest(data)
    tex = data.decode('utf-8')
    body = tex.split('\\begin{document}', 1)[1].split('\\end{document}', 1)[0]
    paragraphs = []
    for match in re.finditer(r'\S[\s\S]*?(?=\n\s*\n|\Z)', body):
        text = match.group()
        if not re.search(r'[A-Za-z]{4}', re.sub(r'\\\w+\{[^}]*\}', '', text)):
            continue
        line = tex[:tex.index(body)+match.start()].count('\n')+1
        keys = sorted(set(re.findall(r'\\nm\{([^}]+)\}', text)))
        cites = sorted({key.strip() for group in re.findall(r'\\cite\w*\{([^}]+)\}', text) for key in group.split(',')})
        paragraphs.append({'id': 'block-' + str(len(paragraphs)+1).zfill(3), 'source_line': line,
                           'sha256': digest(text.encode()), 'number_keys': keys, 'citation_keys': cites,
                           'text': text, 'judgment': 'inventory only; scientific support requires the recorded reviews and per-finding dispositions'})
    return paragraphs


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--root', type=Path, default=ROOT)
    ap.add_argument('--out', type=Path, required=True)
    args = ap.parse_args(argv)
    root, inputs = args.root.resolve(), {}
    blocks = inventory(root, inputs)
    contract = read(root, 'docs/paper/q1/checkpoint_contract.json', inputs)
    registry = read(root, 'docs/paper/q1/numbers.json', inputs)
    source_coverage = {}
    for name, expected in contract['number_source_sha256'].items():
        read(root, name, inputs)
        source_coverage[name] = {'sha256': inputs[name], 'matches_frozen_source': inputs[name] == expected,
                                 'keys': [e['key'] for e in registry['entries'] if e.get('file') == name or any(a.get('file') == name for a in e.get('args', []))]}
    scoring = scoring_audit(root, inputs)
    names = name_audit(root, inputs)
    causalbench = causalbench_audit(root, inputs)
    diagnostic = read(root, 'docs/paper/q1/checkpoint_evidence/rebase_facts-2026-11-03.json', inputs)
    stages = diagnostic['stages']['main']
    largest = min(stages['transitions'], key=lambda x: x['point'])
    ben = read(root, 'analysis/results/ben13/summary.json', inputs)
    findings = [
        {'id': 'scoring', 'status': ('recalculated' if scoring['eligible_graphs'] and scoring['full_reference_cohort_available']
                                   else 'partial recalculation' if scoring['eligible_graphs'] else 'unavailable'), 'evidence': scoring},
        {'id': 'names', 'status': 'partly recalculated', 'evidence': names},
        {'id': 'stages', 'status': 'diagnostic readback; independent stage rerun remains open',
         'evidence': {'completed': stages['completed'], 'runs': stages['runs'], 'largest_paired_transition': largest,
                      'cycle_step': stages['cycle_step']},
         'limitation': 'The committed diagnostic is not the original intermediate-state archive. Public source ZIP lacks full stage states and model-call records.'},
        {'id': 'causalbench', 'status': 'retained-cell summary producer rerun; raw intervention evaluation remains open',
         'evidence': causalbench,
         'limitation': 'A recorded within-tolerance flag is not a fresh reproduction. Raw filtered intervention arrays and evaluator environment are separate inputs.'},
        {'id': 'label-following', 'status': 'frozen counts and historical endpoint discrepancy retained',
         'limitation': 'No confirmatory endpoint claim; specified pre-cycle and computed final-output endpoints differ. No protocol amendment.'},
        {'id': 'matmcd', 'status': 'frozen point and interval interpretation retained; no fresh native rerun',
         'limitation': 'Point below its data-only graph does not establish interval exclusion. See frozen MATMCD diagnostic report.'},
        {'id': 'data-and-licences', 'status': 'frozen mapping/source readback',
         'limitation': 'Reference identity and documented provenance do not independently establish ground truth; no fresh licence/legal determination.'},
        {'id': 'literature-and-architecture', 'status': 'prior scoped reviews retained; current exact native coverage separate',
         'limitation': 'Inventory and source identity are not a new full-text corpus review or independent scientific validation of S1-S4.'},
    ]
    result = {'tickets': ['DLV-05', 'DLV-07'], 'created_at': datetime.now(timezone.utc).isoformat(),
              'manuscript_sha256': inputs['docs/paper/q1/report.tex'], 'tool_sha256': digest(Path(__file__).read_bytes()),
              'source_coverage': source_coverage, 'registry_entries': len(registry['entries']),
              'blocks': blocks, 'findings': findings, 'inputs': inputs,
              'native_execution': False, 'paid_calls': 0, 'whole_paper_reproduction': False,
              'correlation': 'Single audit implementation; independent formula for retained FCI edges, not an independent reviewer or new experiment.'}
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')
    failed = scoring['mismatches'] + names['mismatches'] + causalbench['mismatches'] + [name for name, rec in source_coverage.items() if not rec['matches_frozen_source']]
    print(json.dumps({'blocks_in_inventory': len(blocks), 'registry_entries': len(registry['entries']),
                      'number_sources': len(source_coverage), 'FCI': scoring, 'name_controls': names, 'causalbench': causalbench,
                      'failed': failed, 'whole_paper_reproduction': False}, indent=2))
    return 1 if failed else 0


if __name__ == '__main__':
    raise SystemExit(main())
