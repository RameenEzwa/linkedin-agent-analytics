# Part 5 — Advanced Analytics & Risk Modeling

## Objective

Detect abnormal LinkedIn outreach performance and identify hidden
risk signals that may require a reduction in daily outreach capacity.

## Statistical Method

The model uses standardized z-scores against historical daily metrics.

For a metric X:

z = (X - historical_mean) / historical_standard_deviation

Interpretation:

- |z| < 2: Normal
- 2 <= |z| < 3: Warning
- |z| >= 3: Anomaly

This method is suitable for monitoring changes in normally distributed
or approximately stable operational rates and provides an interpretable
measure of how unusual the current observation is relative to historical
performance.

## Risk Signals

### Acceptance-rate collapse

Acceptance rate is:

accepted invites / invites sent

A statistically significant negative deviation from the historical
acceptance-rate baseline increases risk.

### Reply decay

Reply rate is:

replies received / messages sent

A statistically significant negative deviation from the historical
reply-rate baseline increases risk.

### Ghosting

Ghosting is measured as the proportion of connected leads that have
not produced an expected downstream response within the defined
observation window.

An increasing ghosting rate contributes to risk.

### Throughput / Capacity Risk

Daily activity is compared with the account's permitted daily capacity.
Operating close to or above the applicable capacity ceiling increases
risk.

## Composite Risk Score

| Component | Weight |
|---|---:|
| Acceptance-rate anomaly | 30% |
| Reply-rate anomaly | 30% |
| Ghosting anomaly | 25% |
| Throughput/capacity risk | 15% |
| Total | 100% |

## Risk Thresholds

| Score | Classification |
|---:|---|
| < 60 | Normal |
| 60–74 | Warning |
| 75–89 | High Risk |
| >= 90 | Critical |

## Data Sufficiency

A minimum historical baseline is required before calculating statistical
anomalies.

The initial implementation requires at least 14 daily observations.

If insufficient history exists, the model reports that the statistical
baseline is unavailable rather than producing an unreliable anomaly
score.

## Capacity Recommendations

Capacity recommendations are based on observed historical outcomes and
the applicable account tier ceiling.

If risk is Normal, capacity may remain at the validated operating level.

If risk is Warning, capacity should be reviewed and may be reduced.

If risk is High Risk, a conservative reduction is recommended.

If risk is Critical, outreach should be paused pending investigation.

Final capacity recommendations must never exceed the applicable account
tier ceiling.

## Assumptions

- Historical daily observations are representative of normal operating
  behaviour.
- Rates are calculated using sufficient denominators.
- The historical baseline is reasonably stable.
- Activity timestamps accurately represent source events.
- The observation window for ghosting is consistently applied.

## Confidence

A z-score threshold of approximately 2 corresponds to a two-standard-
deviation warning boundary, while 3 standard deviations represents a
strong anomaly signal under an approximately normal distribution.

These thresholds are operational monitoring thresholds rather than proof
of causality.

## Known Limitations

The current database contains zero rows in fact_linkedin_activity and
only two source outreach records. Therefore acceptance-rate collapse,
reply decay, and ghosting cannot currently be estimated from observed
historical activity.

The model is implemented to become operational after sufficient
historical activity is loaded.

Small denominators can produce unstable rates, so anomaly calculations
should require minimum activity counts before interpreting rate changes.