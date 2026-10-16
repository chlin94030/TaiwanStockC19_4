# Alpha Radar V19.4 | 先選因子，再估權重

## 三步驟開始

1. 解壓縮後將全部檔案放到 GitHub 專案根目錄。保留 data/ 與 Secrets，不要只替換 app.py。
2. Streamlit 啟動檔為 app.py。確認版本顯示 V19.4，先使用既有快取驗證，或線上下載歷史資料。
3. 選擇 5 / 20 / 60 交易日，查看「稀疏模型研究排名」與「留下哪些因子？刪除哪些？」。

**研究候選不等於已通過採用，排名權重不是資金配置比例。**

原因子可以真正刪除，不會被權重縮減加回。原模型獨立保留為對照組；候選未通過門檻時，採用排名可能仍與原模型相同，但新候選仍可獨立查看。

基本面與籌碼必須有實際資料才能參與選擇。未知公告時點的季報，預設只快取不計分。不是所有支援欄位都已有歷史驗證結果。

## Release identity and scope

This is the ONE V19.4 sparse-factor release. It is based only on the last V19.3
91-file build (SHA256 39bed061be3ddfd409f1aab40e88855e3d6c4ba382c2f18fc27902c382587844),
not the other 93-file archive that previously used the V19.3 name.

The full archive is self-contained code; it does not contain your credentials,
private cache, fabricated financial records or an alleged best weight vector.
Old numerical engines remain available for control comparisons. Old research/QA
markdown files are versioned historical records, not this release's acceptance.
Read V194_QA_STATUS.md for what was actually tested in this release.

## Install

```bash
python -m venv .venv
# Linux/macOS: source .venv/bin/activate
# Windows: .venv\Scripts\activate
python -m pip install -r requirements.txt
streamlit run app.py
```

The source is syntax-checked for Python 3.11+ and executed here using Python 3.13.
Streamlit deployment entrypoint remains app.py. Upload extracted files, not the
ZIP itself. Back up your repository, retain data/ and Streamlit Secrets, and
replace all same-name source files. The sparse engine is NOT an app.py-only fix.

Optional FinMind token: set FINMIND_TOKEN in environment or Streamlit Secrets.
No token is included. Actual endpoint reachability, authorization and per-account
rate limits depend on your deployed environment. Request budgets do not bypass
provider limits. A failed download retains usable caches with source status.

## What changes mathematically

1. Each 5/20/60-session model independently selects candidate inputs based on
   data available before its cutoff. No technical/fundamental/ownership family
   has a mandatory weight allocation.
2. All original factors may be dropped. A candidate's exact support mask is
   preserved through coefficient fitting, within-support shrinkage, ranking,
   exports and UI. The old six-factor model is an independent control, NOT a
   mandatory 50% part of every challenger.
3. Singleton controls, promising pairs, forward additions, backward removals and
   swaps are explored. Default search budget is at most 160 subsets per cutoff
   and horizon, with at most 6 underlying factor inputs. An interaction counts
   as its two parents. This is BOUNDED greedy/beam exploration, not enumeration
   of all combinations or proof of a global optimum.
4. Nonnegative ridge coefficients use within-date centered factor values and
   within-date ranks of completed future net returns, fitted on past data only.
   Rank targets reduce raw-return outlier influence. Selected positive weights
   are normalized then shrunk toward equal weighting ONLY on their own support.
   Negative information is not opportunistically inverted after seeing a test.
5. Candidate support selection uses three expanding, purged chronological CV
   folds inside development data. Label end dates must precede the next scoring
   stage. Actual return evaluation keeps selected missing outcomes missing;
   unavailable selected stocks are not replaced after seeing outcomes.
6. The candidate score uses excess to an equal blend of 0050 and the available
   research-universe equal-weight control, adverse excursion, dispersion and
   number of active underlying inputs. It does not penalize distance from old
   weights. Within the configured near-best tolerance, prefer fewer inputs.
7. Only one chosen/refitted candidate proceeds to the final disjoint past-block
   adoption test. A failure does not lead to trying another candidate on those
   same final blocks. The old stability/risk/cost gates remain, with an additional
   requirement to beat the same-pool equal-weight reference on average.
8. Ranking a candidate is distinct from adopting it, investing in it, or holding
   cash. All these outcomes are reported separately. No trading orders are placed.

