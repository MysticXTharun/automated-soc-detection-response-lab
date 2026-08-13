\# Automated SOC Detection \& Response Lab



A hands-on Security Operations Center (SOC) engineering lab designed to simulate a real-world detection and response environment using \*\*Wazuh, Sysmon, Windows 11, Kali Linux, and Python automation\*\*.



The project progresses from endpoint telemetry collection and SIEM monitoring to \*\*threat detection, investigation, custom detection engineering, IOC enrichment, and automated incident response\*\*.



> \*\*Current Status:\*\* Phase 1 completed — Wazuh, Windows 11 endpoint monitoring, Sysmon telemetry, and SIEM visibility are operational.



\---



\## Project Objective



The objective of this project is to build an end-to-end SOC workflow:



```text

Kali Linux

Attack Simulation

&#x20;     │

&#x20;     ▼

Windows 11 Endpoint

&#x20;     │

&#x20;     ▼

Sysmon Telemetry

&#x20;     │

&#x20;     ▼

Wazuh Agent

&#x20;     │

&#x20;     ▼

Wazuh Manager / SIEM

&#x20;     │

&#x20;     ▼

Detection \& Investigation

&#x20;     │

&#x20;     ▼

Custom Detection Rules

&#x20;     │

&#x20;     ▼

SOC Automation

&#x20;     │

&#x20;     ├── IOC Enrichment

&#x20;     ├── Risk Evaluation

&#x20;     ├── Automated Response

&#x20;     └── Incident Documentation

```



The final goal is to demonstrate how a SOC analyst can move from \*\*manual alert investigation to automated detection and response workflows\*\*.



\---



\## Lab Architecture



| System | Purpose | Lab IP |

|---|---|---|

| Ubuntu Server | Wazuh Manager / SIEM | `192.168.130.129` |

| Windows 11 Enterprise | Monitored endpoint | `192.168.130.130` |

| Kali Linux | Controlled attack simulation | `192.168.130.141` |



\### Security Stack



| Technology | Purpose |

|---|---|

| Wazuh 4.14.7 | SIEM / XDR / Detection |

| Sysmon 15.21 | Advanced Windows telemetry |

| Windows Event Logs | Endpoint security events |

| Kali Linux | Controlled security simulations |

| Python | SOC automation — upcoming |

| MITRE ATT\&CK | Detection mapping — upcoming |

| Wazuh Active Response | Automated containment — upcoming |



\---



\# Phase 1 — Wazuh Server Deployment



Wazuh was deployed on an Ubuntu Server VM to provide centralized:



\- Security monitoring

\- Log collection

\- Threat detection

\- Endpoint visibility

\- Security Configuration Assessment

\- File Integrity Monitoring

\- Threat hunting



The Wazuh dashboard was successfully deployed and made accessible over HTTPS.



\---



\# Phase 2 — Windows 11 Endpoint Integration



A Windows 11 Enterprise VM was configured as the monitored endpoint.



Before agent deployment, connectivity to the Wazuh Manager was verified.



```powershell

Test-NetConnection 192.168.130.129 -Port 1514

Test-NetConnection 192.168.130.129 -Port 1515

```



Both connections were successful.



The Wazuh agent was then installed on Windows 11.



\### Troubleshooting



During deployment, the Wazuh service installed successfully but immediately stopped.



The agent log was investigated:



```powershell

Get-Content "C:\\Program Files (x86)\\ossec-agent\\ossec.log" -Tail 30

```



The following error was identified:



```text

Invalid server address found: '0.0.0.0'

No client configured. Exiting.

```



\### Root Cause



The Wazuh agent did not have the correct manager address configured.



\### Resolution



The manager address inside `ossec.conf` was changed to:



```xml

<address>192.168.130.129</address>

```



The Wazuh service was restarted:



```powershell

Start-Service wazuhsvc

```



Service verification:



```powershell

Get-Service wazuhsvc

```



Result:



```text

Status   Name       DisplayName

\------   ----       -----------

Running  wazuhsvc   Wazuh

```



The agent subsequently enrolled successfully and received a valid authentication key.



\---



\## Wazuh Endpoint Status



```text

Agent ID       : 001

Status         : Active

IP Address     : 192.168.130.130

Wazuh Version  : 4.14.7

Operating OS   : Windows 11 Enterprise Evaluation

```



This confirmed:



