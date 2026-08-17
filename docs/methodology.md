# Methodology

## Research objective

The project studies cross-sectional predictability in crypto returns across multiple horizons and asks whether a signal can survive realistic implementation.

The final architecture is a cross-sectional continuation strategy, but the research path also includes a statistically strong yet economically untradable reversal effect and an earlier momentum specification that failed out of sample.

## Data source

The research uses Binance spot USDT market data.

Public GitHub artifacts intentionally exclude raw and processed exchange bars. The repository contains only small universe metadata, frozen result tables, protocol files, and curated figures.

## Point-in-time universe

The research universe is a monthly top-25 set of liquid Binance spot USDT pairs.

Key properties of the frozen universe:

- 76 monthly snapshots;
- exactly 25 assets per month;
- 151 unique symbols across the research union.

Membership is determined point in time rather than from a single end-of-sample asset list.

This is designed to reduce survivorship bias.

## Time handling

The project uses explicit UTC timestamps.

The original research used 4h bars for the initial cycle. After the first frozen validation failed, the redesign used true native 1h Binance data through 2024 only.

Formation horizon, holding horizon, and decision cadence are treated as separate research dimensions.

## Return construction

Past and forward returns are based on exact elapsed-price endpoints.

The research does not forward-fill returns or prices across missing exchange timestamps in order to fabricate valid observations.

Portfolio weights are formed using information available at the decision timestamp and earn only subsequent returns.

## Signal conventions

### Reversal

Short-horizon reversal is represented as the negative of a recent cross-sectional return signal.

It showed strong and persistent IC but failed implementation economics because of turnover.

### Continuation

Continuation ranks assets by prior relative performance and takes a long-short cross-sectional spread.

The final continuation architecture uses overlapping multi-week holdings and different implementation cadences.

## Portfolio mappings

Two mappings are used in the final research:

### Continuous rank

Assets receive cross-sectional rank scores centered around zero and scaled into a dollar-neutral long-short portfolio.

### Equal-weight terciles

The highest-ranked group is held long and the lowest-ranked group short with equal-weight allocation inside each side.

Both mappings are normalized so that gross exposure is controlled and net exposure is approximately zero.

## Turnover

Turnover is measured as full-L1 target-weight change:

\[
TO_t = \sum_i |w_{i,t} - w_{i,t-1}|
\]

This is intentionally more conservative than half-turnover conventions sometimes used in long-short research.

## Transaction costs

The primary cost assumption is:

\[
20 \text{ bps} \times TO_t
\]

Net return is therefore:

\[
r^{net}_t = r^{gross}_t - c \cdot TO_t
\]

where \(c = 0.002\) for the primary 20-bps scenario.

Additional 0 / 7 / 40-bps scenarios are used only for sensitivity analysis.

Break-even execution cost is defined as the cost per unit of turnover that reduces arithmetic mean return to zero.

## Validation chronology

The research uses three broad chronological stages.

### Development / training

Initial signal research and portfolio design use the early sample.

### Frozen validation

The original Cycle-A momentum architecture is evaluated on 2023–2024 after being frozen.

It fails.

### Untouched final holdout

After the failure is diagnosed and a new continuation architecture is developed using pre-2025 data only, the final test uses:

**2025-01-01 through 2026-08-01 exclusive**

The final holdout is opened only after exact finalist definitions and the survival rule are frozen.

## Final survival rule

A finalist passes if all three conditions hold in the untouched final holdout:

1. mean continuation IC > 0;
2. gross annualized mean return > 0;
3. break-even execution cost ≥ 20 bps.

There is no required Sharpe threshold and no required HAC significance threshold in the primary survival rule.

## Dependence-aware inference

Cross-sectional IC series can be serially dependent because signals and holdings overlap through time.

The project therefore reports HAC/Newey-West mean t-statistics where appropriate.

For the final finalists, the overlap-aware lag is based on holding horizon relative to decision cadence.

## Parameter selection philosophy

The project avoids choosing a single isolated parameter cell solely because it has the maximum backtest metric.

Instead, parameter surfaces are interpreted structurally:

- neighboring formation horizons;
- neighboring holding horizons;
- neighboring cadences;
- performance-versus-turnover tradeoffs;
- development versus later pre-2025 evaluation consistency.

The final ECON, BAL, and SHARP variants represent different implementation philosophies within a broad continuation region.

## Failure preservation

Negative results are part of the final package.

In particular:

- short-horizon reversal is statistically strong but economically unattractive;
- the original 3d → 1w momentum architecture fails frozen validation;
- the final continuation effect degrades materially versus pre-2025 evidence.

These results are not removed from the narrative.

## Post-validation diagnostics

After the final holdout, the project characterizes:

- execution-cost sensitivity;
- drawdown and tail behavior;
- monthly time breadth;
- realized BTC and crypto-market exposure;
- portfolio breadth;
- asset-level concentration;
- long/short attribution.

These diagnostics do not trigger any strategy redesign.

## Known modeling limitations

The backtest represents a theoretical long-short portfolio using spot-market information.

It does not fully model:

- borrow availability;
- perpetual-futures funding;
- margin constraints;
- venue-specific fees;
- market impact;
- nonlinear execution cost;
- asset-specific spread dynamics;
- live latency.

The constant 20-bps model is therefore a simplifying implementation assumption, not a claim about exact realizable trading costs.
