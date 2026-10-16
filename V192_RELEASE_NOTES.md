# V19.2 release scope

Base: V19.1 complete 67-file package.

## Report-driven diagnosis

The supplied latest report had 10 exposed dates, 92 symbols including the reference,
and 30 horizon fits. Every fit retained prior weights: stability was unproven in
19 cases, disjoint blocks were insufficient in 5, validation cohorts incomplete
in 5 and training cohorts incomplete in 1. Optional factors had zero coverage.
The fixed/adaptive means were identical; these are not proof that optional factors
are ineffective or that changing a weight arbitrarily would improve returns.

## Changes

- Default 100 uniform random, unique, mature cutoffs; explicit stratified/replay modes.
- Independent seeds for stock universe versus sampled dates; stable cutoff-based fit seeds.
- Online price range downloads independent of number of cutoffs; persistent exact-range
  caches, dataset-level optional caches, monthly fallback cache and bounded retry logic.
- Rate-limit cooldowns survive worker restarts; dataset entitlement failures do not
  unnecessarily disable unrelated datasets. No rate-limit or access-control bypass.
- Exportable SQLite history database and credential-free CSV replay archive.
- Atomic cutoff/horizon JSON checkpoints with price/evidence/settings/code fingerprints.
  Pause/resume in Streamlit; automatic reuse in CLI. Cache-only stock limits respected.
- Six diagnostic technical events plus fourteen existing factor groups; coverage,
  complete-pair rank IC, quintile/event contrasts and same-date factor-removal comparisons.
- Separate disjoint-calendar diagnostic subsets; explicit lack of independence and
  multiple-testing/missing-data caveats. No future audit result feeds its own fit.
- In-memory reuse of causal date groups and training IC diagnostics.
- New UI fields, fixed default old-ten-date toggle, portable-database download,
  100-date/full-factor diagnostic downloads and compact progress presentation.
- Existing live quote safety, investment horizon conventions, cost assumptions,
  reference/cash comparisons and prior-weight acceptance gates retained.

## Not included / not established

No new original disclosure ledger, historical delisted universe, complete financial
statement or holder database, verified intraday path, actual order fill, official
limit-up label series, proven best factor weights, or guarantee of profit.
Provider API reachability still depends on the deployment environment. See QA.
