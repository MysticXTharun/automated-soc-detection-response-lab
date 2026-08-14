# Detection 011 - Automated Incident Risk Scoring

## Overview

Detection 011 adds explainable incident risk scoring to the Automated SOC Detection & Response Lab.

The goal is to calculate an overall incident risk score using multiple security and operational signals instead of relying on a single alert severity value.

The engine evaluates:

- Wazuh rule severity

- IOC risk

- MITRE ATT&CK context

- Asset criticality

- Containment status

- SLA status

- Correlated alert volume

The final score is normalized to a range of:

```text

0 - 100

```

and mapped to a risk classification:

| Score | Risk Level |

|---|---|

| 0-29 | LOW |

| 30-49 | MEDIUM |

| 50-74 | HIGH |

| 75-100 | CRITICAL |

---

## Risk Scoring Workflow

```text

Incident Context

     |

     v

Collect Risk Signals

     |

     +-- Wazuh Severity

     +-- IOC Risk

     +-- MITRE Context

     +-- Asset Criticality

     +-- Containment Status

     +-- SLA Status

     +-- Correlated Activity

     |

     v

Calculate Component Scores

     |

     v

Sum Risk Components

     |

     v

Cap Score at 100

     |

     v

Assign Risk Classification

     |

     v

Generate Recommended SOC Action

```

---

## Risk Components

### Wazuh Severity

| Wazuh Level | Score |

|---|---:|

| 12+ | 25 |

| 8-11 | 20 |

| 4-7 | 12 |

| 0-3 | 5 |

### IOC Risk

| IOC Risk | Score |

|---|---:|

| CRITICAL | 20 |

| HIGH | 16 |

| MEDIUM | 10 |

| LOW | 5 |

| UNKNOWN | 2 |

| INFO | 0 |

### MITRE ATT&CK Context

The current lab assigns:

```text

T1046 - Network Service Discovery = 8 points

```

Other techniques currently receive a default contextual score.

### Asset Criticality

| Asset Criticality | Score |

|---|---:|

| CRITICAL | 15 |

| HIGH | 12 |

| MEDIUM | 8 |

| LOW | 3 |

| UNKNOWN | 0 |

### Containment Status

| Status | Score |

|---|---:|

| FAILED | 15 |

| NOT_ATTEMPTED | 8 |

| UNKNOWN | 5 |

| SUCCESS | 0 |

### SLA Status

| SLA State | Score |

|---|---:|

| BREACHED | 10 |

| AT_RISK | 5 |

| WITHIN_SLA | 0 |

### Correlated Activity

| Alert Count | Score |

|---|---:|

| 10+ | 10 |

| 5-9 | 7 |

| 2-4 | 4 |

| 1 | 0 |

---

## Scenario 1 - Baseline Incident

The baseline incident represents the controlled reconnaissance workflow with successful containment.

### Context

```text

Wazuh Rule Level:     10

IOC Risk:             INFO

MITRE Technique:      T1046

Asset Criticality:    MEDIUM

Containment Status:   SUCCESS

SLA Status:           WITHIN_SLA

Correlated Alerts:    2

```

### Component Scores

| Component | Score |

|---|---:|

| Wazuh Severity | 20 |

| IOC Risk | 0 |

| MITRE Context | 8 |

| Asset Criticality | 8 |

| Containment Status | 0 |

| SLA Status | 0 |

| Correlated Activity | 4 |

Total:

```text

40

```

### Result

```text

Risk Score: 40

Risk Level: MEDIUM

```

Recommended action:

```text

Standard SOC investigation with contextual validation

```

---

## Scenario 2 - Deteriorated Incident

The same underlying incident is evaluated after the operational context worsens.

### Context Changes

```text

Asset Criticality:

MEDIUM â†’ HIGH

Containment:

SUCCESS â†’ FAILED

SLA:

WITHIN_SLA â†’ BREACHED

Correlated Alerts:

2 â†’ 10

```

### Component Scores

| Component | Score |

|---|---:|

| Wazuh Severity | 20 |

| IOC Risk | 0 |

| MITRE Context | 8 |

| Asset Criticality | 12 |

| Containment Status | 15 |

| SLA Status | 10 |

| Correlated Activity | 10 |

Total:

```text

75

```

### Result