```text

Windows 11

&#x20;   │

&#x20;   │ Wazuh Agent

&#x20;   ▼

Wazuh Manager

&#x20;   │

&#x20;   ▼

Wazuh Dashboard

```



\---



\# Phase 3 — Sysmon Deployment



Microsoft Sysinternals \*\*Sysmon\*\* was installed to provide enhanced endpoint telemetry beyond standard Windows event logging.



Sysmon was installed using:



```powershell

.\\Sysmon64.exe -accepteula -i

```



Service status was verified:



```powershell

Get-Service Sysmon64

```



Result:



```text

Running  Sysmon64

```



\---



\# Phase 4 — Sysmon → Wazuh Integration



The Wazuh agent was configured to collect the Sysmon Operational event channel.



The following configuration was added to the Windows Wazuh agent configuration:



```xml

<localfile>

&#x20; <location>Microsoft-Windows-Sysmon/Operational</location>

&#x20; <log\_format>eventchannel</log\_format>

</localfile>

```



The Wazuh agent was restarted:



```powershell

Restart-Service wazuhsvc

```



Both services were verified:



```powershell

Get-Service wazuhsvc

Get-Service \*sysmon\*

```



Result:



```text

Wazuh Agent  → Running

Sysmon       → Running

```



\---



\# Phase 5 — SOC-Focused Sysmon Configuration



A SOC-focused Sysmon configuration was applied to improve endpoint visibility.



The configuration was applied using:



```powershell

.\\Sysmon64.exe -c .\\sysmonconfig-export.xml

```



Sysmon remained operational after the configuration update.



\---



\## Telemetry Validation



Sysmon events were queried directly from the Windows endpoint:



```powershell

Get-WinEvent -LogName "Microsoft-Windows-Sysmon/Operational" -MaxEvents 20 |

Select-Object TimeCreated, Id

```



Multiple event types were successfully generated.



| Event ID | Sysmon Event | SOC Value |

|---:|---|---|

| 1 | Process Creation | Detect suspicious process execution |

| 3 | Network Connection | Monitor outbound/inbound connections |

| 8 | CreateRemoteThread | Identify possible process injection |

| 22 | DNS Query | Detect suspicious domain resolution |



Example telemetry observed:



```text

Event ID 22

Event ID 8

Event ID 3

Event ID 1

```



\---



\# Phase 6 — Wazuh Detection Validation



Sysmon and Windows telemetry successfully reached the Wazuh platform.



Events were validated through:



```text

Wazuh Dashboard

&#x20;     ↓

Threat Intelligence

&#x20;     ↓

Threat Hunting

&#x20;     ↓

Agent ID: 001

```



Wazuh successfully generated detections related to endpoint activity, including discovery and PowerShell-related activity.



This confirmed the complete telemetry pipeline:



```text

Windows Activity

&#x20;     │

&#x20;     ▼

Sysmon

&#x20;     │

&#x20;     ▼

Windows Event Channel

&#x20;     │

&#x20;     ▼

Wazuh Agent

&#x20;     │

&#x20;     ▼

Wazuh Manager

&#x20;     │

&#x20;     ▼

Detection Rules

&#x20;     │

&#x20;     ▼

Threat Hunting

```



\---



\# Phase 7 — Kali Linux Preparation



Kali Linux is being configured as the controlled adversary simulation machine.



```text

Kali Linux IP:

192.168.130.141

```



Connectivity between Kali and the Wazuh server has been successfully verified.



```text

Kali Linux

192.168.130.141

&#x20;     │

&#x20;     ├──────────────► Wazuh

&#x20;     │                192.168.130.129

&#x20;     │

&#x20;     └──────────────► Windows 11

&#x20;                      192.168.130.130

```



Windows connectivity validation and controlled security simulations are the next stage.



\---



\# SOC Automation Roadmap



The automation portion will be introduced progressively so that every stage can be understood and investigated manually before it is automated.



\### Stage 1 — Detection



```text

Security Activity

&#x20;     ↓

Sysmon

&#x20;     ↓

Wazuh Detection

```



\### Stage 2 — Investigation



Extract information such as:



```text

Source IP

Destination IP

Username

Process

Command Line

File Hash

Domain

Event ID

MITRE Technique

```



\### Stage 3 — IOC Enrichment



Python automation will enrich indicators using threat-intelligence sources.



