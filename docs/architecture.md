# Automated SOC Detection & Response Lab - Architecture

## Architecture Overview

The lab implements a layered SOC architecture progressing from telemetry collection and detection to automated response, orchestration, analytics, and executive reporting.

```text

+-----------------------------+
| Kali Linux                  |
| Controlled Attack Simulator |
| 192.168.130.141             |
+--------------+--------------+
               |
               v
+-----------------------------+
| Windows 11 Endpoint         |
| 192.168.130.130             |
|                             |
| Sysmon                      |
| Windows Event Logs          |
| Wazuh Agent                 |
| Windows Firewall            |
+--------------+--------------+
               |
               | Security Telemetry
               v
+-----------------------------+
| Wazuh SIEM / XDR            |
| Ubuntu Server               |
| 192.168.130.129             |
|                             |
| Wazuh Manager               |
| Wazuh Indexer               |
| Wazuh Dashboard             |
| Detection Rules             |
+--------------+--------------+
               |
               v
+-----------------------------+
| Detection Engineering       |
|                             |
| D001 - Recon Detection      |
| D002 - Correlation          |
+--------------+--------------+
               |
       +-------+-------+
       |               |
       v               v
+----------------+  +----------------+
| Response       |  | Investigation  |
|                |  |                |
| Active Response|  | Alert Analysis |
| Firewall       |  | MITRE ATT&CK   |
| IP Containment |  | SOC Context    |
+-------+--------+  +-------+--------+
        |                   |
        +---------+---------+
                  |
                  v
+-----------------------------------+
| SOC Automation                    |
|                                   |
| D003 - IOC Enrichment             |
| D004 - Incident Reporting         |
| D005 - Alert Triage               |
| D006 - Case Management            |
| D007 - Notification / Escalation  |
+----------------+------------------+
                 |
                 v
+-----------------------------------+
| Orchestration                     |
|                                   |
| D008 - SOC Playbook Orchestration |
+----------------+------------------+
                 |
                 v
+-----------------------------------+
| Incident Intelligence             |
|                                   |
| D009 - Incident Deduplication     |
| D010 - SLA Monitoring             |
| D011 - Incident Risk Scoring      |
| D012 - Timeline Reconstruction    |
| D013 - Response Recommendations   |
+----------------+------------------+
                 |
                 v
+-----------------------------------+
| SOC Analytics                     |
|                                   |
| D014 - SOC Metrics & Analytics    |
+----------------+------------------+
                 |
                 v
+-----------------------------------+
| Management Reporting              |
|                                   |
| D015 - SOC Executive Reporting    |
| Executive Dashboard JSON          |
| Executive Markdown Report         |
+-----------------------------------+

```text
---

## SOC Data Flow

The primary data flow is:

```text

Attack Simulation

      |

      v

Endpoint Activity

      |

      v

Telemetry Collection

      |

      v

SIEM Detection

      |

      v

Correlation

      |

      v

Containment

      |

      v

Enrichment

      |

      v

Triage

      |

      v

Incident Report

      |

      v

SOC Case

      |

      v

Notification / Escalation

      |

      v

Playbook Orchestration

      |

      v

Incident Correlation

      |

      v

SLA Evaluation

      |

      v

Risk Assessment

      |

      v

Timeline Reconstruction

      |

      v

Response Recommendation

      |

      v

SOC Analytics

      |

      v

Executive Reporting

```

---

## Architecture Layers

| Layer | Components | Purpose |

|---|---|---|

| Attack Simulation | Kali Linux | Generate controlled security activity |

| Endpoint | Windows 11, Sysmon | Generate endpoint telemetry |

| Collection | Wazuh Agent | Forward security telemetry |

| SIEM | Wazuh | Detection, correlation and investigation |

| Detection | D001-D002 | Identify and correlate suspicious activity |

| Response | Active Response, Windows Firewall | Automated containment |

| Automation | D003-D007 | Enrichment, triage, reporting and case handling |

| Orchestration | D008 | Execute SOC automation as one workflow |

| Incident Intelligence | D009-D013 | Correlation, SLA, risk, timeline and recommendations |

| Analytics | D014 | Generate SOC operational metrics |

| Reporting | D015 | Produce management-level reporting |

---

## Detection Dependency Flow

```text

D001

Network Reconnaissance Detection

|

v

D002

Correlation + Active Response

|

v

D003

IOC Enrichment

|

v

D005

Automated Alert Triage

|

+----------------+

|                |

v                v

D004             D006

Incident         Case

Reporting        Management

                 |

                 v

                D007

                Notification

                & Escalation

D003-D007

   |

   v

D008

Playbook Orchestration

D008

|

+----------+

|          |

v          v

D009       D010

Incident   SLA

Dedup      Monitoring

|          |

+----+-----+

     |

     v

D011

Risk Scoring

     |

     v

D012

Timeline Reconstruction

     |

     v

D013

Response Recommendations

     |

     v

D014

SOC Metrics

     |

     v

D015

Executive Reporting

```

---

## Design Principles

The lab follows several SOC engineering principles:

- Detection before automation

- Context-aware triage

- Explainable scoring

- Evidence preservation

- Controlled automated response

- Separation of detection and response logic

- Deterministic testing

- Structured JSON communication between components

- UTC timestamp normalization

- Priority-aware escalation

- SLA-aware incident handling

- Historical state preservation

- Management reporting separated from technical evidence

---

## Security Boundary

All attack simulations are performed inside an isolated lab environment.

```text

Kali Linux

    |

    | Controlled Security Testing

    v

Windows Lab Endpoint

    |

    | Security Telemetry

    v

Wazuh Lab Server

```

No production endpoints or third-party systems are targeted.

---

## Final Architecture Outcome

The completed project demonstrates the transition from:

```text

Traditional SIEM Monitoring

         |

         v

Detection Engineering

         |

         v

Automated Investigation

         |

         v

Automated Response

         |

         v

SOAR-Style Orchestration

         |

         v

Incident Intelligence

         |

         v

SOC Analytics

         |

         v

Executive Reporting

```

The architecture is intentionally modular so individual components can be tested independently while still participating in the complete SOC workflow.



