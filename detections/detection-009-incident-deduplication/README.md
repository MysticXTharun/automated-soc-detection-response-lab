# Detection 009 - Automated Incident Deduplication and Correlation

## Overview

Detection 009 adds automated incident deduplication and time-based alert correlation to the Automated SOC Detection & Response Lab.

Security monitoring platforms can generate multiple alerts for repeated activity. Creating a separate incident for every repeated alert can increase analyst workload and contribute to alert fatigue.

This detection introduces a correlation engine that determines whether an incoming alert should:

- Create a new incident
- Be correlated with an existing incident

The decision is based on security context and a configurable correlation time window.

---

## Correlation Workflow

```text
Incoming Alert
    |
    v
Extract Correlation Fields
    |
    +-- Rule ID
    +-- Source IP
    +-- Destination IP
    +-- Destination Port
    +-- MITRE Technique
    |
    v
Generate Correlation Key
    |
    v
Search Existing Incidents
    |
    +---------------------+
    |                     |
    v                     v
 Matching Key          No Match
    |                     |
    v                     v
Check Time Window      Create New
    |                  Incident
    v
Within Window?
    |
 +--+--+
 |     |
 v     v
Yes    No
 |     |
 v     v
Correlate          Create New
Alert              Incident
```

---

## Correlation Logic

The engine uses two conditions to determine whether alerts belong to the same incident:

1. The alerts must generate the same correlation key.
2. The matching alert must occur within the configured correlation window.

If both conditions are satisfied, the alert is correlated with the existing incident.

Otherwise, a new incident is created.

---

## Correlation Fields

The correlation key is generated using:

```text
Rule ID
+
Source IP
+
Destination IP
+
Destination Port
+
MITRE Technique ID
```

For the primary reconnaissance activity:

```text
Rule ID:          100111
Source IP:        192.168.130.141
Destination IP:   192.168.130.130
Destination Port: 445
MITRE ID:         T1046
```

Alerts containing the same values for these fields generate the same correlation key.

---

## Correlation Window

The lab uses a default correlation window of:

```text
5 minutes
```

A matching alert is attached to an existing incident only when it occurs within the configured correlation window.

The window can be changed using:

```text
--window <minutes>
```

This prevents matching activity from being correlated indefinitely.

---

## Test Scenarios

Four alerts were used to validate the engine.

| Alert | Source IP | Scenario | Expected Decision |
|---|---|---|---|
| Alert 001 | 192.168.130.141 | Initial reconnaissance activity | NEW |
| Alert 002 | 192.168.130.141 | Same activity within 5 minutes | CORRELATED |
| Alert 003 | 192.168.130.150 | Same detection from different source | NEW |
| Alert 004 | 192.168.130.141 | Same activity outside 5-minute window | NEW |

---

## Scenario 1 - Initial Alert

The first alert represents the initial reconnaissance activity.

```text
Timestamp:      2026-08-13T05:14:03.915+00:00
Source IP:      192.168.130.141
Destination IP: 192.168.130.130
Port:           445
Rule ID:        100111
MITRE ID:       T1046
```

No matching incident exists.

### Result

```text
Decision:    NEW
Incident ID: INC-20260813-051403-8E6ED3A1
```

A new incident is created.

---

## Scenario 2 - Duplicate Activity Within Correlation Window

The second alert contains the same correlation fields as the original alert.

```text
Timestamp: 2026-08-13T05:17:41.250+00:00
Source IP: 192.168.130.141
```

The alert occurs approximately:

```text
3.62 minutes
```

after the previous matching alert.

Because it occurs within the configured 5-minute window, it is correlated with the existing incident.

### Result

```text
Decision:    CORRELATED
Incident ID: INC-20260813-051403-8E6ED3A1
```

Alert 001 and Alert 002 therefore share the same incident ID.

This demonstrates successful incident deduplication.

---

## Scenario 3 - Different Source

The third alert triggers the same Wazuh rule against the same destination and port but originates from a different source.

```text
Timestamp: 2026-08-13T05:19:12.500+00:00
Source IP: 192.168.130.150
```

Because the source IP is part of the correlation key, this alert generates a different key.

### Result

```text
Decision:    NEW
Incident ID: INC-20260813-051912-7FB01649
```

A separate incident is created.

---

## Scenario 4 - Outside Correlation Window

The fourth alert returns to the original source:

```text
Timestamp: 2026-08-13T05:30:00.000+00:00
Source IP: 192.168.130.141
```

Its security attributes match the original activity, so it generates the same correlation key.

However, the activity occurs outside the configured 5-minute correlation window.

### Result

```text
Decision:    NEW
Incident ID: INC-20260813-053000-8E6ED3A1
```

The correlation-key suffix remains `8E6ED3A1` because the security attributes match.

A new incident ID is still generated because the previous matching activity is outside the allowed correlation window.

---

## Validation Results

