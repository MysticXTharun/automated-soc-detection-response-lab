# Automated SOC Detection & Response Lab

A hands-on Security Operations Center (SOC) engineering project that simulates an end-to-end detection, investigation, automation, response, case-management, analytics, and reporting workflow using **Wazuh, Sysmon, Windows 11, Kali Linux, Python, MITRE ATT&CK, and Wazuh Active Response**.

The project progresses from raw endpoint telemetry and SIEM detection into context-aware SOC automation and simplified SOAR-style orchestration.

---

## Project Overview

The lab demonstrates the complete SOC lifecycle:

```text
Controlled Attack Simulation
        |
        v
Windows Endpoint Telemetry
        |
        v
Sysmon + Windows Event Logs
        |
        v
Wazuh Agent
        |
        v
Wazuh Manager / SIEM
        |
        v
Detection & Correlation
        |
        v
MITRE ATT&CK Mapping
        |
        v
Automated Containment
        |
        v
IOC Enrichment
        |
        v
Alert Triage
        |
        v
Incident Reporting
        |
        v
Case Management
        |
        v
Notification & Escalation
        |
        v
Playbook Orchestration
        |
        v
Incident Deduplication
        |
        v
SLA Monitoring
        |
        v
Incident Risk Scoring
        |
        v
Timeline Reconstruction
        |
        v
Response Recommendations
        |
        v
SOC Metrics & Analytics
        |
        v
Executive Reporting
```

---

## Lab Architecture

| System | Purpose | Lab IP |
|---|---|---|
| Ubuntu Server | Wazuh Manager / Indexer / Dashboard | `192.168.130.129` |
| Windows 11 | Monitored SOC Endpoint | `192.168.130.130` |
| Kali Linux | Controlled Attack Simulation | `192.168.130.141` |

### Architecture Flow

```text
                     Wazuh Server
                  192.168.130.129
                         ^
                         |
                  Security Telemetry
                         |
                         |
                 Windows 11 Endpoint
                  192.168.130.130
                   Wazuh + Sysmon
                         ^
                         |
                  Controlled Testing
                         |
                         |
                     Kali Linux
                  192.168.130.141
```

---

## Technology Stack

| Technology | Purpose |
|---|---|
| Wazuh | SIEM, XDR, detection, correlation, threat hunting |
| Sysmon | Advanced Windows endpoint telemetry |
| Windows Event Logs | Endpoint event collection |
| Windows Firewall | Network containment and response |
| Kali Linux | Controlled security simulations |
| Python | SOC automation and orchestration |
| MITRE ATT&CK | Detection and technique mapping |
| AbuseIPDB | Public IP reputation enrichment |
| PowerShell | Windows administration and validation |
| Git / GitHub | Version control and portfolio documentation |

---

## Key SOC Capabilities Demonstrated

This lab demonstrates practical implementation of:

- Security monitoring
- SIEM alert triage
- Incident investigation
- Threat hunting
- Detection engineering
- Event correlation
- MITRE ATT&CK mapping
- IOC enrichment
- Threat-intelligence usage
- Risk assessment
- Automated containment
- Case management
- SLA tracking
- Incident deduplication
- Response recommendations
- SOC metrics
- Executive reporting
- SOAR-style workflow orchestration

---

# Detection Engineering & Automation Modules

The project contains **15 detection and automation modules**.

| Detection | Module | Purpose |
|---|---|---|
| 001 | Network Reconnaissance Detection | Detect network discovery activity |
| 002 | Network Reconnaissance Correlation | Correlate repeated scanning and trigger containment |
| 003 | IOC Enrichment & SOC Risk Assessment | Enrich public IPs and classify IOC risk |
| 004 | Automated Incident Reporting | Convert enriched alerts into analyst-ready reports |
| 005 | Automated Alert Triage | Context-aware P1-P4 alert prioritization |
| 006 | Automated Case Management | Case ID, queue, SLA, timeline, assignment |
| 007 | SOC Notification & Escalation | Determine notification severity and escalation |
| 008 | Playbook Orchestration | Chain automation modules into a single workflow |
| 009 | Incident Deduplication | Correlate duplicate alerts into existing incidents |
| 010 | SLA Monitoring & Escalation | Detect SLA risk and breach conditions |
| 011 | Incident Risk Scoring | Calculate explainable 0-100 incident risk |
| 012 | Incident Timeline Reconstruction | Normalize and reconstruct incident chronology |
| 013 | Response Recommendation Engine | Recommend investigation, containment, and escalation actions |
| 014 | SOC Metrics & Analytics | Generate operational SOC metrics |
| 015 | SOC Executive Reporting | Aggregate incident and SOC data into management reports |

