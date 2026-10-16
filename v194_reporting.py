"""Selected, excluded, and adopted supports, distinct from performance claims."""
from __future__ import annotations
from collections import Counter
from pathlib import Path
import pandas as pd
from v19_config import FACTORS
from v194_factors import input_support


def sparse_summary(fits):
    rows=[]
    for h in sorted({r['horizon'] for r in fits}):
        cases=[r for r in fits if r['horizon']==h]
        counts=Counter(k for r in cases for k in r.get('selected_factors',[]))
        for k in FACTORS:
            weights=[r.get('challenger_weights',{}).get(k,0.) for r in cases if r.get('challenger_weights')]
            rows.append({'horizon':h,'factor':k,'candidate_cases':len(weights),
                         'selected_cases':counts[k], 'mean_candidate_weight':sum(weights)/len(weights) if weights else None,
                         'adopted_cases':sum(r.get('status')=='SPARSE_INNER_VALIDATION_ACCEPTED' and r.get('challenger_weights',{}).get(k,0)>0 for r in cases),
                         'not_a_probability':True})
    return rows


def export_sparse(output, report):
    from v19_data import atomic_csv,atomic_json
    output=Path(output);rows=[];latest=[]
    for r in report.get('fits',[]):
        for k in FACTORS:
            w=r.get('challenger_weights',{}).get(k,0.)
            rows.append({'cutoff':r['cutoff'],'horizon':r['horizon'],'factor':k,'candidate_weight':w,
                'adopted_weight':r.get('weights',{}).get(k,0.),'selected':w>0,
                'state':'SELECTED' if w>0 else r.get('excluded',{}).get(k,'NOT_SELECTED'),
                'fit_status':r.get('status'),'training_coverage':r.get('feature_coverage',{}).get(k)})
    for h,b in report.get('weights',{}).items():
        info=b.get('fit',{});candidate=info.get('challenger_weights',{})
        for k in FACTORS:
            latest.append({'horizon':int(h),'factor':k,'candidate_weight':candidate.get(k,0.),
                           'adopted_weight':b.get('weights',{}).get(k,0.),
                           'selected':candidate.get(k,0.)>0,'fit_status':info.get('status')})
    atomic_csv(output/'sparse_factor_selection.csv',pd.DataFrame(rows))
    atomic_csv(output/'sparse_latest_weights.csv',pd.DataFrame(latest))
    atomic_csv(output/'sparse_selection_summary.csv',pd.DataFrame(report.get('sparse_selection_summary',[])))
    atomic_json(output/'sparse_protocol.json',{'version':report.get('version'),'settings':report.get('settings'),
        'subset_search':'nested_purged_forward_backward_swap_bounded','global_optimum_proven':False,
        'original_factors_forced_into_candidate':False,'deleted_factors_restored_by_shrinkage':False,
        'financial_revision_ledger_verified':False,'strict_candidate_input_coverage':1.0,
        'development_data_not_new_blind_holdout':True,
        'entry_exit_and_commissions':'see settings; hypothetical not executed',
        'equity_universe_is_not_historical_membership':True})


def sparse_markdown(report):
    if report.get('settings',{}).get('factor_design')!='sparse_v194':return ''
    out=['## Sparse subset selection (V19.4)', '',
         'Legacy is an independent control, NOT a mandatory component in a challenger.',
         'Every original factor can be zero. Shrinkage only acts within the positive learned support.',
         'Search, coefficient fitting, and the final adoption test use separate chronological stages.',
         'Search is bounded, not proof of a global optimum. Control and cash results remain separate.',
         'Quarter-end dates are not publication timestamps. Default strict financial mode excludes undated statements.',
         'Optional lagged financial research assumes availability and does not establish original unrevised PIT data.', '',
         '| Horizon | Latest selected research factors | Adopted factors | Status |',
         '|---|---|---|---|']
    for h,b in report.get('weights',{}).items():
        info=b.get('fit',{});candidate=info.get('challenger_weights',{})
        text=', '.join(f'{k}: {100*v:.2f}%' for k,v in candidate.items() if v>0) or 'No fitted candidate'
        adopted=', '.join(f'{k}: {100*v:.2f}%' for k,v in b.get('weights',{}).items() if v>0)
        out.append(f'| {h} | {text} | {adopted} | {info.get("status")} |')
    out += ['', 'Detailed per-date included/excluded masks: sparse_factor_selection.csv.',
            'Selection frequency is not a hit probability. Zero data coverage is NOT evidence of zero predictive value.']
    return '\n'.join(out)
