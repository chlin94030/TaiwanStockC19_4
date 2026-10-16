# Alpha Radar V19.2 - online history and 100-date factor validation

This release changes the validation workflow, not a proven optimal investment model.
It is based on the supplied V19.1 report. The fixed/adaptive results were the same,
all 30 fits retained baseline weights, and optional-factor coverage was zero.
Those observations do not establish that revenue or institutional factors are useless.

## Install

Extract the FULL package into the repository root. Streamlit entry point remains
`app.py`. Preserve `data/`, existing databases and Streamlit Secrets. Do not upload
only the ZIP itself, and do not overwrite a newer/custom project with the patch.
The patch is for the exact previously delivered V19.1 67-file package only.

```sh
pip install -r requirements.txt
streamlit run app.py
```

## Browser workflow

The sidebar now defaults to 3 years, a target pool of 100 stocks, **100 unique
random cutoff dates**, and 5/20/60 trading-day holding periods. The stock count
and cutoff count are different controls. The old 10-date replay is OFF by default.

1. Select the historical interval and a completed-day cutoff.
2. Choose the button for online download plus validation. Existing exact-range
   caches are reused. There is also a download-only button and a cache-only button.
3. Open the historical-validation page. It shows requested/available/drawn dates,
   completed cases, performance on identical dates, factor coverage, rank IC and
   leave-one-factor-out differences.
4. Download the historical database and the full diagnostic bundle.

The date seed defaults to 1920. The independent stock-pool seed remains 1900.
Changing the date seed does not also change the stock pool. Sampling is uniformly
without replacement by default; stratified sampling is available. Dates are then
processed in chronological order. The date list and eligible-pool hash are saved
BEFORE outcomes are examined. Missing outcomes are not replaced with more lucky dates.

If there are fewer than 100 eligible dates with 60 future common trading sessions,
the run reports INSUFFICIENT_HISTORY and actual count zero; it does not claim a
10-date or repeated-date result to be a 100-date validation. A recent IPO or a
short dataset can reduce coverage. The download may contain fewer than 100 equities;
the actual count is shown and no failed symbol is silently replaced after observing returns.

## Command-line workflow

```sh
# Online download, then 100 random dates; resumable case checkpoints are ON.
python run_v19.py --years 3 --stocks 100 --dates 100 --horizons 5,20,60 --seed 1920

# Only download and export a portable historical database.
python run_v19.py --years 3 --stocks 100 --dates 100 --download-only

# No further HTTP requests; reuse the downloaded database/cache.
python run_v19.py --cache-only --years 3 --stocks 100 --dates 100 --seed 1920

# Add available revenue, institutional-flow and margin history.
python run_v19.py --years 3 --stocks 100 --dates 100 --optional-data --request-budget 600

# Reproduce a fixed period; specify the SAME settings as the original run.
python run_v19.py --cache-only --as-of 2026-10-15 --years 3 --stocks 100 --dates 100 --seed 1920

# Import the exported database ZIP/diagnostic ZIP using its CSV replay inputs.
python run_v19.py --replay-bundle YOUR_DATABASE.zip --as-of 2026-10-15 --years 3 --dates 100

# Explicitly replay the already-exposed ten dates (not a 100-date test).
python run_v19.py --cache-only --dates 10 --reference-report reference_validation_v191.md
```

Advanced: `--sampling stratified`, `--universe-seed 1900`, `--fresh-run` (ignore
case checkpoints), `--refresh-history` (force a provider refresh), `--raw-first`,
`--no-factor-audit` (performance-only research), `--tickers 2330.TW,2317.TW,...`.
Use a separate `--data` / `--output` directory to preserve an alternate experiment.
The as-of date is frozen before the CLI or app worker begins.

## What is actually downloaded

- One requested daily-history interval per symbol from the existing Yahoo chart /
  FinMind provider chain, with bounded TWSE monthly raw fallback for the benchmark
  and a small number of symbols. There is no per-cutoff HTTP loop.
- Date, OHLC, physical share volume, adjusted close if available, ticker and source.
- Optional revenue and institutional/margin datasets are cached independently.
  Successfully downloaded optional datasets are not needlessly repeated after a
  different dataset fails. Missing optional data never becomes a zero value.
- `data/v19/history.sqlite` has `prices`, `evidence`, and `metadata` tables.
  `data/v19/v192_history_database.zip` contains SQLite, compressed CSV replay inputs,
  source metadata and the SQLite checksum. It does not contain API credentials.

The current provider universe is NOT verified historical exchange membership.
Survivorship bias remains. Yahoo is a third-party reference source; FinMind and
TWSE access/entitlements/rate limits are not bypassed. A failed source does not
prove that no trading occurred. A cache refresh is not the same as a live quote.

### Optional factors and API budgets

The optional toggle is OFF by default for a fast price-only baseline. It must be
turned ON to test downloaded revenue/foreign/trust/joint/dealer/margin factors.
Quarterly earnings-quality and large-holder factors still require timestamped
`data/v19/optional_evidence.csv` inputs; they are not automatically fabricated.
Required columns: `ticker`, `available_at`, `source`; usable value columns include
`revenue_yoy`, `eps_growth`, `eps_ttm`, `gross_margin`, `foreign_net`, `trust_net`,
`dealer_net`, `margin_balance`, `holder_change`. Values must be historically
available at the stated time; today's data cannot be backfilled into past dates.
Vendor revenue release dates plus a conservative lag are still a timing proxy,
not an original immutable disclosure ledger.

