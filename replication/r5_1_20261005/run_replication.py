"""Public summary replay and optional hash-bound refits using lawfully obtained inputs.

The public default does not estimate models from row-level GDP observations.
No network access, raw-source download, filling or new specification is performed.
"""
from pathlib import Path
import argparse
import csv
import hashlib
import json
import sys

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / 'code'))
import frozen_validation as methods
import bootstrap_refit

KEYS = ['source_panel', 'analysis', 'product', 'benchmark']


def digest(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for block in iter(lambda: stream.read(1048576), b''):
            h.update(block)
    return h.hexdigest()


def read(path):
    return pd.read_csv(path, dtype={'city_code': str, 'province_code': str})


def check_hashes():
    records = read(ROOT / 'PACKAGE_SHA256.csv')
    for row in records.itertuples():
        target = (ROOT / row.relative_path).resolve()
        if not target.is_relative_to(ROOT.resolve()):
            raise ValueError('Unsafe package path')
        if digest(target) != row.sha256:
            raise ValueError('Package fingerprint mismatch: ' + row.relative_path)
    return len(records)


def replay_summaries():
    annual = []
    for kind in ['standalone', 'conditional']:
        q = read(ROOT / 'reference' / ('R5_source_panel_' + kind + '_results.csv'))
        q['analysis'] = kind
        annual.append(q)
    annual = pd.concat(annual, ignore_index=True)
    rows = []
    for key, q in annual.groupby(KEYS):
        n = int(q.N.sum())
        m, b = q.model_SSE.sum(), q.baseline_SSE.sum()
        skill_col = 'conditional_skill' if key[1] == 'conditional' else 'standalone_skill'
        rows.append(dict(zip(KEYS, key), N_observations=n, pooled_model_SSE=m,
            pooled_baseline_SSE=b, pooled_skill=1-m/b,
            equal_year_mean_skill=q[skill_col].mean(), model_RMSE=np.sqrt(m/n),
            baseline_RMSE=np.sqrt(b/n),
            model_MAE=np.average(q.model_MAE, weights=q.N),
            baseline_MAE=np.average(q.baseline_MAE, weights=q.N),
            mean_delta_loss=(m-b)/n,
            equal_year_mean_delta_loss=q.mean_delta_loss.mean()))
    result = pd.DataFrame(rows)
    reference = read(ROOT / 'reference/R5_source_panel_domain_summary.csv')
    matched = result.merge(reference, on=KEYS, suffixes=('_new', '_reference'), validate='one_to_one')
    assert len(matched) == len(reference) == 64
    columns = [c for c in result.columns if c not in KEYS]
    for col in columns:
        if not np.allclose(matched[col+'_new'], matched[col+'_reference'], atol=2e-12, rtol=2e-11):
            raise AssertionError('Summary replay mismatch: ' + col)
    return result, len(matched) * len(columns)


def format_number(value, places):
    return f'{value:.{places}f}'.replace('-', '\u2212')


def table3(domain):
    points = domain[domain.analysis.eq('conditional')].set_index(['product', 'benchmark', 'source_panel'])
    intervals = read(ROOT / 'reference/R5_extension_loss_uncertainty.csv')
    intervals = intervals[intervals.source_panel.eq('P4') & intervals.contrast.eq('conditional_M1_minus_M0')].set_index(['product', 'benchmark'])
    source = ROOT / 'tables/Table_3.csv'
    with source.open(encoding='utf-8-sig', newline='') as stream:
        expected = list(csv.reader(stream))
    rows = [expected[0]]
    for product in ['EOG', 'Black Marble']:
        for benchmark in methods.BENCHMARKS:
            ci = intervals.loc[(product, benchmark)]
            rows.append([product, benchmark] + [format_number(points.loc[(product, benchmark, panel), 'pooled_skill'], 4)
                for panel in ['P1', 'P4']] + [format_number(ci.mean_loss_difference_point*1e4, 3),
                '[' + format_number(ci.CI95_lower*1e4, 3) + ', ' + format_number(ci.CI95_upper*1e4, 3) + ']'])
    assert rows == expected, 'Published Table 3 formatting/value mismatch'
    return rows


def summary_from_predictions(pred, kind, panel):
    if kind == 'standalone':
        chunks = []
        for benchmark in methods.BENCHMARKS:
            q = pred.copy()
            q['benchmark'] = benchmark
            q['p0'] = q['predicted_' + benchmark]
            chunks.append(q)
        data = pd.concat(chunks, ignore_index=True)
        yc, y, p1, p0 = 'target_year', 'actual_gdp_growth', 'predicted_light_mapping', 'p0'
    else:
        data = pred
        yc, y, p1, p0 = 'prediction_year', 'y', 'predicted_M1', 'predicted_M0'
    rows = []
    for (product, benchmark), q in data[data[yc].ge(2022)].groupby(['product', 'benchmark']):
        a, b = (q[y]-q[p1])**2, (q[y]-q[p0])**2
        rows.append(dict(source_panel=panel, analysis=kind, product=product, benchmark=benchmark,
            N_observations=len(q), pooled_model_SSE=a.sum(), pooled_baseline_SSE=b.sum(),
            pooled_skill=1-a.sum()/b.sum(), mean_delta_loss=(a-b).mean()))
    return pd.DataFrame(rows)


def refit_models(input_dir, output_dir, bootstrap):
    registry = read(ROOT / 'RESTRICTED_INPUT_SHA256.csv')
    panels = {}
    for row in registry.itertuples():
        path = input_dir / row.filename
        if not path.is_file():
            raise FileNotFoundError('Restricted input unavailable: ' + row.filename + '. Contact the corresponding author; obtain lawful access first.')
        if digest(path) != row.sha256:
            raise ValueError('Frozen statistical input mismatch: ' + row.filename)
        panels[row.source_panel] = read(path)
    methods.domain_for = lambda year, conditional=False: ('primary_high_coverage' if year <= 2019
        else 'near_national_stress' if year <= 2021 else 'post2021_extension')
    prediction_sets, summaries = {}, []
    for panel in ['P1', 'P2', 'P4']:
        data = panels[panel]
        assert data.city_code.nunique() == 296 and data.province_code.nunique() == 31
        assert data.loc[data.year.ge(2022), 'transformed_log_growth_extended'].notna().sum() == 888
        stand, _ = methods.run_standalone(data)
        conditional, _, leakage = methods.run_conditional(data)
        assert leakage.violations.eq(0).all()
        prediction_sets[panel] = (stand, conditional)
        for kind, pred in [('standalone', stand), ('conditional', conditional)]:
            summaries.append(summary_from_predictions(pred, kind, panel))
    keys = panels['P3'].loc[panels['P3'].year.ge(2022) & panels['P3'].transformed_log_growth_extended.notna(), ['city_code', 'year']]
    assert len(keys) == 482
    for kind, pred in zip(['standalone', 'conditional'], prediction_sets['P1']):
        yc = 'target_year' if kind == 'standalone' else 'prediction_year'
        subset = pred.merge(keys, left_on=['city_code', yc], right_on=['city_code', 'year'], validate='many_to_one')
        summaries.append(summary_from_predictions(subset, kind, 'P3'))
    results = pd.concat(summaries, ignore_index=True)
    frozen = read(ROOT / 'reference/R5_source_panel_domain_summary.csv')
    q = results.merge(frozen, on=KEYS, suffixes=('_new', '_reference'), validate='one_to_one')
    checks = 0
    for column in ['N_observations', 'pooled_model_SSE', 'pooled_baseline_SSE', 'pooled_skill', 'mean_delta_loss']:
        assert np.allclose(q[column+'_new'], q[column+'_reference'], atol=2e-12, rtol=2e-11), column
        checks += len(q)
    results.to_csv(output_dir / 'refitted_extension_metrics.csv', index=False, float_format='%.17g')
    # Historical rows are invariant to the alternative post-2021 outcomes.
    for kind, index, yc, numeric in [
        ('standalone', 0, 'target_year', ['actual_gdp_growth', 'predicted_light_mapping'] + ['predicted_'+b for b in methods.BENCHMARKS]),
        ('conditional', 1, 'prediction_year', ['y', 'predicted_M0', 'predicted_M1'])]:
        base = prediction_sets['P1'][index]
        identity = ['product', 'city_code', yc] + (['benchmark'] if kind == 'conditional' else [])
        for panel in ['P2', 'P4']:
            joined = base[base[yc].le(2021)].merge(prediction_sets[panel][index].query(f'{yc} <= 2021'), on=identity,
                suffixes=('_p1', '_alternative'), validate='one_to_one')
            assert len(joined) == len(base[base[yc].le(2021)])
            for col in numeric:
                assert np.allclose(joined[col+'_p1'], joined[col+'_alternative'], atol=1e-12, rtol=0)
                checks += 1
    bootstrap_checks = 0
    if bootstrap:
        rng = np.random.default_rng(20261002)
        W = rng.multinomial(31, np.repeat(1/31, 31), size=9999)
        intervals = read(ROOT / 'reference/R5_extension_loss_uncertainty.csv')
        interval_rows = []
        for panel in ['P1', 'P2', 'P4']:
            draws, _ = bootstrap_refit.evaluate(panels[panel], methods, W)
            point, _ = bootstrap_refit.evaluate(panels[panel], methods, np.ones((1,31), dtype=int))
            for row in intervals[intervals.source_panel.eq(panel)].itertuples():
                k = (row.product, row.benchmark)
                lo, hi = np.quantile(draws[k]['mean_delta_loss'], [.025, .975])
                value = point[k]['mean_delta_loss'][0]
                assert np.allclose([value, lo, hi], [row.mean_loss_difference_point, row.CI95_lower, row.CI95_upper], atol=2e-12, rtol=2e-11)
                bootstrap_checks += 3
                interval_rows.append(dict(source_panel=panel, product=row.product, benchmark=row.benchmark,
                    mean_loss_difference_point=value, CI95_lower=lo, CI95_upper=hi, draws=9999, seed=20261002))
            print('Bootstrap refit completed:', panel, flush=True)
        pd.DataFrame(interval_rows).to_csv(output_dir / 'refitted_loss_intervals.csv', index=False, float_format='%.17g')
    return {'model_metric_checks': checks, 'bootstrap_numeric_checks': bootstrap_checks,
            'raw_source_certification_rerun': False,
            'scope': 'processed_input_statistical_refit_not_a_public_data_release'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    parser.add_argument('--reproduce-summaries', action='store_true')
    parser.add_argument('--refit', action='store_true')
    parser.add_argument('--inputs', type=Path)
    parser.add_argument('--bootstrap', action='store_true')
    parser.add_argument('--output', type=Path, default=ROOT / 'generated')
    args = parser.parse_args()
    if args.bootstrap and not args.refit:
        parser.error('--bootstrap requires --refit')
    hashes = check_hashes()
    domain, checks = replay_summaries()
    rows = table3(domain)
    result = {'package_hashes_verified': hashes, 'summary_numeric_checks': checks,
        'submission_table3_data_cells_verified': 48, 'public_summary_reproduction': 'PASS',
        'row_level_model_refit': 'NOT_RUN_RESTRICTED_INPUTS_NOT_INCLUDED'}
    if args.reproduce_summaries or args.refit:
        args.output.mkdir(parents=True, exist_ok=True)
        domain.to_csv(args.output / 'source_panel_metrics_from_annual_summaries.csv', index=False, float_format='%.17g')
        with (args.output / 'Table_3.csv').open('w', encoding='utf-8-sig', newline='') as stream:
            csv.writer(stream).writerows(rows)
    if args.refit:
        if args.inputs is None:
            parser.error('--refit requires --inputs pointing to lawfully obtained frozen statistical files')
        result.update(refit_models(args.inputs.resolve(), args.output.resolve(), args.bootstrap))
        result['row_level_model_refit'] = 'PASS_WITH_SEPARATELY_SUPPLIED_INPUTS'
    if args.reproduce_summaries or args.refit:
        (args.output / 'reproduction_status.json').write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
