# Research History

This document preserves the intellectual path of the project, including the failed hypotheses and the redesign that followed.

The public notebooks are deliberately organized by research logic rather than by the original internal step numbers. This file records the historical sequence so that the final repository does not erase how the conclusions were reached.

## 1. Initial research question

The project began with a broad cross-sectional question:

> Does relative past crypto performance predict relative future performance, and can any such relationship survive realistic portfolio implementation?

The initial research universe was a point-in-time monthly top-25 set of liquid Binance spot USDT pairs. The first empirical work used 4h decision bars and examined both reversal and momentum across formation and forward horizons.

## 2. Initial horizon research

The original horizon surface showed two notable regions:

- strong very-short-horizon reversal;
- weaker medium-horizon momentum.

The representative initial candidates were:

- 4h formation → 4h forward reversal;
- 3d formation → 1w forward momentum.

The research then studied signal decay, timing, and abnormal trading activity.

### Activity result

Higher abnormal quote/trade activity weakened short-horizon reversal. A quote-activity-conditioned reversal signal was therefore promoted alongside the baseline reversal.

For medium-horizon momentum, the activity interaction was unstable through time and was not promoted.

## 3. First frozen candidate set

Four Cycle-A candidates were frozen before portfolio construction:

1. baseline reversal;
2. activity-conditioned reversal;
3. immediate 3d momentum;
4. 1d-delayed 3d momentum.

Portfolio construction used neutral long-short weights, explicit formation-to-holding timing, and full-L1 turnover.

## 4. Implementation economics

The first major negative result appeared before out-of-sample validation.

Short-horizon reversal was statistically strong but generated extremely high turnover. Even after slowing refresh cadence, its realized break-even execution cost remained far below the primary 20-bps assumption.

The reversal family was therefore rejected on economic grounds.

The two momentum candidates retained acceptable in-sample implementation economics and advanced to frozen 2023–2024 validation.

## 5. Frozen 2023–2024 validation failure

The original momentum architecture failed.

Both immediate and delayed momentum produced negative net-20 returns and negative net-20 Sharpe in the validation sample:

| Candidate | Net-20 Sharpe | Break-even cost |
|---|---:|---:|
| Immediate momentum | -0.98 | 2.21 bps |
| Delayed momentum | -1.32 | -1.59 bps |

The predeclared validation decision was:

**VALIDATION_FAILURE**

This failure is intentionally preserved in the public repository. It is not hidden by the later redesign.

## 6. Post-failure diagnosis

Only after the validation failure was accepted did the research reopen the modeling question.

The redesign used true native 1h Binance data through 2024 only and kept the 2025+ sample untouched.

The main diagnostic findings were:

- the old 3d → 1w momentum relationship was positive in 2020–2022 but negative in 2023–2024;
- very-short reversal retained its statistical sign but remained economically unattractive;
- a distinct continuation region appeared when formation, holding, and implementation cadence were separated.

The redesign explicitly distinguished:

- formation horizon;
- holding horizon;
- decision cadence.

Market-trend, volatility, dispersion, and abnormal-activity state diagnostics were also explored. No state filter was robust enough to promote.

## 7. Independent reversal and continuation replay

Reversal and continuation were tested as separate sleeves under chronological pre-2025 replay.

### Reversal

Reversal sign persistence was extremely strong, but turnover remained fatal. No fixed reversal implementation survived the combined sign, economic, and 20-bps criteria across replay years.

### Continuation

The initial continuation grid also failed the strict replay gate, but the failure surface contained a useful structural clue: economics improved toward the longest tested holding horizon.

That boundary behavior justified extending continuation holding length, not rescuing reversal.

## 8. Continuation horizon extension

The continuation research was extended into overlapping multi-week holdings and then into a broader formation × holding × cadence grid.

The resulting pre-2025 surface showed a broad interior region rather than a single isolated optimum:

- formation broadly viable from roughly 1d through 2w;
- 6w–8w holding horizons economically central;
- slower cadences often improved cost efficiency;
- 3m formation failed clearly.

This supported a distinct multi-week continuation architecture.

## 9. Pre-2025 finalist freeze

Three exact implementations were frozen before opening the final holdout:

| Finalist | Philosophy | Mapping | Formation | Holding | Cadence |
|---|---|---|---:|---:|---:|
| ECON | Economic resilience | Continuous rank | 2w | 6w | 24h |
| BAL | Balanced | Equal-weight terciles | 3d | 8w | 48h |
| SHARP | Higher Sharpe | Equal-weight terciles | 1d | 8w | 8h |

These were chosen to represent different implementation philosophies within a broad continuation region, not because they were hindsight-selected from 2025+ performance.

## 10. Untouched final holdout

The final holdout was 2025-01-01 through 2026-08-01 exclusive.

Before opening it, the project froze:

- finalist definitions;
- 20-bps primary cost;
- the survival rule;
- dependence-aware IC inference;
- a no-retuning / no-combination protocol.

All three finalists passed the primary survival rule:

- positive continuation direction;
- positive gross annualized return;
- break-even execution cost at least 20 bps.

Headline holdout results:

| Finalist | Mean IC | Gross Sharpe | Net-20 Sharpe | Break-even |
|---|---:|---:|---:|---:|
| ECON | 0.0484 | 0.33 | 0.10 | 28.5 bps |
| BAL | 0.0466 | 0.79 | 0.41 | 42.0 bps |
| SHARP | 0.0368 | 1.13 | 0.42 | 31.7 bps |

The correct conclusion is **3/3 implementation-level survival of one continuation architecture**, not three independent alphas.

## 11. Post-validation diagnostics

The final risk and robustness stage did not alter the strategy.

It found:

- materially weaker economics than pre-2025 evaluation;
- meaningful drawdowns;
- stronger performance in 2025 than Jan–Jul 2026;
- negative realized beta to BTC and a point-in-time crypto-market factor;
- broad implementation with roughly 29–31 active names;
- low single-name concentration;
- high correlation across the three finalists.

No post-holdout beta hedge, asset exclusion, leg redesign, ensemble fit, or winner selection was performed.

## Final research state

Empirical research is complete and frozen.

The repository may reorganize code, improve documentation, and regenerate figures, but it may not change the substantive empirical conclusions.
