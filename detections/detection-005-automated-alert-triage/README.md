# Detection 005 - Automated Alert Triage and Prioritization

## Overview

Detection 005 extends the Automated SOC Detection & Response Lab with context-aware alert triage and prioritization.

Instead of assigning priority based only on SIEM severity, the Python triage engine evaluates multiple security signals to calculate an overall triage score and recommend an analyst response.

The engine evaluates:

- Wazuh alert severity
- IOC risk assessment
- MITRE ATT&CK technique context
- Destination asset criticality
- Automated containment status

The resulting score is converted into a SOC priority from P1 to P4.

---

## Triage Pipeline

```text
Wazuh Alert
    |
    v
IOC Enrichment
    |
    v
Context-Aware Triage Engine
    |
    +-- Wazuh Severity
    +-- IOC Risk
    +-- MITRE Technique
    +-- Asset Criticality
    +-- Containment Status
    |
    v
Triage Score
    |
    v
P1 / P2 / P3 / P4
    |
    v
Recommended SOC Action
```

---

## Related Detection

The test input originates from the correlated network reconnaissance workflow.

| Field | Value |
|---|---|
| Wazuh Rule ID | 100111 |
| Wazuh Level | 10 |
| Source IP | 192.168.130.141 |
| Destination IP | 192.168.130.130 |
| Destination Port | 445 |
| MITRE Technique | Network Service Discovery |
| MITRE ID | T1046 |
| MITRE Tactic | Discovery |

---

## Input Sources

Detection 005 consumes three contextual data sources.

### Alert and IOC Context

`triage-input-100111.json`

Contains:

- Wazuh rule information
- Network context
- MITRE ATT&CK metadata
- IOC enrichment
- SOC risk assessment

### Asset Context

`asset-context.json`

Contains information about the destination asset:

```text
Hostname: DESKTOP-D316EOG
Asset Type: Windows 11 Endpoint
Criticality: MEDIUM
Business Context: SOC lab monitored endpoint
```

### Response Context

Response-context files describe the outcome of automated containment.

The lab tests both:

```text
Containment Status: SUCCESS
```

and:

```text
Containment Status: FAILED
```

---

## Scoring Model

The triage engine calculates priority using five signals.

### Wazuh Severity

| Wazuh Level | Score |
|---|---:|
| 12+ | 50 |
| 8-11 | 40 |
| 4-7 | 25 |
| 0-3 | 10 |

Rule `100111` has level `10`.

```text
Wazuh Severity Score = 40
```

### IOC Risk

| IOC Risk | Score |
|---|---:|
| CRITICAL | 50 |
| HIGH | 40 |
| MEDIUM | 25 |
| LOW | 10 |
| UNKNOWN | 5 |
| INFO | 0 |

The controlled Kali source is a private IP.

```text
IOC Risk = INFO
IOC Risk Score = 0
```

### MITRE ATT&CK Context

The reconnaissance alert maps to:

```text
T1046 - Network Service Discovery
```

The lab assigns:

```text
MITRE Technique Score = 10
```

The current implementation uses simplified technique scoring for demonstration purposes.

### Asset Criticality

| Criticality | Score |
|---|---:|
| CRITICAL | 30 |
| HIGH | 25 |
| MEDIUM | 15 |
| LOW | 5 |
| UNKNOWN | 0 |

The Windows 11 lab endpoint is classified as:

```text
Criticality = MEDIUM
Asset Score = 15
```

### Containment Status

| Status | Score Adjustment |
|---|---:|
| FAILED | +15 |
| NOT_ATTEMPTED | +5 |
| UNKNOWN | 0 |
| SUCCESS | -10 |

Successful containment reduces immediate triage urgency.

Failed containment increases priority because the detected source may remain capable of interacting with the monitored system.

---

## Priority Thresholds

| Total Score | Priority |
|---|---|
| 100 | P1 |
| 70-99 | P2 |
| 40-69 | P3 |
| 0-39 | P4 |

Scores are capped between `0` and `100`.

---

## Scenario 1 - Successful Containment

The first test represents successful automated Windows Firewall containment.

```text
Wazuh Severity         +40
IOC Risk                 0
MITRE T1046            +10
Asset Criticality      +15
Successful Containment -10
                       ---
Total                    55
```

Result:

```text
Priority: P3

Recommended Action:
Standard SOC analyst review and validate related activity
```

---

## Scenario 2 - Failed Containment

The second test uses the same detection but changes the containment result to `FAILED`.

```text
Wazuh Severity       +40
IOC Risk               0
MITRE T1046          +10
Asset Criticality    +15
Failed Containment   +15
                     ---
Total                  80
```

Result:

```text
Priority: P2

Recommended Action:
High-priority investigation and containment required
```

---

## Dynamic Prioritization Result

The same security activity receives different SOC priorities depending on operational context.

| Scenario | Score | Priority |
|---|---:|---|
| Containment Successful | 55 | P3 |
| Containment Failed | 80 | P2 |

This demonstrates why SIEM alert severity alone should not determine complete incident priority.

---

## SOC Value

With successful containment:

```text
HIGH Severity Alert
        +
Internal IOC
        +
MITRE Discovery Activity
        +
Medium-Criticality Asset
        +
Successful Containment
        |
        v
P3 Analyst Review
```

With failed containment:

```text
HIGH Severity Alert
        +
Internal IOC
        +
MITRE Discovery Activity
        +
Medium-Criticality Asset
        +
Failed Containment
        |
        v
P2 High-Priority Investigation
```

The triage decision therefore reflects both detection severity and current operational context.

---

## Evidence

```text
evidence/
    asset-context.json
    response-context.json
    response-context-failed.json
    triage-input-100111.json

sample-output/
    triage-result-100111.json
    triage-result-containment-failed.json

scripts/
    alert_triage.py
```

---

## Limitations

This implementation is designed for a controlled SOC lab.

Current limitations include:

- Simplified scoring thresholds
- Static asset inventory
- Limited MITRE technique scoring
- Manually supplied containment context
- No identity or user-risk context
- No vulnerability information
- No business-service dependency mapping
- No historical alert-frequency scoring
- No automatic Wazuh API ingestion

The calculated score should therefore be treated as a lab triage model rather than a production risk score.

---

## Future Improvements

Future versions can incorporate:

- CVE and vulnerability context
- Asset exposure
- User and identity risk
- Threat-intelligence confidence
- Alert frequency
- Historical incidents
- Multiple MITRE techniques
- Business impact
- Detection confidence
- Automatic Wazuh API ingestion
- Case-management integration
- SLA assignment based on priority

---

## Learning Outcome

Detection 005 demonstrates:

```text
Detect
  |
  v
Enrich
  |
  v
Add Asset Context
  |
  v
Evaluate Response Status
  |
  v
Calculate Risk Signals
  |
  v
Assign Priority
  |
  v
Recommend SOC Action
```

This extends the lab from automated detection and response into context-aware SOC alert prioritization.