```text

Risk Score: 75

Risk Level: CRITICAL

```

Recommended action:

```text

Immediate SOC escalation, containment validation, and incident-response investigation required

```

This demonstrates that the same incident can become substantially more risky as operational conditions deteriorate.

---

## Scenario 3 - Maximum Risk

A maximum-risk scenario was used to test score normalization.

### Context

```text

Wazuh Rule Level:     15

IOC Risk:             CRITICAL

MITRE Technique:      T1046

Asset Criticality:    CRITICAL

Containment Status:   FAILED

SLA Status:           BREACHED

Correlated Alerts:    15

```

### Component Scores

| Component | Score |

|---|---:|

| Wazuh Severity | 25 |

| IOC Risk | 20 |

| MITRE Context | 8 |

| Asset Criticality | 15 |

| Containment Status | 15 |

| SLA Status | 10 |

| Correlated Activity | 10 |

Raw total:

```text

103

```

The engine caps the final result at:

```text

100

```

### Result

```text

Risk Score: 100

Risk Level: CRITICAL

```

This confirms that the scoring model remains bounded to the intended 0-100 range.

---

## Dynamic Risk Comparison

| Scenario | Raw Score | Final Score | Risk |

|---|---:|---:|---|

| Baseline | 40 | 40 | MEDIUM |

| Deteriorated | 75 | 75 | CRITICAL |

| Maximum Risk | 103 | 100 | CRITICAL |

The result demonstrates that risk classification changes dynamically based on accumulated security context.

---

## Explainable Scoring

The engine outputs the individual contribution of every signal.

Example:

```text

wazuh_severity      : 20

ioc_risk            : 0

mitre_context       : 8

asset_criticality   : 8

containment_status  : 0

sla_status          : 0

correlated_activity : 4

```

This makes the risk score explainable to an analyst.

Instead of seeing only:

```text

Risk Score: 40

```

the analyst can understand exactly which conditions contributed to the result.

---

## Generated Output

The engine generates a structured JSON result containing:

```text

evaluation_timestamp_utc

incident_id

case_id

rule_id

risk_score

risk_level

recommended_action

risk_components

context

```

---

## SOC Value

Detection 011 demonstrates how a SOC can combine multiple operational signals into one explainable incident-risk assessment.

Instead of:

```text

Alert Severity

     |

     v

Manual Risk Decision

```

the workflow becomes:

```text

Alert Severity

     +

IOC Reputation

     +

MITRE Context

     +

Asset Criticality

     +

Containment State

     +

SLA State

     +

Correlated Activity

     |

     v

Explainable Risk Score

     |

     v

Recommended SOC Action

```

This can improve consistency in incident prioritization and analyst decision-making.

---

## Evidence Structure

```text

detection-011-incident-risk-scoring/

|

|-- README.md

|

|-- evidence/

|   |-- risk-input-100111.json

|   |-- risk-input-100111-deteriorated.json

|   `-- risk-input-100111-max-risk.json

|

|-- sample-output/

|   |-- risk-result-100111.json

|   |-- risk-result-100111-deteriorated.json

|   `-- risk-result-100111-max-risk.json

|

`-- scripts/

   `-- incident_risk_scoring.py

```

---

## Limitations

This implementation is designed for a controlled SOC lab.

Current limitations include:

- Static scoring weights

- Limited MITRE technique weighting

- Local JSON input

- No vulnerability context

- No identity-risk context

- No business-impact scoring

- No historical risk baseline

- No external risk engine

- No automatic Wazuh API ingestion

- No dynamic weighting based on environment

---

## Future Improvements

Future versions can include:

- CVE severity

- Exploitability context

- Identity risk

- User privilege

- Business-service criticality

- Threat-intelligence confidence

- Historical incident frequency

- Dynamic scoring weights

- Environment-specific risk profiles

- Machine-learning-assisted scoring

- Case-management integration

- Automatic risk recalculation

---

## Learning Outcome

Detection 011 demonstrates:

```text

Collect Incident Context

     |

     v

Score Individual Signals

     |

     v

Aggregate Risk

     |

     v

Normalize 0-100

     |

     v

Assign Risk Level

     |

     v

Recommend SOC Action

```

This extends the lab with explainable, context-aware incident risk scoring.


