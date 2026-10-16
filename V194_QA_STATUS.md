# Alpha Radar V19.4 | Validation status

## Scope

Implemented sparse factor selection followed by within-support coefficient fitting.
This document concerns the ONE V19.4 full release based on V19.3 / 91 files.
It does not certify an optimal investment strategy, complete fundamentals,
original public-disclosure timing, actual execution or profitable live trading.

## Engineering tests actually completed

- Final source suite: **261 passed in 289.02 seconds**.
- Earlier intermediate suite: 253 passed; these are included in the final 261,
  not additional distinct tests.
- New sparse-feature tests: **44 passed**, included in the 261 (not 44 more).
- Python source compilation: PASS.
- Python 3.11 grammar parsing of all source files: PASS. Runtime here: Python 3.13.5.
- Three main pages using the user's complete historical factor panel and report,
  with a Streamlit test double: no error calls. Tables contained actual sparse
  masks/weights and candidate returns, not just empty synthetic page placeholders.
- Browser/Streamlit Cloud execution: NOT_TESTED. Streamlit is not installed here;
  the install attempt could not obtain it from the configured package index.
- External market/fundamental endpoint connectivity: NOT_VALIDATED in this release.
  HTTP/data adapters are covered by mocked response/cache/failure tests.

### New tests cover

- Original factors can all be excluded; exact zeros survive every shrink/normalize step.
- Uninformative or negative ridge coefficients can be zero; singleton controls exist.
- Parent/composite conflicts, interaction input counts, input and search-budget bounds.
- Purged chronological folds; changing outer future labels cannot change past fits.
- A constructed synthetic edge can pass the unchanged final gate (not market proof).
- Required missing selected inputs exclude a stock without per-stock renormalization.
- Actual sparse ranking matches fast replay arrays; selected missing future outcomes
  stay missing and are not replaced by stocks with known outcomes.
- Feature prefix invariance, finite scale, no fabricated fundamental values.
- Quarter end is not publication date; explicit lag mode is tagged NOT_PIT.
- Availability uses all contributing inputs; negative EPS base is not false growth.
- Annual cash-flow versus four-quarter income alignment, daily PE availability.
- Optional API caching, per-dataset failure isolation, imported ledger on both
  download+validate and cache-only paths, disabled evidence ignored.
- Changing subset settings does not silently reuse an incompatible last fit.
- Candidate return percentages are formatted correctly, included/excluded tables
  distinguish ranking use from adoption, and export files contain explicit zeros.
- Checkpoint fingerprint includes the new numerical modules.

Old tests that explicitly test the prior engine now set its design explicitly.
Version/count expectations were updated. Historical price/return/control assertions
were not weakened to make the sparse redesign pass.

## Supplied-price development replay actually completed

- 63,928 daily records, 92 symbols including 0050 (91 equities).
- Supplied data period: 2023-10-16 through 2026-10-15.
- 100 seeded cutoffs, 5/20/60 sessions, 300 outer case fits.
- Origin: user-supplied Yahoo_daily history. Not independently exchange-verified.
- Original baseline: 300 case completeness/missing states reproduced exactly;
  294 finite returns, maximum absolute error 2.220446049250313e-16.
- Final numerical source digest matches the replay checkpoint manifest.
- No optional fundamental/ownership source records were present. Their empirical
  efficacy was NOT tested; enabled code paths do not establish successful live data.
- These are exposed development dates, NOT fresh blind holdouts. Overlapping
  holding windows are not independent trials. No subsequent tuning was performed
  to make this supplied outer replay look better.

### Candidate support and final inner checks

| Horizon | Fitted candidates | Passed final past-block gate | Candidates deleting all original six |
|---|---:|---:|---:|
| 5 | 88 | 5 | 69 |
| 20 | 74 | 8 | 48 |
| 60 | 3 | 0 | 3 |

There were 165 fitted candidates: 107 with one active score, 48 with two and 10
with three. Some scores are interactions and count multiple underlying inputs.
A gate pass is based solely on prior internal blocks, not on that outer case's
subsequent returns; it does not imply the subsequent trade was profitable.
No candidate was fitted for 135 cases due to insufficient/cohort-limited data.
Long-horizon nested validation is particularly constrained by three years of
history; repeated random cutoffs do not create additional independent history.

### Matched-date mean returns (not a compounded portfolio)

| Horizon | Strategy | Paired cases | Original control | Model | Difference (percentage points) |
|---|---|---:|---:|---:|---:|
| 5 | training_challenger_research | 86 | -0.468% | -0.316% | +0.152 |
| 5 | adaptive | 98 | -0.418% | -0.216% | +0.202 |
| 20 | training_challenger_research | 69 | +1.577% | +0.393% | -1.185 |
| 20 | adaptive | 96 | +2.079% | +1.172% | -0.907 |
| 60 | training_challenger_research | 3 | -10.628% | -8.067% | +2.562 |
| 60 | adaptive | 100 | +1.760% | +1.760% | +0.000 |

Research-candidate cases are only the subset with a fitted, observable candidate;
do not compare their mean with the original full 100-date mean. Adopted results
include original-control fallback when the final gate rejected the candidate.
No missing returns are filled with zero. Cash slots follow the predeclared entry
assumptions and are reported separately.

The adopted 5-session mean improved in this replay but remains negative. The
20-session mean deteriorated. The 60-session adopted result was unchanged.
This does NOT demonstrate an overall improvement, best weights, superiority to
0050 or readiness to trade. Results, including unfavorable ones, are preserved.

### Latest weights at 2026-10-15

- 5 sessions: research candidate `{'accumulation': 1.0}`; status `SPARSE_CANDIDATE_NOT_ADOPTED`.
- 20 sessions: research candidate `{'momentum_persistence': 1.0}`; status `SPARSE_CANDIDATE_NOT_ADOPTED`.
- 60 sessions: research candidate `{'liquidity_quality': 1.0}`; status `SPARSE_VALIDATION_COHORT_INCOMPLETE`.

All three latest adopted rankings remain the independent old control; sparse
research candidates are separately accessible in the UI. A candidate coefficient
of 100% means one ranking input, NOT investing 100% of capital in one stock.

## Untested or incomplete

- Streamlit Cloud/mobile browser and real-time quote endpoints.
- Live success rates for optional data downloads/account entitlements.
- Original financial publication and revision history. Lagged financial research
  is not PIT and is prohibited from authorizing capital allocation through that flag.
- Historical full-universe membership, delisted coverage, corporate-action
  completeness, official limit-up label series and intraday executable paths.
- Calibration of rise/limit-up probabilities, actual fills, investable capacity,
  transaction minimums, complete cashflow/dividend accounting and a compounded
  fully-invested portfolio curve.
- Global/exhaustive optimum. Search is bounded and does not test every possible
  model, factor transformation, sign, threshold or nonlinear interaction.

## Final package verification

- Final archive contains 99 root files, below the 100-file upload limit.
- Archive CRC validation and every non-manifest SHA256 entry: PASS.
- Extracted archive compilation / Python 3.11 grammar parsing: PASS.
- All 44 new tests rerun FROM the extracted package: 44 passed in 15.06 seconds.
  They are a repeat subset of the 261 tests, not 44 additional distinct cases.
- Source and extracted numerical files are byte-for-byte equal.
- After updating only this verification note, the final archive and manifest
  were rebuilt and CRC/hash/compilation checked again; no numerical source changed.