```text

Wazuh Alert

&#x20;     ↓

Extract IOC

&#x20;     ↓

Threat Intelligence Lookup

&#x20;     ↓

Reputation / Context

```



\### Stage 4 — Risk Decision



Automation will evaluate factors such as:



```text

Alert Severity

&#x20;     +

IOC Reputation

&#x20;     +

Detection Context

&#x20;     +

Repeated Activity

&#x20;     ↓

Risk Decision

```



\### Stage 5 — Automated Response



Approved lab scenarios will trigger Wazuh Active Response.



Example:



```text

Malicious Activity Detected

&#x20;         ↓

Wazuh Alert

&#x20;         ↓

IOC Enrichment

&#x20;         ↓

Risk Threshold Met

&#x20;         ↓

Active Response

&#x20;         ↓

Block Source IP

```



\### Stage 6 — Incident Documentation



The final automation workflow will generate structured investigation information:



```text

Incident ID

Detection Time

Affected Endpoint

Source IP

Detection Rule

MITRE ATT\&CK Technique

IOC Reputation

Response Action

Final Status

```



\---



\# Planned Detection Scenarios



The lab will progressively implement controlled scenarios such as:



\- Network reconnaissance

\- Authentication failures

\- Suspicious PowerShell execution

\- Abnormal process execution

\- DNS-based indicators

\- File integrity changes

\- Suspicious outbound connections

\- Credential-access indicators

\- Persistence-related activity

\- Process injection indicators



Each scenario will follow:



```text

Simulate

&#x20;  ↓

Detect

&#x20;  ↓

Investigate

&#x20;  ↓

Map to MITRE ATT\&CK

&#x20;  ↓

Create/Improve Detection

&#x20;  ↓

Automate

&#x20;  ↓

Validate Response

```



\---



\# Repository Structure



```text

automated-soc-detection-response-lab/

│

├── README.md

│

├── docs/

│

├── screenshots/

│

├── detections/

│

├── automation/

│

├── active-response/

│

├── attack-simulations/

│

└── incident-reports/

```



\### `docs/`



Architecture, installation notes, troubleshooting, and technical documentation.



\### `detections/`



Custom Wazuh detection rules and MITRE ATT\&CK mappings.



\### `automation/`



Python-based SOC automation and IOC enrichment scripts.



\### `active-response/`



Automated containment and Wazuh Active Response configurations.



\### `attack-simulations/`



Controlled lab scenarios used to validate detections.



\### `incident-reports/`



Example SOC investigation reports generated from lab scenarios.



\### `screenshots/`



Evidence showing alerts, telemetry, detections, and automated response results.



\---



\# Skills Demonstrated



This project is designed to demonstrate practical experience with:



\- Security Operations Center workflows

\- SIEM monitoring

\- Wazuh

\- Windows endpoint monitoring

\- Sysmon

\- Windows Event Logs

\- Alert triage

\- Incident investigation

\- Threat hunting

\- Detection engineering

\- Log analysis

\- Event correlation

\- MITRE ATT\&CK

\- IOC analysis

\- Python security automation

\- Wazuh Active Response

\- Automated incident response

\- SOC documentation



\---



\# Current Project Status



| Phase | Status |

|---|---|

| Wazuh Server Deployment | Completed |

| Windows 11 Agent Integration | Completed |

| Sysmon Installation | Completed |

| Sysmon → Wazuh Integration | Completed |

| SOC-Focused Sysmon Configuration | Completed |

| Wazuh Telemetry Validation | Completed |

| Kali Linux Preparation | In Progress |

| Attack Simulations | Planned |

| Custom Detection Rules | Planned |

| MITRE ATT\&CK Mapping | Planned |

| Python SOC Automation | Planned |

| IOC Enrichment | Planned |

| Wazuh Active Response | Planned |

| Automated Incident Reporting | Planned |



\---



\# Learning Outcome



This project focuses on understanding the complete SOC lifecycle rather than simply executing tools.



For every detection scenario, the objective is to understand:



\*\*What happened? → Why was it detected? → Which logs prove it? → How would a SOC analyst investigate it? → How can the detection be improved? → Which parts can safely be automated?\*\*



\---



\## Disclaimer



This project is built exclusively for \*\*cybersecurity education, defensive security research, and SOC engineering practice\*\*.



All security testing is performed against isolated virtual machines owned and controlled by the project author. No techniques demonstrated in this repository are intended for unauthorized systems.