---

# Detection 001 - Network Reconnaissance Detection

Detection 001 identifies controlled network-reconnaissance activity against the monitored Windows endpoint.

The detection demonstrates:

```text
Network Activity
      |
      v
Windows Telemetry
      |
      v
Wazuh Detection
      |
      v
MITRE ATT&CK Mapping
```

Primary MITRE technique:

```text
T1046 - Network Service Discovery
```

---

# Detection 002 - Correlation and Automated Containment

Detection 002 extends individual alerting with correlation logic.

Repeated reconnaissance events are correlated into a higher-severity alert.

```text
Repeated Network Events
        |
        v
Wazuh Correlation Rule
        |
        v
High-Severity Alert
        |
        v
Active Response
        |
        v
Windows Firewall Containment
```

The workflow demonstrates:

- Event correlation
- Higher-level detection
- Wazuh Active Response
- Automated IP blocking
- Automatic recovery/unblocking

---

# Detection 003 - IOC Enrichment and SOC Risk Assessment

Detection 003 extracts an IOC from a manually supplied IP or Wazuh alert.

The automation performs:

```text
Extract IOC
    |
    v
Classify IP
    |
    +-- Private IP
    |
    `-- Public IP
            |
            v
       Reverse DNS
            |
            v
       AbuseIPDB Lookup
            |
            v
       SOC Risk Assessment
```

The script safely skips public threat-intelligence lookup for private IP addresses.

---

# Detection 004 - Automated Incident Reporting

Detection 004 converts enriched Wazuh alerts into structured SOC incident reports.

Generated incident context includes:

- Rule ID
- Severity
- Source IP
- Destination IP
- Destination port
- MITRE ATT&CK mapping
- IOC enrichment
- SOC risk assessment
- Investigation summary
- Recommended analyst actions

---

# Detection 005 - Automated Alert Triage

Detection 005 calculates analyst priority using multiple security signals.

```text
Wazuh Severity
      +
IOC Risk
      +
MITRE Technique
      +
Asset Criticality
      +
Containment Status
      |
      v
Context-Aware Triage Score
      |
      v
P1 / P2 / P3 / P4
```

Example validation:

```text
Successful Containment
Score: 55
Priority: P3

Failed Containment
Score: 80
Priority: P2
```

---

# Detection 006 - Automated Case Management

Detection 006 converts triage results into a structured SOC case.

The case contains:

- Unique case ID
- Case status
- Priority
- Assigned queue
- Analyst assignment state
- SLA
- SLA due time
- Incident timeline
- Closure recommendation

Example:

```text
Priority: P3
Queue: SOC Standard Investigation Queue
Owner: UNASSIGNED
SLA: 8 hours
Status: WITHIN_SLA
```

---

# Detection 007 - SOC Notification and Escalation

Detection 007 evaluates case priority, containment status, and SLA health.

Example decisions:

```text
P3 + SUCCESS + WITHIN_SLA
    |
    v
STANDARD Notification
No Escalation
```

```text
P2 + FAILED
    |
    v
HIGH Notification
L2 Escalation
```

```text
SLA BREACHED
    |
    v
CRITICAL Notification
Management Escalation
```

---

# Detection 008 - Automated SOC Playbook Orchestration

Detection 008 chains multiple SOC automation modules together.

```text
Wazuh Alert
    |
    v
IOC Enrichment
    |
    v
Automated Triage
    |
    v
Incident Reporting
    |
    v
Case Management
    |
    v
Notification & Escalation
    |
    v
Playbook Summary
```

The entire workflow can be executed using a single orchestration command.

---

# Detection 009 - Incident Deduplication and Correlation

Detection 009 reduces duplicate incident creation.

Correlation fields include:

```text
Rule ID
Source IP
Destination IP
Destination Port
MITRE Technique
Time Window
```

Validation:

```text
Alert 001 -> NEW
Alert 002 -> CORRELATED
Alert 003 -> NEW
Alert 004 -> NEW
```

Results:

```text
Alerts Processed: 4
Incidents Created: 3
Correlated Alerts: 1
Deduplication Rate: 25%
```

---

# Detection 010 - SLA Monitoring and Escalation

Detection 010 monitors case deadlines and changes escalation state over time.

```text
WITHIN_SLA
    |
    v