| Timestamp | Source IP | Decision | Incident ID |
|---|---|---|---|
| 05:14:03 | 192.168.130.141 | NEW | INC-20260813-051403-8E6ED3A1 |
| 05:17:41 | 192.168.130.141 | CORRELATED | INC-20260813-051403-8E6ED3A1 |
| 05:19:12 | 192.168.130.150 | NEW | INC-20260813-051912-7FB01649 |
| 05:30:00 | 192.168.130.141 | NEW | INC-20260813-053000-8E6ED3A1 |

### Processing Summary

```text
Alerts Processed:       4
Incidents Created:      3
Duplicates Correlated:  1
Correlation Window:     5 minutes
```

The test confirms the expected behavior:

```text
Alert 001 --> NEW
Alert 002 --> CORRELATED with Alert 001
Alert 003 --> NEW
Alert 004 --> NEW
```

---

## Incident Tracking

Each generated incident maintains the following information:

```text
incident_id
correlation_key
rule_id
source_ip
destination_ip
destination_port
mitre_ids
first_seen
last_seen
alert_count
related_alert_timestamps
```

When another matching alert is correlated with an existing incident, the engine updates:

```text
last_seen
alert_count
related_alert_timestamps
```

This allows multiple related alerts to be represented as a single SOC investigation context.

---

## Example Correlated Incident

The first two alerts are represented as one incident.

```text
Incident ID: INC-20260813-051403-8E6ED3A1

Source IP: 192.168.130.141

First Seen:
2026-08-13T05:14:03.915+00:00

Last Seen:
2026-08-13T05:17:41.250+00:00

Alert Count: 2
```

Instead of creating two independent incidents, repeated activity is grouped into one investigation.

---

## Deduplication Comparison

### Without Deduplication

```text
Alert 001 ---> Incident 1
Alert 002 ---> Incident 2
Alert 003 ---> Incident 3
Alert 004 ---> Incident 4

4 Alerts
4 Incidents
```

### With Deduplication

```text
Alert 001 -----+
               |
Alert 002 -----+----> Incident 1

Alert 003 ----------> Incident 2

Alert 004 ----------> Incident 3

4 Alerts
3 Incidents
```

One duplicate alert is successfully absorbed into an existing incident.

---

## SOC Value

Incident deduplication helps reduce unnecessary case creation when repeated alerts represent the same underlying activity.

The workflow changes from:

```text
Repeated Alerts
      |
      v
Multiple Independent Cases
      |
      v
Additional Analyst Work
```

to:

```text
Repeated Alerts
      |
      v
Correlation Engine
      |
      v
Related Alerts Grouped
      |
      v
Single Investigation Context
```

This can help SOC analysts:

- Reduce duplicate investigations
- Reduce alert and case noise
- Preserve related-event context
- Track repeated activity using first-seen and last-seen timestamps
- Focus on distinct security incidents
- Maintain cleaner incident queues

---

## Generated Output

The engine creates:

```text
deduplication-result.json
```

The output contains:

```text
correlation_window_minutes
alerts_processed
incidents_created
duplicates_correlated
results
incidents
```

The `results` section records the decision made for every alert.

The `incidents` section contains the final correlated incident dataset.

---

## Evidence Structure

```text
detection-009-incident-deduplication/
|
|-- README.md
|
|-- evidence/
|   |-- alert-001-original.json
|   |-- alert-002-duplicate.json
|   |-- alert-003-different-source.json
|   `-- alert-004-outside-window.json
|
|-- sample-output/
|   `-- deduplication-result.json
|
`-- scripts/
    `-- deduplication_engine.py
```

---

## Limitations

This implementation is designed for a controlled SOC lab.

Current limitations include:

- In-memory incident correlation
- Static correlation fields
- Local JSON input
- No persistent incident database
- No cross-rule correlation
- No fuzzy matching
- No user or identity correlation
- No asset-based correlation
- No historical incident lookup
- No automatic Wazuh API ingestion

---

## Future Improvements

Future versions can include:

- Persistent incident storage
- Automatic Wazuh API ingestion
- Cross-rule correlation
- Dynamic correlation windows
- Asset-aware correlation
- User and identity correlation
- Alert-frequency analysis
- Threat-intelligence correlation
- Multi-stage attack correlation
- MITRE ATT&CK tactic correlation
- Case-management integration
- Automatic incident merging

---

## Learning Outcome

Detection 009 demonstrates the following SOC workflow:

```text
Receive Alerts
      |
      v
Normalize Security Context
      |
      v
Generate Correlation Key
      |
      v
Search Existing Incidents
      |
      v
Evaluate Correlation Window
      |
      +--------------------+
      |                    |
      v                    v
Matching Activity      New Activity
Within Window          or Window Expired
      |                    |
      v                    v
Correlate Alert        Create Incident
      |                    |
      +---------+----------+
                |
                v
       Correlated Incident
             Dataset
```

Detection 009 extends the Automated SOC Detection & Response Lab with automated alert deduplication and time-based incident correlation.