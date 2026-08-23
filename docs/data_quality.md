# Data Quality & Automation

## DQ Checks

The pipeline performs five automated data-quality checks:

1. Completeness
2. Uniqueness
3. Validity
4. Timeliness
5. Referential integrity

## Composite DQ Score

The composite score uses the following weights:

| Check | Weight |
|---|---:|
| Completeness | 25% |
| Uniqueness | 20% |
| Validity | 20% |
| Timeliness | 15% |
| Referential integrity | 20% |

The score ranges from 0 to 100.

### Threshold

- Score >= 90: PASS
- Score < 90: FAIL

## DQ History

Every DQ execution is stored in:

`dq_results_history`

This allows DQ performance to be trended over time.

## Scheduled Refresh

The refresh entry point is:

`Scripts/run_quality_check.ps1`

The script can be executed by Windows Task Scheduler.

The recommended schedule is daily.

## Failure Behaviour

The script returns exit code 0 when the DQ result is PASS.

If the DQ result is FAIL, the Python process returns exit code 1. The PowerShell wrapper detects the non-zero exit code, writes an error message, and exits with the same failure code.

This allows Windows Task Scheduler or another orchestration system to identify a failed refresh.

## Current Validation

A successful execution produced:

- Composite DQ score: 100.0
- Threshold: 90.0
- Status: PASS
- Total checks: 5
- Passed checks: 5
- Failed checks: 0