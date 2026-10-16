# V19.2 verification status - 2026-10-16

## Code and input-report scope

Based on V19.1 complete 67-file delivery, not an unrelated rewrite.
The supplied V19.1 markdown was read as an aggregate research report. Its original
92-symbol price/evidence bundle was NOT attached; it was not reproduced here.
No optimal factor weights or real-market excess return is asserted.

## Executed checks

- Unmodified V19.1 baseline: 155 tests passed (120.95 seconds, single BLAS thread).
- V19.2 full regression before final additions: 177 passed (223.47 seconds).
- New V19.2 suite after four additional cases: 26 passed (48.87 seconds).
- Additional corrupt-checkpoint JSON shape cases: 3 passed.
- Final clean-package full suite: **184 tests passed**, no failed or skipped tests.
  Actual output is preserved in V19_TEST_OUTPUT.txt. No failing tests were deselected.
- Existing fixed-seed fixture explicitly pins the previous seed1900. The product
  date seed is1920 and stock-universe seed1900. Old version assertions now expect19.2.

## Complete 100-date flow check (synthetic)

Deterministic 100 synthetic equities plus a synthetic0050 reference, 750 business
sessions, 75,750 price rows; 100 distinct randomly sampled dates, 5/20/60-session
holding periods, 24 candidate-weight trials maximum per case.

Result: PASS. 300 cutoff/horizon fits, 6,000 factor/event diagnostic rows,
3,000 selected-trade rows and 1,500 strategy comparison rows were generated.
Elapsed compute399.93 seconds in this container; this is NOT a promise for
Streamlit Cloud speed or external API response times. Raw synthetic performance
reports and fake market data are deliberately NOT distributed with the app.
V192_SYNTHETIC_FLOW_CHECK.json records counts and explicit synthetic-only flags.

After that flow run, a small checkpoint loader shape guard was added and tested
separately (valid JSON lists/null/strings are ignored safely); scoring, selection,
sampling and outcome formulae did not change after the full flow check.
Reproduce the full flow from the released code with:

```sh
OPENBLAS_NUM_THREADS=1 python stress_v192.py --output data/v192_synthetic_test
```

## Test coverage, not an investment guarantee

100 unique/mature/date-seeded samples; no future outcome based sample replacement;
explicit insufficient-history status; independent stock/date seeds; no assumed
independence for overlapping holding windows; causal technical-event prefix tests;
missing optional factors distinct from zero; complete-pair Spearman; factor ablation;
SQLite integrity and safe CSV replay; no credentials in exported database;
provider retry budgets and rate-limit cooldowns; dataset entitlement isolation;
per-dataset evidence cache; no per-cutoff historical downloads; stock cache limits;
checkpoint hash invalidation/tamper/shape rejection; pause/resume; default100 UI
instead of old10 replay; original quote/entry safety gates retained.

UI tests use simulated Streamlit components, not an actual mobile browser or an
authenticated Streamlit Cloud production session. Initial numeric dataset copies,
local renderer speed and source connectivity are separate from these checks.

## Actual external API probe

FinMind, TWSE and Yahoo chart requests were attempted from the working container.
All three raised ConnectionError caused by DNS NameResolutionError. Each attempt
ended around5seconds. This does not establish that the providers are unavailable
from the user's deployment. Mock HTTP and recorded-parser checks passed, but a
real full online 100-date data run is NOT_TESTED in this container.

## Still unverified / not promised

- New 100-date real-market returns, outperformance and best factor weights.
- Complete historical delisted-stock membership and survivorship-free universe.
- Complete immutable release-time fundamentals, holder/broker data, actual fills.
- Official historical limit-up labels and historical live intraday reversal paths.
- Persistence across a host filesystem wipe, server hibernation or redeployment.

The default optional-data switch is OFF. Turn it ON for available revenue,
institutional and margin inputs. Quarterly quality / large-holder evidence still
requires appropriately timestamped input; absence remains NOT_TESTED.

100 dates can overlap heavily, especially at60sessions. The report also shows a
calendar-selected disjoint subset. Neither total sample count nor that subset
proves independence or universal investment performance.

## Reproduce local checks

```sh
pip install -r requirements-dev.txt
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 python -m pytest -q
python -m compileall -q .
```

See V192_README.md for online execution and the exported database/diagnostic bundle.

## Final packaging integrity

Full ZIP CRC check, SHA256 manifest, extraction and compile checks passed.
Applying the patch to the exact V19.1 67-file delivery produces the same files
as the V19.2 complete package, byte for byte. Legacy trading/quote modules and
V18.21 workbench remain unchanged. No live database, Secrets, cache directories,
synthetic market prices, or font files are included.
