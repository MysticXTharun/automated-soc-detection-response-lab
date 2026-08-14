\# Detection 006 - Automated Case Management and Incident Timeline



\## Overview



Detection 006 extends the Automated SOC Detection \& Response Lab with automated SOC case creation and incident tracking.



The case-management engine consumes the context-aware triage output produced by Detection 005 and automatically creates a structured SOC case containing:



\- Unique case ID

\- Case status

\- SOC queue assignment

\- Analyst assignment state

\- SLA

\- SLA status

\- Detection context

\- Asset context

\- IOC assessment

\- Containment status

\- Investigation summary

\- Incident timeline

\- Closure recommendation



This demonstrates how enriched and prioritized alerts can be converted into analyst-ready SOC cases.



\---



\## Case Management Pipeline



```text

Wazuh Alert

&#x20;   |

&#x20;   v

Detection and Correlation

&#x20;   |

&#x20;   v

IOC Enrichment

&#x20;   |

&#x20;   v

Alert Triage

&#x20;   |

&#x20;   v

Priority Assignment

&#x20;   |

&#x20;   v

Automated Case Creation

&#x20;   |

&#x20;   +-- Case ID

&#x20;   +-- Queue

&#x20;   +-- SLA

&#x20;   +-- Assignment State

&#x20;   +-- Timeline

&#x20;   +-- Closure Recommendation

&#x20;   |

&#x20;   v

SOC Analyst Review

```



\---



\## Related Workflow



Detection 006 builds on the previous stages:



| Detection | Function |

|---|---|

| Detection 001 | Network reconnaissance detection |

| Detection 002 | Correlation and automated containment |

| Detection 003 | IOC enrichment and SOC risk assessment |

| Detection 004 | Automated incident reporting |

| Detection 005 | Context-aware alert triage |

| Detection 006 | Automated case management |



\---



\## Test Scenario



The test case was generated from Wazuh Rule `100111`.



| Field | Value |

|---|---|

| Wazuh Rule ID | 100111 |

| Rule Level | 10 |

| Priority | P3 |

| Source IP | 192.168.130.141 |

| Destination IP | 192.168.130.130 |

| Destination Port | 445 |

| MITRE Technique | Network Service Discovery |

| MITRE ID | T1046 |

| Containment Status | SUCCESS |



\---



\## Case Generation



The engine automatically generates a unique case ID.



Example:



```text

CASE-20260814-035612-R100111

```



The format includes:



```text

CASE

\+

UTC creation timestamp

\+

Wazuh rule ID

```



\---



\## Case Status



Because automated containment succeeded, the generated case status is:



```text

Contained - Analyst Review Required

```



If containment fails, the case status becomes:



```text

Open - Containment Required

```



\---



\## Queue Assignment



Priority determines the SOC queue.



| Priority | Queue |

|---|---|

| P1 | SOC L2/L3 Escalation Queue |

| P2 | SOC High Priority Queue |

| P3 | SOC Standard Investigation Queue |

| P4 | SOC Monitoring Queue |



The lab case received:



```text

Priority: P3

Queue: SOC Standard Investigation Queue

```



\---



\## Analyst Assignment State



The automation does not invent an analyst identity.



Instead, the generated case contains:



```text

Owner: UNASSIGNED

State: Awaiting SOC Analyst Assignment

```



A production case-management platform would later assign the case to a real SOC analyst.



\---



\## SLA Management



SLA duration is derived from incident priority.



| Priority | SLA |

|---|---|

| P1 | 1 hour |

| P2 | 4 hours |

| P3 | 8 hours |

| P4 | 24 hours |



The current case received:



```text

Priority: P3

SLA: 8 hours

Status: WITHIN\_SLA

```



The engine also calculates:



\- Case creation time

\- SLA due time

\- Case age

\- Remaining SLA time

\- SLA status



Possible SLA states include:



```text

WITHIN\_SLA

AT\_RISK

BREACHED

```



\---



\## Incident Timeline



The case contains a chronological timeline.



Example:



```text

Security alert detected

&#x20;       |

&#x20;       v

Automated triage completed

&#x20;       |

&#x20;       v

Containment status evaluated

&#x20;       |

&#x20;       v

SOC case created

```



The timeline preserves the original Wazuh detection timestamp and the later automation timestamps.



\---



\## Closure Recommendation



The lab case was successfully contained and triaged as P3.



The generated closure recommendation is:



```text

Eligible for closure after analyst validation confirms no additional suspicious activity

```



If containment fails, the engine recommends keeping the case open until manual containment is completed.



\---



\## Case Output



The generated case contains:



```text

case\_id

case\_status

priority

assigned\_queue

assignment

sla

closure\_recommendation

detection

asset\_context

ioc\_assessment

containment

triage

investigation\_summary

timeline

```



\---



\## Evidence



```text

evidence/

&#x20;   case-input-100111.json



sample-cases/

&#x20;   case-100111.json



scripts/

&#x20;   case\_manager.py

```



\---



\## SOC Value



Detection 006 demonstrates how a SOC can move beyond alert generation.



Instead of stopping at:



```text

Alert generated

```



the automation continues through:



```text

Alert

&#x20; |

&#x20; v

Enrichment

&#x20; |

&#x20; v

Triage

&#x20; |

&#x20; v

Priority

&#x20; |

&#x20; v

Case Creation

&#x20; |

&#x20; v

SLA

&#x20; |

&#x20; v

Timeline

&#x20; |

&#x20; v

Analyst Assignment

```



This resembles a simplified SOAR and case-management workflow.



\---



\## Limitations



This implementation is designed for a controlled SOC lab.



Current limitations include:



\- Local JSON case storage

\- No external case-management platform

\- No analyst authentication

\- No automatic ticket updates

\- No SLA notifications

\- No persistent case database

\- No automatic closure

\- No case comments

\- No evidence attachments

\- No workflow approval process



\---



\## Future Improvements



Future versions can include:



\- TheHive integration

\- ServiceNow integration

\- Jira integration

\- Analyst assignment

\- Case comments

\- SLA notifications

\- Automatic escalation

\- Evidence attachments

\- Case state transitions

\- Persistent case storage

\- Case dashboards

\- API-driven case updates



\---



\## Learning Outcome



Detection 006 demonstrates:



```text

Detect

&#x20; |

&#x20; v

Enrich

&#x20; |

&#x20; v

Triage

&#x20; |

&#x20; v

Prioritize

&#x20; |

&#x20; v

Create Case

&#x20; |

&#x20; v

Track SLA

&#x20; |

&#x20; v

Build Timeline

&#x20; |

&#x20; v

Recommend Closure

```



This extends the project into automated SOC case management and incident lifecycle tracking.

