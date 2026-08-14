\# SOC Lab Evidence Index



\## Overview



This document provides a centralized index of technical evidence generated throughout the Automated SOC Detection \& Response Lab.



Evidence includes Wazuh alerts, detection results, IOC enrichment, automated triage, incident reports, case-management records, orchestration outputs, SLA evaluations, risk assessments, timelines, response recommendations, SOC metrics, and executive reporting.



\---



\## Detection Evidence



| Detection | Capability | Primary Evidence |

|---|---|---|

| D001 | Network Reconnaissance Detection | Wazuh detection and rule validation |

| D002 | Correlation \& Active Response | Correlated alert and containment evidence |

| D003 | IOC Enrichment | Enrichment JSON and risk assessment |

| D004 | Incident Reporting | Generated SOC incident report |

| D005 | Automated Alert Triage | Triage scoring and priority output |

| D006 | Case Management | Structured SOC case |

| D007 | Notification \& Escalation | Notification and escalation decisions |

| D008 | Playbook Orchestration | Complete orchestration artifacts |

| D009 | Incident Deduplication | Correlation and incident grouping results |

| D010 | SLA Monitoring | WITHIN\_SLA, AT\_RISK and BREACHED results |

| D011 | Risk Scoring | Baseline, deteriorated and maximum-risk results |

| D012 | Timeline Reconstruction | JSON and Markdown incident timelines |

| D013 | Response Recommendations | Context-aware response recommendations |

| D014 | SOC Metrics | SOC metrics JSON and Markdown report |

| D015 | Executive Reporting | Executive dashboard and management report |



\---



\## End-to-End Evidence Chain



```text

Security Activity

&#x20;     |

&#x20;     v

Wazuh Detection

&#x20;     |

&#x20;     v

Correlation

&#x20;     |

&#x20;     v

Automated Containment

&#x20;     |

&#x20;     v

IOC Enrichment

&#x20;     |

&#x20;     v

Alert Triage

&#x20;     |

&#x20;     v

Incident Report

&#x20;     |

&#x20;     v

SOC Case

&#x20;     |

&#x20;     v

Notification / Escalation

&#x20;     |

&#x20;     v

Playbook Execution

&#x20;     |

&#x20;     v

Incident Deduplication

&#x20;     |

&#x20;     v

SLA Evaluation

&#x20;     |

&#x20;     v

Risk Assessment

&#x20;     |

&#x20;     v

Timeline Reconstruction

&#x20;     |

&#x20;     v

Response Recommendation

&#x20;     |

&#x20;     v

SOC Metrics

&#x20;     |

&#x20;     v

Executive Report

```



\---



\## Key Validation Results



\### Incident Deduplication



```text

Alerts Processed:      4

Incidents Created:     3

Duplicates Correlated: 1

Deduplication Rate:    25%

```



\### SLA Monitoring



```text

Within SLA:

Remaining Time = 360 minutes

Escalation = False



At Risk:

Remaining Time = 30 minutes

Escalation = SOC Lead Warning



Breached:

Remaining Time = -30 minutes

Escalation = Management Escalation

```



\### Incident Risk Scoring



```text

Baseline:

Risk Score = 40

Risk Level = MEDIUM



Deteriorated:

Risk Score = 75

Risk Level = CRITICAL



Maximum Risk:

Risk Score = 100

Risk Level = CRITICAL

```



\### Executive Reporting



```text

Risk Score:        75

Risk Level:        CRITICAL

SLA Status:        BREACHED

Response Urgency:  IMMEDIATE

Escalation:        Management Escalation

```



\---



\## Evidence Philosophy



The repository preserves intermediate artifacts instead of presenting only final results.



This makes it possible to trace:



```text

Input

&#x20;|

&#x20;v

Processing

&#x20;|

&#x20;v

Decision

&#x20;|

&#x20;v

Response

&#x20;|

&#x20;v

Final Reporting

```



This approach provides an auditable evidence chain and demonstrates how each automation component contributes to the final SOC decision.



\---



\## Important Interpretation



All evidence was generated inside a controlled cybersecurity lab.



Metrics, timestamps, risk scores, SLA states, and escalation rates are validation data used to demonstrate automation behavior.



They should not be interpreted as production SOC performance measurements.