AT_RISK
    |
    v
BREACHED
```

Validation:

| Scenario | Priority | Remaining | Result |
|---|---|---:|---|
| Normal | P3 | 360 min | No Escalation |
| At Risk | P3 | 30 min | SOC Lead Warning |
| High-Priority At Risk | P2 | 30 min | Immediate SOC Lead Escalation |
| Breached | P3 | -30 min | Management Escalation |

---

# Detection 011 - Incident Risk Scoring

Detection 011 calculates an explainable incident-risk score.

Signals include:

```text
Wazuh Severity
IOC Risk
MITRE Context
Asset Criticality
Containment Status
SLA Status
Correlated Activity
```

Validation:

```text
Baseline Incident
40 / 100 -> MEDIUM

Deteriorated Incident
75 / 100 -> CRITICAL

Maximum-Risk Scenario
Raw Score: 103
Final Score: 100
Risk: CRITICAL
```

---

# Detection 012 - Incident Timeline Reconstruction

Detection 012 combines workflow events from different automation stages.

The engine:

- Parses different ISO timestamp formats
- Normalizes timestamps to UTC
- Sorts events chronologically
- Calculates event gaps
- Calculates elapsed time
- Produces JSON and Markdown timelines

Example:

```text
Security Alert
      |
      v
Triage Completed
      |
      v
Case Created
      |
      v
Notification Generated
      |
      v
Risk Assessment
```

---

# Detection 013 - Response Recommendation Engine

Detection 013 converts incident context into actionable analyst recommendations.

The engine generates:

- Investigation actions
- Containment recommendations
- Evidence-collection actions
- Escalation guidance
- Closure guidance
- Analyst summary

Example:

```text
CRITICAL Risk
+
FAILED Containment
+
AT_RISK SLA
      |
      v
IMMEDIATE Response
      |
      v
L2/L3 Escalation
```

---

# Detection 014 - SOC Metrics and Analytics

Detection 014 aggregates operational data into SOC metrics.

Generated metrics include:

- Alert count
- Incident count
- Deduplication rate
- SLA compliance
- SLA breach rate
- Average risk score
- Highest risk score
- Escalation rate
- Timeline metrics

Example test-dataset results:

```text
Alerts Processed:       4
Incidents Created:      3
Deduplication Rate:     25%

SLA Compliance Rate:    33.33%
SLA Breach Rate:        33.33%

Average Risk Score:     57.5
Highest Risk Score:     75

Escalation Rate:        66.67%
```

These are controlled validation metrics and are not presented as production SOC performance.

---

# Detection 015 - SOC Executive Reporting

Detection 015 is the final reporting layer.

It aggregates:

```text
Case Management
Incident Correlation
SLA Monitoring
Risk Scoring
Timeline Reconstruction
Response Recommendations
SOC Metrics
      |
      v
Executive Reporting
```

The final validation scenario generated:

```text
Executive Status:
CRITICAL ATTENTION REQUIRED

Risk Score:
75

Risk Level:
CRITICAL

SLA:
BREACHED

Response Urgency:
IMMEDIATE

Escalation:
Management Escalation
```

The output is generated as:

```text
executive-dashboard.json
executive-report.md
```

---

# End-to-End SOC Workflow

The completed automation architecture is:

```text
Kali Linux
Controlled Security Testing
        |
        v
Windows 11 Endpoint
        |
        v
Sysmon / Windows Logs
        |
        v
Wazuh Agent
        |
        v
Wazuh SIEM
        |
        v
Detection Engineering
        |
        v
Correlation
        |
        v
MITRE ATT&CK Mapping
        |
        v
Active Response
        |
        v
IOC Enrichment
        |
        v
Alert Triage
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
Playbook Orchestration
        |
        v
Incident Deduplication
        |
        v
SLA Monitoring
        |
        v
Risk Scoring
        |
        v
Timeline Reconstruction
        |
        v
Response Recommendations
        |
        v
SOC Metrics
        |
        v