Cohort limitations are explicit: coefficients use complete candidate-input rows
within the fitting fold; eligibility first requires at least 85% training coverage.
This can constrain optional-factor studies with uneven coverage. Validation dates
are fixed by reference completeness, not selected for a contender's good returns.
Each contender must be complete on the fixed CV scoring cohort. This is not a
solution to historical membership, missing-not-at-random data or revisions.

Default numerical settings are hypotheses/governance limits, not proven optima:
max inputs 6, subsets 160, beam 3, CV folds 3, ridge .02, within-support learned
weight .5, correlation exclusion .95, per-input objective penalty .0005,
near-best tolerance .001. Original risk/liquidity/overheat rules remain explicit
strategy assumptions, not learned factors. Changing them requires new validation.

## Candidate library (34 columns, NOT 34 independent signals)

- Legacy technical groups: trend, relative_strength, breakout, reversal,
  pattern, volume.
- Extended technical groups: trend_efficiency, momentum_persistence,
  accumulation, downside_resilience, liquidity_quality, orderly_pullback,
  squeeze_release, market_resilience.
- Separately selectable atomic signals: kd_turn, rsi_rebound, macd_turn,
  bias_repair. A composite reversal group and its components cannot both count.
- Optional groups: revenue, quality, foreign, trust, joint, dealer, margin,
  holders. These need actual data, not inferred "smart money" from prices.
- Additional business inputs: earnings_growth, gross_profit_quality,
  earnings_yield, cash_conversion, balance_safety.
- Three predeclared interactions: growth_pullback_pair, flow_breakout_pair,
  rebound_accumulation_pair. They require both parents and cannot double-count
  their parent features in the same support.

Missing selected inputs exclude a stock from sparse ranking. They are never
filled with zero/50 or silently reweighted across that stock's remaining inputs.
The old control retains its original coverage rule for reproducibility.
KD/MACD/RSI/W signals and earnings growth are observations, not calibrated
probabilities of tomorrow's rise, limit-up, future earnings or analyst estimates.
Gross-margin/valuation comparability across industries is not automatically
neutralized; financial-sector ratios require particularly careful interpretation.

## Optional financial and ownership data

The original monthly revenue, institutional buys/sells and margin-balance
pipelines are preserved. V19.4 also requests:

- TaiwanStockFinancialStatements
- TaiwanStockBalanceSheet
- TaiwanStockCashFlowsStatement
- TaiwanStockPER

Raw API payloads are cached separately. Missing permissions or a single failed
dataset do not cause invented values or silently disable every other dataset.
A fresh 100-stock run requesting all optional datasets can exceed the default
per-run budget; resume the same download settings to reuse completed caches.

IMPORTANT: a financial-statement date is a period-end date, not its publication
moment. Default `disclosure_required` excludes statements without a supplied
publication/availability timestamp, while retaining raw cache for later review.

The explicitly opt-in `lagged_research` scenario assumes availability 120 calendar
days after period end. It is labeled NOT_PIT, may be wrong for late/restated filings,
and does not authorize capital allocation based on that assumption. Current vendor
snapshots do not prove originally published, unrevised historical financial data.
Even vendor-provided publication dates are not an original revision ledger.

EPS YoY uses a positive prior-year EPS denominator. Negative-base turnarounds are
not invented as ordinary percentage growth. TTM requires four consecutive quarters.
Cash conversion currently uses annual Q4 cash flow versus four-quarter income;
YTD cash flow is not mixed with single-quarter profit. Missing source items stay
missing. The accounting meanings must match the provider schema.

Imported evidence: copy the HEADER-ONLY optional_evidence_template.csv, add your
real sourced records, and use the UI uploader or put optional_evidence.csv under
data/v19. Required: ticker (e.g. 2330.TW), available_at, source. Other fields are
optional; timing should identify publication evidence or an explicit assumption.
Dates without timezone are interpreted in the app's Taipei decision convention.
Use one row per observation/source/release; do not paste today's value on old dates.
An import updates research input, not your original uploaded files. It is merged
for cache validation and online download+validation when optional_data is enabled.

Holder_change is the change in large-holder ownership percentage points, not a
broker-branch identity. Dealer flow excludes hedge trades. No complete historical
large-holder or branch database is fabricated or required by default.

## UI workflow

The primary pages remain selection/planning, historical validation and individual
stock diagnosis. Original V18.21 workspace remains an explicitly labeled sidebar
option for compatibility, not a second claim of validated new weights.

