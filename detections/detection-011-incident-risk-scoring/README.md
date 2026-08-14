# Detection 011 - Automated Incident Risk Scoring

## Overview

Detection 011 adds explainable incident risk scoring to the **Automated SOC Detection & Response Lab**.

The engine calculates an overall incident risk score using multiple security and operational signals instead of relying only on the original alert severity.

The following factors are evaluated:

- Wazuh rule severity
- IOC risk
- MITRE ATT&CK context
- Asset criticality
- Containment status
- SLA status
- Correlated alert volume

The final score is normalized to a **0-100 scale** and mapped to a risk classification.

| Risk Score | Classification |
|---:|---|
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
       +-- MITRE ATT&CK Context
       +-- Asset Criticality
       +-- Containment Status
       +-- SLA Status
       +-- Correlated Activity
       |
       v
Calculate Component Scores
       |
       v
Aggregate Risk Score
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

## Risk Scoring Model

### Wazuh Severity

| Wazuh Rule Level | Score |
|---:|---:|
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

The current lab assigns the following score to the tested technique:

```text
T1046 - Network Service Discovery = 8 points
```

Other MITRE techniques currently receive the default contextual score configured in the scoring engine.

### Asset Criticality

| Asset Criticality | Score |
|---|---:|
| CRITICAL | 15 |
| HIGH | 12 |
| MEDIUM | 8 |
| LOW | 3 |
| UNKNOWN | 0 |

### Containment Status

| Containment Status | Score |
|---|---:|
| FAILED | 15 |
| NOT_ATTEMPTED | 8 |
| UNKNOWN | 5 |
| SUCCESS | 0 |

### SLA Status

| SLA Status | Score |
|---|---:|
| BREACHED | 10 |
| AT_RISK | 5 |
| WITHIN_SLA | 0 |

### Correlated Activity

| Alert Count | Score |
|---:|---:|
| 10+ | 10 |
| 5-9 | 7 |
| 2-4 | 4 |
| 1 | 0 |

---

## Scenario 1 - Baseline Incident

The baseline scenario represents the controlled reconnaissance incident after successful automated containment.

### Incident Context

```text
Wazuh Rule Level    : 10
IOC Risk            : INFO
MITRE Technique     : T1046 - Network Service Discovery
Asset Criticality   : MEDIUM
Containment Status  : SUCCESS
SLA Status          : WITHIN_SLA
Correlated Alerts   : 2
```

### Score Calculation

```text
Wazuh Severity      : 20
IOC Risk            :  0
MITRE Context       :  8
Asset Criticality   :  8
Containment Status  :  0
SLA Status          :  0
Correlated Activity :  4
                      ----
Total Risk Score    : 40
```

### Result

```text
Risk Score          : 40/100
Risk Level          : MEDIUM
Recommended Action  : Standard SOC investigation with contextual validation
```

---

## Scenario 2 - Deteriorated Incident

The same underlying incident was tested again after its operational context deteriorated.

### Context Changes

```text
Asset Criticality   : MEDIUM     -> HIGH
Containment Status  : SUCCESS    -> FAILED
SLA Status          : WITHIN_SLA -> BREACHED
Correlated Alerts   : 2          -> 10
```

### Score Calculation

```text
Wazuh Severity      : 20
IOC Risk            :  0
MITRE Context       :  8
Asset Criticality   : 12
Containment Status  : 15
SLA Status          : 10
Correlated Activity : 10
                      ----
Total Risk Score    : 75
```

### Result

```text
Risk Score          : 75/100
Risk Level          : CRITICAL
Recommended Action  : Immediate SOC escalation, containment validation,
                      and incident-response investigation required
```

This demonstrates that the risk score changes dynamically as operational conditions worsen.

---

## Scenario 3 - Maximum-Risk Validation

A maximum-risk scenario was created to verify score normalization and the 100-point upper limit.

### Incident Context

```text
Wazuh Rule Level    : 15
IOC Risk            : CRITICAL
MITRE Technique     : T1046 - Network Service Discovery
Asset Criticality   : CRITICAL
Containment Status  : FAILED
SLA Status          : BREACHED
Correlated Alerts   : 15
```

