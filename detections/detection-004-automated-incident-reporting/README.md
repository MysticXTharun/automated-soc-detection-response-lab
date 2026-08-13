\# Detection 004 - Automated SOC Incident Reporting



\## Overview



Detection 004 extends the Automated SOC Detection \& Response Lab by converting enriched Wazuh security alerts into structured SOC incident reports.



The Python report generator consumes the output produced by the IOC enrichment workflow and automatically creates a Markdown incident report containing detection context, network information, MITRE ATT\&CK mapping, IOC enrichment results, SOC assessment, incident disposition, escalation guidance, and recommended analyst actions.



This demonstrates how detection and enrichment data can be transformed into analyst-ready incident documentation.



\---



\## Automation Pipeline



```text

Wazuh Detection

&#x20;     |

&#x20;     v

Correlated Security Alert

&#x20;     |

&#x20;     v

Alert Metadata

&#x20;     |

&#x20;     v

IOC Extraction

&#x20;     |

&#x20;     v

IOC Enrichment

&#x20;     |

&#x20;     v

SOC Risk Assessment

&#x20;     |

&#x20;     v

Incident Report Generator

&#x20;     |

&#x20;     v

Structured SOC Incident Report

```



\---



\## Related Detections



Detection 004 builds on the previous lab components:



| Detection | Function |

|---|---|

| Detection 001 | Network reconnaissance detection |

| Detection 002 | Correlation and automated containment |

| Detection 003 | IOC enrichment and SOC risk assessment |

| Detection 004 | Automated incident reporting |



\---



\## Input



The report generator accepts enriched Wazuh alert JSON produced by Detection 003.



Example:



```powershell

python incident\_report\_generator.py --input incident-100111-input.json --output incident-100111.md

```



The input contains information such as:



\- Detection timestamp

\- Wazuh rule ID

\- Wazuh rule level

\- Rule description

\- Agent information

\- Source IP

\- Destination IP

\- Destination port

\- MITRE ATT\&CK metadata

\- IOC enrichment

\- SOC assessment



\---



\## Generated Incident Report



The script automatically generates an analyst-readable Markdown incident report.



The report contains:



\- Incident ID

\- Detection timestamp

\- Report generation timestamp

\- Alert severity

\- Wazuh rule information

\- Endpoint information

\- Network context

\- MITRE ATT\&CK mapping

\- IOC enrichment

\- SOC assessment

\- Incident disposition

\- Escalation recommendation

\- Investigation summary

\- Recommended analyst actions

\- Evidence summary



\---



\## Test Scenario



The workflow was tested using the correlated reconnaissance detection from the controlled lab environment.



| Field | Value |

|---|---|

| Wazuh Rule ID | 100111 |

| Wazuh Rule Level | 10 |

| Severity | HIGH |

| Source IP | 192.168.130.141 |

| Destination IP | 192.168.130.130 |

| Destination Port | 445 |

| MITRE Technique | Network Service Discovery |

| MITRE Technique ID | T1046 |

| MITRE Tactic | Discovery |



The source system was the controlled Kali Linux testing host and the destination was the monitored Windows 11 endpoint.



\---



\## MITRE ATT\&CK Integration



MITRE metadata is not hard-coded into the incident report generator.



Instead, the information flows through the alert and enrichment pipeline:



```text

Wazuh Alert

&#x20;   |

&#x20;   v

rule.mitre

&#x20;   |

&#x20;   v

IOC Enrichment

&#x20;   |

&#x20;   v

alert\_context

&#x20;   |

&#x20;   v

Incident Report Generator

```



For the test scenario:



```text

Tactic: Discovery

Technique: Network Service Discovery

Technique ID: T1046

```



This design allows the reporting workflow to support additional detections without requiring technique-specific reporting logic.



\---



\## Severity Calculation



The report generator derives an incident severity from the Wazuh rule level.



| Wazuh Level | Report Severity |

|---|---|

| 0-3 | LOW |

| 4-7 | MEDIUM |

| 8-11 | HIGH |

| 12+ | CRITICAL |



Rule `100111` has a Wazuh level of `10`, resulting in:



```text

Severity: HIGH

```



\---



\## IOC Assessment



The source IOC was:



```text

192.168.130.141

```



The enrichment workflow determined:



```text

Classification: Private IP

Public Threat Intelligence Lookup: False

SOC Verdict: INTERNAL

Risk Level: INFO

```



Public reputation services are not applicable to private RFC1918 addresses.



\---



\## Alert Severity vs Contextual Risk



The generated report intentionally distinguishes between alert severity and contextual IOC risk.



For this incident:



```text

Alert Severity: HIGH

IOC Risk Level: INFO

```



The HIGH severity originates from the correlated Wazuh detection rule.



The INFO risk level originates from IOC enrichment, which identifies the source as an internal/private lab address.



These values represent different analytical dimensions and should not be interpreted as contradictory.



\---



\## Incident Disposition



Because the detection description identifies the event as controlled lab activity, the automated disposition was:



```text

Confirmed Lab Security Activity

```



The corresponding escalation recommendation was:



```text

No production escalation required - controlled lab activity

```



In a production environment, disposition should incorporate additional contextual evidence and analyst validation.



\---



\## Recommended Analyst Actions



The generated report recommends that the analyst:



1\. Validate whether the source system is authorized.

2\. Review related alerts from the same source IP.

3\. Review destination ports and associated services.

4\. Correlate Windows, Sysmon, and network telemetry.

5\. Confirm whether automated containment was triggered.

6\. Review related MITRE ATT\&CK activity.

7\. Escalate according to the generated recommendation.



\---



\## Evidence



The Detection 004 directory contains:



```text

evidence/

&#x20;   incident-100111-input.json



sample-reports/

&#x20;   incident-100111.md



scripts/

&#x20;   incident\_report\_generator.py

```



The JSON file represents the enriched input consumed by the reporting engine.



The Markdown file demonstrates the resulting SOC incident report.



\---



\## Security and Design Considerations



The reporting engine does not require API credentials.



Threat-intelligence enrichment occurs upstream in Detection 003.



The report generator consumes only the resulting structured JSON data.



This separation keeps the workflow modular:



```text

Detection

&#x20;   ↓

Enrichment

&#x20;   ↓

Assessment

&#x20;   ↓

Reporting

```



Each component can therefore be improved independently.



\---



\## Limitations



This implementation is designed for a controlled SOC lab.



Current limitations include:



\- Markdown output only

\- Single-event report generation

\- Simplified severity mapping

\- Rule-description-based lab disposition

\- No case-management integration

\- No ticket creation

\- No analyst assignment

\- No email or notification workflow

\- No automatic report ingestion from the Wazuh API



\---



\## Future Improvements



Future development can include:



\- HTML incident reports

\- PDF incident reports

\- Automatic Wazuh API ingestion

\- Case-management integration

\- Ticket creation

\- Analyst assignment

\- SLA tracking

\- Incident timelines

\- Multi-alert correlation

\- Automated evidence collection

\- Email or notification workflows

\- Executive incident summaries



\---



\## Learning Outcome



Detection 004 demonstrates the following workflow:



```text

Detect

&#x20; |

&#x20; v

Correlate

&#x20; |

&#x20; v

Enrich

&#x20; |

&#x20; v

Assess

&#x20; |

&#x20; v

Generate Incident

&#x20; |

&#x20; v

Document Evidence

&#x20; |

&#x20; v

Recommend Analyst Action

```



This extends the project from detection and automated response into structured SOC incident-management automation.

