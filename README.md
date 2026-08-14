# Automated SOC Detection & Response Lab

A hands-on Security Operations Center (SOC) engineering lab designed to simulate a real-world detection and response environment using Wazuh, Sysmon, Windows 11, Kali Linux, and Python automation.

The project progresses from endpoint telemetry collection and SIEM monitoring to threat detection, investigation, custom detection engineering, IOC enrichment, and automated incident response.

Current Status: Wazuh, Windows 11 endpoint monitoring, Sysmon telemetry, and SIEM visibility are operational. Kali Linux preparation is currently in progress.

---

## Project Objective

The objective of this project is to build an end-to-end SOC detection, investigation, and automated response environment.

```text
Kali Linux
Attack Simulation
      |
      v
Windows 11 Endpoint
      |
      v
Sysmon Telemetry
      |
      v
Wazuh Agent
      |
      v
Wazuh Manager / SIEM
      |
      v
Detection & Investigation
      |
      v
Custom Detection Rules
      |
      v
SOC Automation
      |
      +---- IOC Enrichment
      |
      +---- Risk Evaluation
      |
      +---- Automated Response
      |
      +---- Incident Documentation
```

The final objective is to progress from manual SOC investigation to automated detection and response workflows.

---

## Lab Architecture

| Component | Purpose | Lab IP |
|---|---|---|
| Ubuntu Server | Wazuh Manager / SIEM | 192.168.130.129 |
| Windows 11 Enterprise | Monitored Endpoint | 192.168.130.130 |
| Kali Linux | Controlled Attack Simulation | 192.168.130.141 |

## Security Stack

| Technology | Purpose |
|---|---|
| Wazuh 4.14.7 | SIEM, XDR and threat detection |
| Sysmon 15.21 | Advanced Windows endpoint telemetry |
| Windows Event Logs | Endpoint security events |
| Kali Linux | Controlled security simulations |
| Python | SOC automation - upcoming |
| MITRE ATT&CK | Detection mapping - upcoming |
| Wazuh Active Response | Automated containment - upcoming |

---

# Phase 1 - Wazuh Server Deployment

Wazuh was deployed on an Ubuntu Server virtual machine.

The Wazuh server provides centralized capabilities for:

Security monitoring

Log collection

Threat detection

Endpoint visibility

File Integrity Monitoring

Security Configuration Assessment

Threat hunting

The Wazuh Dashboard was successfully deployed and made accessible over HTTPS.

---

# Phase 2 - Windows 11 Endpoint Integration

A Windows 11 Enterprise virtual machine was configured as the monitored endpoint.

Before deploying the Wazuh agent, connectivity between Windows 11 and the Wazuh Manager was verified.

```powershell
Test-NetConnection 192.168.130.129 -Port 1514
Test-NetConnection 192.168.130.129 -Port 1515
```

Both connectivity tests returned:

```text
TcpTestSucceeded : True
```

The Wazuh Windows agent was then installed.

## Agent Troubleshooting

During initial deployment, the Wazuh service installed successfully but would not remain running.

The Wazuh agent log was investigated using:

```powershell
Get-Content "C:\Program Files (x86)\ossec-agent\ossec.log" -Tail 30
```

The following error was discovered:

```text
Invalid server address found: '0.0.0.0'
No client configured. Exiting.
```

## Root Cause

The Wazuh agent did not contain the correct Wazuh Manager address.

The manager address was corrected to:

```text
192.168.130.129
```

The Wazuh service was then started:

```powershell
Start-Service wazuhsvc
```

Service status was verified:

```powershell
Get-Service wazuhsvc
```

Result:

```text
Status   Name       DisplayName
Running  wazuhsvc   Wazuh
```

The agent successfully enrolled with the Wazuh Manager and received a valid authentication key.

## Wazuh Endpoint Status

```text
Agent ID       : 001
Status         : Active
IP Address     : 192.168.130.130
Wazuh Version  : 4.14.7
Operating OS   : Windows 11 Enterprise Evaluation
```

This successfully established:

```text
Windows 11 Endpoint
        |
        | Wazuh Agent
        v
Wazuh Manager
        |
        v
Wazuh Dashboard
```