FinMind's documentation describes hourly request limits. The app conservatively
keeps local rolling-hour budgets (280 without a token; 560 with a token). A 600-call
job setting does NOT bypass that hourly budget. Optional data across 100 stocks
may require another quota window. Configure `FINMIND_TOKEN` in environment or
Streamlit Secrets, never in source files. Entitlement errors are isolated by
dataset; invalid credentials and rate limits block the provider. Transient network
or server errors get at most one retry by default, with all calls budgeted.

## Resume and reproducibility

Per-symbol files are written as downloads finish. An exact requested range is
reused across app restarts until force-refresh is selected. For adjusted histories,
a changed requested interval fetches a consistent series rather than stitching
new adjusted prices into an old provider coordinate.

Each completed cutoff/horizon has an atomic JSON checkpoint under
`data/v19/checkpoints/`. The key includes price contents, optional evidence contents,
settings, version and numerical-code hashes. A changed dataset, date, seed or code
invalidates reuse. Bad/incomplete checkpoint hashes are ignored. No pickle is loaded.

Pause stops the app-owned worker at a safe boundary. If downloads were interrupted,
press online download plus validation again: per-symbol and per-dataset caches are
reused. After downloads have finished, resume the computation with the SAME settings
and data by pressing the cache-only validation button. Do not change the cutoff date
mid-resume. Previously successful reports remain available if a new run fails.
An active server can continue when a phone disconnects; platform hibernation,
container replacement or disk deletion can interrupt it. Export the database and
results or use persistent storage when long-term retention is needed.

## Understanding the factor report

`factor_validation_cases.csv` contains each sampled date/horizon/factor; the summary
contains 14 factor groups plus 6 binary event diagnostics for each of 3 horizons.
The 6 events are low-zone KD cross, MACD histogram flip, RSI oversold recovery,
negative-bias repair, W neckline breakout/retest, and volume-supported breakout.
Binary events have no separately assigned model weight, so their ablation cells are empty.

- Coverage: how much eligible signal-date data actually exists.
- Rank IC: pairwise Spearman rank association between factor scores and later
  executable-policy net returns. Positive is directional association, not a win rate.
- High-minus-low: the top/bottom quintiles, or signal-on/off groups for binary events.
  Constituents are selected before checking their future prices. Missing selected
  outcomes invalidate that comparison rather than dropping a possible losing stock.
- Full-minus-removed: full model return minus return after removing one active
  factor and renormalizing remaining weights. Positive favors retaining the factor
  on these samples. This includes rank, coverage and risk-penalty interactions and
  is not proof of a causal effect.
- Disjoint subset: a calendar-selected set of non-overlapping holding windows.
  Results are separately shown; even those cases can remain correlated by regime.

All returns in CSV/JSON are decimal fractions (`0.02` means 2%). IC is not a
percentage. Zero coverage means NOT TESTED, not ineffective. Constant signals and
incomplete outcome pairs are explicitly excluded from IC denominators. The audit
is descriptive and subject to multiple-testing and missing-data bias; no p-values
or optimal-factor claims are invented.

## Weight design and validation discipline

The 100 sampled dates are development evaluation points, NOT 100 independent
trials. A 60-session horizon overlaps heavily within 1-3 years. Increasing the
number of draws does not create more historical training or independent long-horizon blocks.

Before each cutoff, only already-mature outcomes are available to fit weights.
The existing baseline-shrinkage, disjoint inner validation, benchmark, fill and
risk gates remain. The factor audit never uses the same date's future result to
change its selected weights. The latest research fit can use information that
has since matured, but it does not rewrite historical test records.

The supplied V19.1 report did not justify a particular new KD/MACD/fundamental
weight. This release therefore expands evidence collection rather than manually
forcing a winner. A gate rejection means the prior stays in place, not a frozen UI.
Future evaluation after reading these results needs a separately frozen protocol;
changing seeds repeatedly until the result looks good is not new blind evidence.

## Output files

- `v19_validation.md`: whole-run results, counts, source gaps and factor summary.
- `factor_validation.md`, `factor_validation_summary.csv`, `factor_validation_cases.csv`.
- `sampling_plan.json`: exact sampled dates, seed, candidate-pool hash and disjoint counts.
- `comparison.csv`, `selected_trades.csv`: all strategy cases and individual assumed trades.
- `fit_traces.json`, `weights_candidate.json`, `case_diagnostics.csv`, `source_gap_ledger.csv`.
- `v192_diagnostic_bundle.zip`: results plus prices, evidence and metadata for exact replay.
  The older `v191_diagnostic_bundle.zip` alias remains for compatibility.

## Test versus investment performance

Run `pip install -r requirements-dev.txt` and `python -m pytest -q` for local tests.
The tests include synthetic data, replay, missing-data, cache, budget and UI-contract
checks. They do not establish live-provider availability or real-market outperformance.
Do not use synthetic test output as an investment result. See the release QA file
for exactly which checks ran in the delivery environment.