1. Choose 1-3 years, stock count, 100 seeded cutoff dates, factor-count limit and
   search budget. Stock and cutoff sampling use separate seeds.
2. With downloaded data already cached, use cache-only validation. Otherwise
   download online. Price history is downloaded once, not 100 times for 100 dates.
3. In selection, choose the sparse research candidate, adopted ranking or original
   control. If no compatible trained candidate exists, the UI says so and displays
   an explicitly labeled control. It does not invent current best weights.
4. Inspect the included/excluded table: factor, coefficient, training coverage,
   not selected/disabled/missing status. Coefficients are ranking weights, not
   portfolio allocations or hit probabilities.
5. On validation, compare original control, training-selected candidate, adopted
   result, cash policy, 0050 and pool equal weight on matched dates/bases. Averages
   of overlapping cases are not a compounded capital curve or independent trials.
6. On stock diagnosis, historical bars and today's quote remain separate. Quote
   failures remain explicit. A daily rebound is not proof of live black-to-red
   prediction. Reference prices are not executable orders.

Changes to factor-count limits, search settings, costs or evidence timing do not
silently reuse an incompatible previous weight fit. Imported evidence requires a
new validation run. Existing data/ is retained; stale checkpoints are invalidated
by source/evidence/settings/numerical-code fingerprints, not blindly reused.

## Command-line examples

Online, optional data enabled (actual account limits still apply):

```bash
python run_v19.py --years 3 --stocks 100 --dates 100 --optional-data --request-budget 1000 --max-factors 6 --search-budget 160 --data data/v19 --output data/v19/cli_report
```

Cache only:

```bash
python run_v19.py --cache-only --years 3 --stocks 100 --dates 100 --optional-data --data data/v19 --output data/v19/cli_report
```

Exact user-price development replay used for this release (no optional evidence
was present in this bundle; do not claim fundamental effectiveness from it):

```bash
python run_v19.py --replay-bundle v192_diagnostic_bundle.zip --as-of 2026-10-15 --dates 100 --seed 1920 --max-factors 6 --search-budget 160 --data data/replay_v194 --output results_v194
```

Reference-only old engines remain accessible through --factor-design legacy_v192
or --factor-design expanded_v193. V19.4 default is sparse_v194. `--trials 24` is the
legacy search knob; sparse search uses `--search-budget`, so they are not equivalent.

## Output / reproducibility

- v19_validation.md, comparison.csv: research results, missing-case reasons,
  source/price-coordinate caveats, sample and overlap counts.
- selected_trades.csv: selected names and assumed next-session entries/exits.
- sparse_factor_selection.csv: every cutoff/horizon and explicit zero/nonzero
  candidate and adopted coefficients, coverage, exclusions and adoption status.
- sparse_latest_weights.csv: latest 5/20/60-session candidate versus adopted weights.
- sparse_selection_summary.csv: selection frequencies, not hit probabilities.
- sparse_protocol.json: settings and selection/timing limits.
- fit_traces.json: bounded search candidates, fold scores, final gate evidence.
- v194_diagnostic_bundle.zip: compatible full replay inputs, results and diagnostics.

The familiar older diagnostic filenames are also exported for compatibility;
the V19.4 download is canonical. ZIP readers do not execute pickle or bundled code.
Secrets/tokens are not put into research exports.

## Testing

```bash
python -m pip install -r requirements-dev.txt
python -m pytest -q --disable-warnings
```

Engineering tests use synthetic data, mocked HTTP and a Streamlit test double.
They are not brokerage executions. The separately supplied replay result uses
user-provided price history, not artificial market returns. Inspect V194_QA_STATUS.md
for final counts, findings, performance scope and untested external endpoints.

## Investment and research limits

This release implements a better-defined research process, not a proven optimal
investment strategy. The supplied 100 dates were already seen in development;
a new seed does not make overlapping history a new blind test. Price history is
user-supplied/provider history, not independently exchange-verified per bar.
Historical delisted membership, publication revisions, intraday order paths,
official limit-up prices, investable capacity and portfolio cashflows remain
incomplete. Entry/exit cost and slippage assumptions are in Settings, not actual
fills. A stop/reference-risk estimate cannot guarantee maximum loss on gaps.
No autonomous order execution, investment suitability assessment or guaranteed
profit is provided. Use fresh precommitted data for the next independent test.
