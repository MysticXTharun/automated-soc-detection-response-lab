\# Detection 014 - Automated SOC Metrics and Analytics

\## Overview

Detection 014 adds automated SOC metrics and analytics to the \*\*Automated SOC Detection \& Response Lab\*\*.

The objective is to convert outputs from previous detections into measurable SOC indicators.

The analytics engine consumes data from:

\- Incident deduplication

\- SLA monitoring

\- Incident risk scoring

\- Response recommendation decisions

\- Timeline reconstruction

It produces both machine-readable JSON metrics and an analyst-readable Markdown report.

\---

\## Analytics Workflow

```text

Deduplication Results

&#x20;       +

SLA Evaluations

&#x20;       +

Risk Assessments

&#x20;       +

Response Decisions

&#x20;       +

Timeline Metrics

&#x20;       |

&#x20;       v

SOC Metrics Engine

&#x20;       |

&#x20;       +-- Alert Metrics

&#x20;       +-- Incident Metrics

&#x20;       +-- Deduplication Metrics

&#x20;       +-- SLA Metrics

&#x20;       +-- Risk Metrics

&#x20;       +-- Escalation Metrics

&#x20;       +-- Timeline Metrics

&#x20;       |

&#x20;       v

JSON Metrics

&#x20;       +

Markdown Analytics Report

```

\---

\## Source Components

Detection 014 aggregates data from previous stages of the lab.

| Detection | Data Used |

|---|---|

| Detection 009 | Alert and incident correlation |

| Detection 010 | SLA state and escalation |

| Detection 011 | Incident risk scoring |

| Detection 012 | Incident timeline metrics |

| Detection 013 | Response and escalation decisions |

This demonstrates how operational SOC data can be transformed into measurable analytics.

\---

\## Alert and Incident Metrics

The deduplication dataset contains:

```text

Alerts Processed:      4

Incidents Created:     3

Correlated Alerts:     1

```

The engine calculates:

```text

Deduplication Rate:

Correlated Alerts / Alerts Processed

1 / 4 = 25%

```

and:

```text

Incident Creation Rate:

Incidents Created / Alerts Processed

3 / 4 = 75%

```

\### Result

| Metric | Value |

|---|---:|

| Alerts Processed | 4 |

| Incidents Created | 3 |

| Correlated Alerts | 1 |

| Deduplication Rate | 25% |

| Incident Creation Rate | 75% |

\---

\## SLA Metrics

Three SLA evaluation scenarios were included:

```text

WITHIN\_SLA

AT\_RISK

BREACHED

```

\### Result

| SLA State | Count |

|---|---:|

| WITHIN\_SLA | 1 |

| AT\_RISK | 1 |

| BREACHED | 1 |

Total evaluations:

```text

3

```

SLA compliance rate:

```text

1 / 3 = 33.33%

```

SLA breach rate:

```text

1 / 3 = 33.33%

```

These percentages represent the controlled validation dataset and should not be interpreted as production SOC performance.

\---

\## Risk Metrics

Two incident-risk assessments were included.

| Scenario | Risk Score | Risk Level |

|---|---:|---|

| Baseline | 40 | MEDIUM |

| Deteriorated | 75 | CRITICAL |

Average risk score:

```text

(40 + 75) / 2 = 57.5

```

Highest observed risk score:

```text

75

```

\### Risk Distribution

```text

MEDIUM   : 1

CRITICAL : 1

```

\---

\## Response Metrics

Three response-recommendation scenarios were evaluated:

```text

Baseline

Critical

Breached

```

The baseline scenario did not require escalation.

The critical and breached scenarios required escalation.

\### Result

| Metric | Value |

|---|---:|

| Response Decisions | 3 |

| Escalated Decisions | 2 |

| Escalation Rate | 66.67% |

Urgency distribution includes:

```text

STANDARD

IMMEDIATE

IMMEDIATE

```

Therefore:

```text

STANDARD  : 1

IMMEDIATE : 2

```

\---

\## Timeline Metrics

The reconstructed incident timeline contains:

```text

5 events

```

The timeline records:

```text

timeline\_start\_utc

timeline\_end\_utc

total\_timeline\_duration\_minutes

```

The elapsed timeline duration represents the time across the generated lab artifacts.

It is intentionally \*\*not labeled MTTD or MTTR\*\* because the current lab data was generated across separate development sessions and does not represent production SOC response timing.

\---

\## Metric Summary

The test dataset produced the following high-level results:

| Category | Metric | Value |

|---|---|---:|

| Alert | Alerts Processed | 4 |

