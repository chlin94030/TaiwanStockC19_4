# V19.3 development protocol (frozen before expanded-factor replay)

Input: user-supplied v192_diagnostic_bundle.zip. All 100 exposed cutoff dates
are DEVELOPMENT REPLAY, not a fresh blind holdout. Do not optimize on their
outcomes or choose a flattering subset after observing performance.

1. First reproduce V19.2 legacy fixed weights on the raw attached price input.
2. Preserve the six-factor legacy reference and the transaction/price engine.
3. Add eight causal price/volume groups: trend efficiency, skip-five-session
   momentum persistence, money-flow accumulation (NOT institutional ownership),
   downside resilience, liquidity quality, orderly trend pullback, compression
   release, and relative resilience on down-market days.
4. Define horizon-specific expanded research priors before inspecting returns.
   They are hypotheses, not optimal weights. Correlated groups share a budget.
5. One candidate is selected using only matured pre-cutoff training outcomes;
   optional columns require actual timestamped evidence and training coverage.
   Cap correlated group weights and shrink noisy IC estimates. No factor can
   be promoted on the exposed outer replay's observed gains.
6. Preserve the existing seven-condition inner validation gate. A failed
   expanded candidate is still reported as a separate research strategy and
   is never silently called accepted, or converted into a buy signal.
7. Report legacy, expanded fixed, adaptive, guarded cash policy and 0050 on
   matched dates, including incomplete cases and non-overlap subset counts.
8. Export attempted candidate weights and returns even when adoption fails.
9. Additional earnings/value/ownership evidence is optional, not fabricated.
   Publication timing and source revisions remain explicit limitations.
10. Freeze this revision before collecting genuinely new forward outcomes.

Governance defaults are not tuned to maximize the supplied 100-date report.
No automatic orders. No calibrated limit-up probability is claimed.