---

# Phase 3 - Sysmon Deployment

Microsoft Sysinternals Sysmon was installed on the Windows 11 endpoint to provide enhanced endpoint telemetry.

Sysmon was installed using:

```powershell
.\Sysmon64.exe -accepteula -i
```

The Sysmon service was verified:

```powershell
Get-Service Sysmon64
```

Result:

```text
Status   Name
Running  Sysmon64
```

---

# Phase 4 - Sysmon Integration with Wazuh

The Wazuh Windows agent was configured to collect events from the Sysmon Operational event channel.

The following configuration was added to the Wazuh agent configuration:

```xml
<localfile>
  <location>Microsoft-Windows-Sysmon/Operational</location>
  <log_format>eventchannel</log_format>
</localfile>
```

The Wazuh agent was restarted:

```powershell
Restart-Service wazuhsvc
```

Both services were verified:

```powershell
Get-Service wazuhsvc
Get-Service Sysmon64
```

Result:

```text
Wazuh Agent : Running
Sysmon64    : Running
```

---

# Phase 5 - SOC-Focused Sysmon Configuration

A SOC-focused Sysmon configuration was applied to improve endpoint visibility and collect security-relevant telemetry.

The configuration was applied using:

```powershell
.\Sysmon64.exe -c .\sysmonconfig-export.xml
```

Sysmon continued running successfully after the configuration update.

## Telemetry Validation

Sysmon events were queried directly from Windows:

```powershell
Get-WinEvent -LogName "Microsoft-Windows-Sysmon/Operational" -MaxEvents 20 |
Select-Object TimeCreated, Id
```

The following Sysmon events were observed:

| Event ID | Event | SOC Purpose |
|---|---|---|
| 1 | Process Creation | Monitor process execution |
| 3 | Network Connection | Monitor network connections |
| 8 | CreateRemoteThread | Identify possible process injection |
| 22 | DNS Query | Monitor domain resolution |

This confirmed that the enhanced Sysmon configuration was successfully generating security telemetry.

---

# Phase 6 - Wazuh Detection Validation

Sysmon and Windows telemetry successfully reached the Wazuh platform.

Events were validated through the Wazuh Threat Hunting interface using Windows agent ID 001.

Wazuh generated detections related to endpoint activity, including discovery and PowerShell-related activity.

The complete telemetry pipeline is now operational:

```text
Windows Activity
      |
      v
Sysmon
      |
      v
Windows Event Logs
      |
      v
Wazuh Agent
      |
      v
Wazuh Manager
      |
      v
Detection Rules
      |
      v
Threat Hunting Dashboard
```

---

# Phase 7 - Kali Linux Preparation

Kali Linux is being configured as the controlled security-testing system.

Current Kali Linux lab IP:

```text
192.168.130.141
```

Connectivity between Kali Linux and the Wazuh server has been successfully verified.

Current lab architecture:

```text
              Wazuh Server
            192.168.130.129
                   ^
                   |
             Security Logs
                   |
             Windows 11
            192.168.130.130
             Wazuh + Sysmon
                   ^
                   |
          Controlled Testing
                   |
              Kali Linux
            192.168.130.141
```

Kali-to-Windows connectivity validation is the next step.

---

# SOC Automation Roadmap

The automation portion of the project will be introduced progressively.

The purpose is to first understand how an analyst manually detects and investigates an incident before automating the repetitive portions.

## Stage 1 - Detection

```text
Security Activity
      |
      v
Sysmon
      |
      v
Wazuh Detection
```

## Stage 2 - Investigation

Important information will be extracted from alerts, including:

```text
Source IP
Destination IP
Username
Process Name
Command Line
File Hash
Domain
Event ID
Alert Severity
MITRE ATT&CK Technique
```

## Stage 3 - IOC Enrichment

Python automation will later process indicators extracted from Wazuh alerts.

```text
Wazuh Alert
      |
      v
Extract IOC
      |
      v
Threat Intelligence Enrichment
      |
      v
Reputation and Context
```

## Stage 4 - Risk Evaluation

The automation workflow will evaluate information such as:

```text
Alert Severity
      +
IOC Reputation
      +
Detection Context
      +
Repeated Activity
      |
      v
Risk Decision
```

## Stage 5 - Automated Response

Approved lab scenarios will eventually trigger Wazuh Active Response.

Example workflow:

```text
Suspicious Activity
       |
       v
Wazuh Detection
       |
       v
IOC Enrichment
       |
       v
Risk Evaluation
       |
       v
Response Decision
       |
       v
Wazuh Active Response
       |
       v
Containment
```

## Stage 6 - Incident Documentation

The final automation workflow will create structured incident information such as:

```text
Incident ID
Detection Time
Affected Endpoint
Source IP
Detection Rule
MITRE ATT&CK Technique
IOC Reputation
Response Action
Final Status
```

---

# Planned Detection Scenarios

The following controlled scenarios will be developed throughout the project:

Network reconnaissance

Authentication failures

Suspicious PowerShell activity

Abnormal process execution

Suspicious DNS activity

File integrity changes

Suspicious network connections

Persistence-related activity

Process injection indicators

Each scenario will follow the same SOC lifecycle:

```text
Simulate
   |
   v
Detect
   |
   v
Investigate
   |
   v
MITRE ATT&CK Mapping
   |
   v
Improve Detection
   |
   v
Automate
   |
   v
Validate Response
```

---

# Repository Structure

```text
automated-soc-detection-response-lab/
|
|-- README.md
|
|-- docs/
|
|-- screenshots/
|
|-- detections/
|
|-- automation/
|
|-- active-response/
|
|-- attack-simulations/
|
`-- incident-reports/
```

## Directory Purpose

docs

Architecture, deployment notes, troubleshooting, and technical documentation.

detections

Custom Wazuh detection rules and MITRE ATT&CK mappings.

automation

Python-based SOC automation and IOC enrichment scripts.

active-response

Wazuh Active Response configurations and containment workflows.

attack-simulations

Controlled lab scenarios used to validate detections.

incident-reports

SOC investigation reports generated from lab scenarios.

screenshots

Evidence showing endpoint telemetry, Wazuh alerts, detections, investigations, and automated responses.

---

# Skills Demonstrated

This project is designed to demonstrate practical experience with:

SOC Operations

SIEM Monitoring

Wazuh

Sysmon

Windows Event Logs

Endpoint Monitoring

Alert Triage

Incident Investigation

Threat Hunting

Log Analysis

Event Correlation

Detection Engineering

MITRE ATT&CK

IOC Analysis

Python Security Automation

Wazuh Active Response

Automated Incident Response

Security Documentation

---

# Project Progress

| Phase | Status |
|---|---|
| Wazuh Server Deployment | Completed |
| Windows 11 Agent Integration | Completed |
| Sysmon Installation | Completed |
| Sysmon to Wazuh Integration | Completed |
| SOC-Focused Sysmon Configuration | Completed |
| Wazuh Telemetry Validation | Completed |
| Kali Linux Preparation | Completed |
| Controlled Attack Simulations | Completed |
| Custom Wazuh Detection Rules | Completed |
| MITRE ATT&CK Mapping | Completed |
| Network Reconnaissance Detection | Completed |
| Correlation Detection | Completed |
| Windows Firewall Event Monitoring | Completed |
| Python SOC Automation | Completed |
| Wazuh Active Response | Completed |
| Automated IP Containment | Completed |
| Automatic IP Unblocking | Completed |
| IOC Enrichment | Completed |
| Automated Incident Reporting | Completed |

---

# Learning Outcome

This project focuses on understanding the complete SOC lifecycle rather than simply installing and running security tools.

For every detection scenario, the project will answer:

```text
What happened?
      |
Why was it detected?
      |
Which logs provide evidence?
      |
How should a SOC analyst investigate it?
      |
Which MITRE ATT&CK technique applies?
      |
How can the detection be improved?
      |
Which repetitive steps can be automated?
      |
How should the response be validated?
```

---

# Disclaimer

This project is developed exclusively for cybersecurity education, defensive security research, and SOC engineering practice.

All security simulations are performed against isolated virtual machines owned and controlled by the project author.