Executive Reporting
```

---

# Repository Structure

```text
automated-soc-detection-response-lab/
|
|-- README.md
|
|-- detections/
|   |-- detection-001-network-reconnaissance/
|   |-- detection-002-network-recon-correlation/
|   |-- detection-003-ioc-enrichment/
|   |-- detection-004-automated-incident-reporting/
|   |-- detection-005-automated-alert-triage/
|   |-- detection-006-automated-case-management/
|   |-- detection-007-soc-notification-escalation/
|   |-- detection-008-playbook-orchestration/
|   |-- detection-009-incident-deduplication/
|   |-- detection-010-sla-monitoring-escalation/
|   |-- detection-011-incident-risk-scoring/
|   |-- detection-012-incident-timeline-reconstruction/
|   |-- detection-013-response-recommendation-engine/
|   |-- detection-014-soc-metrics-analytics/
|   `-- detection-015-soc-executive-reporting/
|
`-- .gitignore
```

Each detection directory contains some combination of:

```text
README.md
rules/
scripts/
evidence/
sample-output/
sample-reports/
active-response/
```

---

# Project Progress

| Area | Status |
|---|---|
| Wazuh Server Deployment | Completed |
| Windows Endpoint Integration | Completed |
| Sysmon Deployment | Completed |
| Wazuh Telemetry Validation | Completed |
| Kali Linux Attack Simulation | Completed |
| Custom Detection Engineering | Completed |
| MITRE ATT&CK Mapping | Completed |
| Wazuh Active Response | Completed |
| Automated Containment | Completed |
| IOC Enrichment | Completed |
| Automated Incident Reporting | Completed |
| Context-Aware Alert Triage | Completed |
| Automated Case Management | Completed |
| Notification & Escalation | Completed |
| SOAR-Style Playbook Orchestration | Completed |
| Incident Deduplication | Completed |
| SLA Monitoring | Completed |
| Incident Risk Scoring | Completed |
| Incident Timeline Reconstruction | Completed |
| Response Recommendation Engine | Completed |
| SOC Metrics & Analytics | Completed |
| Executive Reporting | Completed |

---

# Skills Demonstrated

The project demonstrates practical experience with:

- SOC operations
- SIEM monitoring
- Wazuh
- Sysmon
- Windows Event Logs
- Windows Firewall
- Endpoint telemetry
- Alert triage
- Incident investigation
- Threat hunting
- Detection engineering
- Log analysis
- Event correlation
- MITRE ATT&CK
- IOC analysis
- Threat intelligence
- Python automation
- PowerShell
- Automated containment
- Active Response
- Incident reporting
- Case management
- SLA monitoring
- Risk scoring
- Incident deduplication
- Timeline reconstruction
- SOAR concepts
- Security orchestration
- SOC metrics
- Executive reporting
- Git / GitHub documentation

---

# Engineering Principles Demonstrated

The project also focuses on implementation quality.

Examples include:

- Defensive JSON parsing
- Null-safe automation logic
- Secret handling through environment variables
- No API keys committed to source control
- Deterministic test scenarios
- UTC timestamp normalization
- Explainable risk calculations
- Priority-aware escalation
- Time-window correlation
- State preservation across workflow stages
- Separation of technical and management reporting

---

# Key Learning Outcomes

The project demonstrates the complete progression:

```text
What happened?
      |
      v
How was it detected?
      |
      v
Which logs provide evidence?
      |
      v
Which MITRE ATT&CK technique applies?
      |
      v
How should a SOC analyst investigate?
      |
      v
Can repetitive investigation steps be automated?
      |
      v
Should containment occur?
      |
      v
How should the case be prioritized?
      |
      v
Is the SLA healthy?
      |
      v
How risky is the incident?
      |
      v
What should the analyst do next?
      |
      v
What operational metrics can be measured?
      |
      v
How should the incident be summarized for management?
```

---

# Important Lab Interpretation

This repository represents a **controlled cybersecurity lab environment**.

Some timestamps and metrics were intentionally generated across separate development sessions.

Therefore:

- Lab timeline duration is not presented as production MTTD.
- Lab timeline duration is not presented as production MTTR.
- SLA percentages represent controlled validation scenarios.
- Escalation percentages represent test-dataset behavior.
- Risk scores demonstrate scoring logic and are not universal production risk policies.

---

# Disclaimer

This project is developed exclusively for:

- Cybersecurity education
- Defensive security research
- SOC engineering practice
- Detection engineering practice
- Incident-response automation learning

All security simulations are performed against isolated virtual machines owned and controlled by the project author.
