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

Yes    No

|     |

v     v

Correlate   Create New

Alert       Incident

```



---



## Correlation Fields



The engine generates a deterministic correlation key using:



```text

Rule ID

\+

Source IP

\+

Destination IP

\+

Destination Port

\+

MITRE Technique ID

```



For the primary reconnaissance activity:



```text

Rule ID: 100111

Source IP: 192.168.130.141

Destination IP: 192.168.130.130

Destination Port: 445

MITRE ID: T1046

```



Alerts containing the same correlation fields generate the same correlation key.



---



## Correlation Window



The lab uses a default correlation window of:



```text

5 minutes

```



An alert with matching correlation fields is attached to an existing incident only when it occurs within the configured correlation window.



The window can be changed using:



```text

--window <minutes>

```



---



## Test Scenarios



Four alerts were used to validate the correlation logic.



| Alert | Source IP | Activity | Expected Decision |

|---|---|---|---|

| Alert 001 | 192.168.130.141 | Initial reconnaissance | NEW |

| Alert 002 | 192.168.130.141 | Repeated activity within 5 minutes | CORRELATED |

| Alert 003 | 192.168.130.150 | Same detection from different source | NEW |

| Alert 004 | 192.168.130.141 | Same activity outside 5-minute window | NEW |



---



## Scenario 1 - Initial Alert



Timestamp:



```text

2026-08-13T05:14:03.915+00:00

```



Source:



```text

192.168.130.141

```



No existing matching incident is available.



Result:



```text

Decision: NEW

Incident ID: INC-20260813-051403-8E6ED3A1

```



A new incident is created.



---



## Scenario 2 - Duplicate Activity Within Correlation Window



Timestamp:



```text

2026-08-13T05:17:41.250+00:00

```



Source:



```text

192.168.130.141

```



The alert matches the original correlation fields and occurs approximately:



```text

3.62 minutes

```



after the previous matching alert.



Result:



```text

Decision: CORRELATED

Incident ID: INC-20260813-051403-8E6ED3A1

```



The second alert receives the same incident ID as the original alert.



This demonstrates successful incident deduplication.



---



## Scenario 3 - Different Source



Timestamp:



```text

2026-08-13T05:19:12.500+00:00

```



Source:



```text

192.168.130.150

```



Although the Wazuh rule, destination, destination port, and MITRE technique are the same, the source IP is different.



Result:



```text

Decision: NEW

Incident ID: INC-20260813-051912-7FB01649

```



A separate incident is created.



---



## Scenario 4 - Outside Correlation Window



Timestamp:



```text

2026-08-13T05:30:00.000+00:00

```



Source:



```text

192.168.130.141

```



The security activity contains the same correlation fields as the original incident.



However, the activity occurs outside the configured 5-minute correlation window.



Result:



```text

Decision: NEW

Incident ID: INC-20260813-053000-8E6ED3A1

```



The correlation-key suffix remains the same because the security attributes match, but a new incident is created because the correlation window has expired.



---



## Validation Results



| Timestamp | Source IP | Decision | Incident |

|---|---|---|---|

| 05:14:03 | 192.168.130.141 | NEW | INC-20260813-051403-8E6ED3A1 |

| 05:17:41 | 192.168.130.141 | CORRELATED | INC-20260813-051403-8E6ED3A1 |

| 05:19:12 | 192.168.130.150 | NEW | INC-20260813-051912-7FB01649 |

| 05:30:00 | 192.168.130.141 | NEW | INC-20260813-053000-8E6ED3A1 |



Overall result:



```text

Alerts Processed: 4

Incidents Created: 3

Duplicates Correlated: 1

```



---



## Incident Tracking



Each incident maintains:



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



When another matching alert is correlated, the engine updates:



```text

last_seen

alert_count

related_alert_timestamps

```



This allows multiple related alerts to be represented as a single SOC incident.



---



## Example Correlated Incident



The first two alerts are represented as one incident:



```text

Incident ID:

INC-20260813-051403-8E6ED3A1



Source:

192.168.130.141



First Seen:

2026-08-13T05:14:03.915+00:00



Last Seen:

2026-08-13T05:17:41.250+00:00



Alert Count:

2

```



Instead of generating two independent incidents, the repeated activity is grouped into one investigation context.



---



## SOC Value



Without deduplication:



```text

Alert 1 --> Incident 1

Alert 2 --> Incident 2

Alert 3 --> Incident 3

Alert 4 --> Incident 4

```



With correlation:



```text

Alert 1 --------+

               |

Alert 2 --------+--> Incident 1



Alert 3 ------------> Incident 2



Alert 4 ------------> Incident 3

```



This reduces unnecessary duplicate incidents while preserving genuinely separate activity.



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

- No Wazuh API ingestion



---



## Future Improvements



Future versions can include:



- Persistent incident storage

- Wazuh API ingestion

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



Detection 009 demonstrates:



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

Compare Existing Incidents

   |

   v

Evaluate Time Window

   |

   +----------------+

   |                |

   v                v

Correlate          Create

Duplicate          New Incident

   |                |

   +-------+--------+

           |

           v

    Incident Dataset

```



This adds automated alert deduplication and time-based incident correlation to the SOC automation workflow.