### Score Calculation

```text
Wazuh Severity      : 25
IOC Risk            : 20
MITRE Context       :  8
Asset Criticality   : 15
Containment Status  : 15
SLA Status          : 10
Correlated Activity : 10
                      ----
Raw Risk Score      : 103
Final Risk Score    : 100
```

The engine uses a maximum score cap, preventing the final value from exceeding 100.

### Result

```text
Risk Score          : 100/100
Risk Level          : CRITICAL
Recommended Action  : Immediate SOC escalation, containment validation,
                      and incident-response investigation required
```

---

## Validation Summary

| Scenario | Raw Score | Final Score | Risk Level |
|---|---:|---:|---|
| Baseline Incident | 40 | 40 | MEDIUM |
| Deteriorated Incident | 75 | 75 | CRITICAL |
| Maximum-Risk Incident | 103 | 100 | CRITICAL |

The tests demonstrate three important behaviors:

- Multiple security signals contribute independently to risk.
- Operational deterioration increases the incident risk score.
- Scores exceeding the supported range are capped at 100.

---

## Explainable Risk Scoring

The engine does not return only a final number. It records the contribution of every risk component.

Example baseline output:

```text
wazuh_severity      : 20
ioc_risk            : 0
mitre_context       : 8
asset_criticality   : 8
containment_status  : 0
sla_status          : 0
correlated_activity : 4
```

This allows a SOC analyst to understand why an incident received its classification.

```text
Security Context
       |
       v
Individual Risk Components
       |
       v
Explainable Score
       |
       v
Risk Classification
       |
       v
Recommended Analyst Action
```

---

## Generated Output

Each risk assessment produces a structured JSON document containing:

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

Example:

```text
Incident ID         : INC-20260813-051403-8E6ED3A1
Case ID             : CASE-20260814-035612-R100111
Risk Score          : 40
Risk Level          : MEDIUM
```

---

## Integration with Previous Detections

Detection 011 consumes security context generated by earlier stages of the lab.

```text
Wazuh Detection
       |
       v
IOC Enrichment
       |
       v
Automated Alert Triage
       |
       v
Incident Reporting
       |
       v
Case Management
       |
       v
Notification / Escalation
       |
       v
Incident Deduplication
       |
       v
SLA Monitoring
       |
       v
Incident Risk Scoring
```

This allows the risk engine to make decisions using information collected throughout the SOC workflow.

---

## SOC Value

Traditional alert prioritization may rely heavily on the severity assigned by a detection rule.

Detection 011 demonstrates a more contextual approach:

```text
Wazuh Severity
      +
IOC Reputation
      +
MITRE ATT&CK Context
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
Context-Aware Risk Score
      |
      v
SOC Priority Decision
```

This approach can help:

- Improve incident prioritization
- Identify deteriorating incidents
- Reduce reliance on a single severity field
- Provide explainable analyst decisions
- Incorporate operational context into security decisions
- Support escalation workflows
- Standardize risk assessment across incidents

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

- Static risk weights
- Limited MITRE technique weighting
- Local JSON-based input
- No vulnerability severity context
- No identity-risk context
- No user privilege assessment
- No business-impact calculation
- No historical risk baseline
- No environment-specific weighting
- No automatic Wazuh API ingestion

---

## Future Improvements

Future versions can include:

- CVE and CVSS context
- Exploitability information
- User and identity risk
- Privileged-account context
- Business-service criticality
- Threat-intelligence confidence scoring
- Historical incident frequency
- Dynamic scoring weights
- Environment-specific risk profiles
- Automatic risk recalculation
- Case-management integration
- SOAR-based risk-driven response

---

## Learning Outcome

Detection 011 demonstrates an end-to-end contextual risk calculation process:

```text
Collect Incident Context
       |
       v
Evaluate Security Signals
       |
       v
Calculate Component Scores
       |
       v
Aggregate Risk
       |
       v
Normalize to 0-100
       |
       v
Assign Risk Level
       |
       v
Recommend SOC Action
```

The result is an explainable and context-aware incident risk score that can support SOC prioritization, investigation, and escalation decisions.