| Incident | Incidents Created | 3 |

| Correlation | Correlated Alerts | 1 |

| Correlation | Deduplication Rate | 25% |

| SLA | Evaluations | 3 |

| SLA | Compliance Rate | 33.33% |

| SLA | Breach Rate | 33.33% |

| Risk | Assessments | 2 |

| Risk | Average Risk Score | 57.5 |

| Risk | Highest Risk Score | 75 |

| Response | Decisions | 3 |

| Response | Escalated Decisions | 2 |

| Response | Escalation Rate | 66.67% |

| Timeline | Events | 5 |

\---

\## Generated Output

Detection 014 creates two output artifacts.

\### JSON Metrics

```text

soc-metrics.json

```

The JSON output contains:

```text

generated\_at\_utc

dataset

alert\_metrics

sla\_metrics

risk\_metrics

response\_metrics

timeline\_metrics

```

\### Markdown Report

```text

soc-metrics-report.md

```

The Markdown report provides an analyst-readable summary of the calculated metrics.

\---

\## Example Analytics Flow

```text

4 Security Alerts

&#x20;     |

&#x20;     v

Deduplication

&#x20;     |

&#x20;     +--> 1 Correlated Alert

&#x20;     |

&#x20;     v

3 Incidents

&#x20;     |

&#x20;     v

SLA Evaluation

&#x20;     |

&#x20;     +--> 1 Within SLA

&#x20;     +--> 1 At Risk

&#x20;     `--> 1 Breached

&#x20;     |

&#x20;     v

Risk Assessment

&#x20;     |

&#x20;     +--> MEDIUM

&#x20;     `--> CRITICAL

&#x20;     |

&#x20;     v

Response Decisions

&#x20;     |

&#x20;     +--> 1 Standard

&#x20;     `--> 2 Escalated

&#x20;     |

&#x20;     v

SOC Analytics Report

```

\---

\## SOC Value

SOC teams need more than individual alerts and cases. They also need visibility into how detection and response processes behave over time.

Detection 014 demonstrates how SOC automation artifacts can be transformed into measurable indicators.

This can help with:

\- Alert-volume analysis

\- Incident-volume tracking

\- Deduplication measurement

\- SLA monitoring

\- Risk trend analysis

\- Escalation tracking

\- Operational reporting

\- Detection-engineering validation

\- Workflow-performance analysis

\---

\## Important Interpretation Note

The metrics generated in this detection come from a controlled lab dataset.

For example:

```text

SLA Compliance Rate: 33.33%

Escalation Rate:     66.67%

```

These values exist because the dataset intentionally contains multiple test states.

They should \*\*not\*\* be presented as the performance metrics of a real SOC environment.

The purpose of Detection 014 is to demonstrate the analytics pipeline and calculation logic.

\---

\## Evidence Structure

```text

detection-014-soc-metrics-analytics/

|

|-- README.md

|

|-- evidence/

|   `-- metrics-input.json

|

|-- sample-output/

|   |-- soc-metrics.json

|   `-- soc-metrics-report.md

|

`-- scripts/

&#x20;   `-- soc\_metrics.py

```

\---

\## Limitations

Current limitations include:

\- Small controlled dataset

\- Local JSON input

\- Static test scenarios

\- No historical metrics database

\- No dashboard visualization

\- No trend analysis

\- No real-time metric collection

\- No production MTTD calculation

\- No production MTTR calculation

\- No analyst workload metrics

\- No case-aging distribution

\- No detection false-positive metrics

\---

\## Future Improvements

Future versions can include:

\- Real-time Wazuh metrics ingestion

\- Daily and weekly SOC summaries

\- MTTD calculation

\- MTTR calculation

\- Mean time to containment

\- Mean time to escalation

\- Alert-volume trends

\- Incident-severity distribution

\- Analyst workload metrics

\- Case-aging analysis

\- False-positive rate

\- Detection effectiveness metrics

\- SLA compliance trends

\- Dashboard visualization

\- CSV export

\- SIEM dashboard integration

\---

\## Learning Outcome

Detection 014 demonstrates:

```text

Collect SOC Artifacts

&#x20;      |

&#x20;      v

Extract Operational Data

&#x20;      |

&#x20;      v

Calculate Metrics

&#x20;      |

&#x20;      v

Calculate Percentages

&#x20;      |

&#x20;      v

Summarize Risk and SLA

&#x20;      |

&#x20;      v

Analyze Escalations

&#x20;      |

&#x20;      v

Generate SOC Report

```

This extends the lab from individual detection and response automation into SOC-level operational analytics.


