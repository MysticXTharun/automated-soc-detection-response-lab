# Detection 001 - Network Reconnaissance

## Overview

This detection demonstrates the identification of network activity originating from a controlled Kali Linux testing system and targeting a monitored Windows 11 endpoint.

The activity is captured using **Sysmon Event ID 3** and analyzed by Wazuh using a custom detection rule.

> This detection is intentionally scoped to the lab environment and demonstrates the telemetry-to-alert detection engineering workflow.

---

## Detection Summary

| Field | Value |
|---|---|
| Detection ID | DET-001 |
| Detection Name | Network Reconnaissance |
| Wazuh Rule ID | 100100 |
| Severity | Level 7 |
| Data Source | Sysmon |
| Event ID | 3 - Network Connection |
| MITRE ATT&CK | T1046 - Network Service Discovery |
| Tactic | Discovery |
| Response | Analyst Investigation |
| Environment | Controlled SOC Lab |

---

## Lab Environment

| System | IP Address | Purpose |
|---|---|---|
| Kali Linux | `192.168.130.141` | Controlled security testing |
| Windows 11 | `192.168.130.130` | Monitored endpoint |
| Wazuh Server | `192.168.130.129` | SIEM and detection |

---

## Detection Architecture

```text
Kali Linux
192.168.130.141
      |
      | Nmap TCP Connect Scan
      v
Windows 11
192.168.130.130
      |
      v
Sysmon Event ID 3
      |
      v
Wazuh Agent
      |
      v
Wazuh Manager
      |
      v
Custom Rule 100100
      |
      v
Level 7 Alert
      |
      v
MITRE ATT&CK T1046
      |
      v
SOC Investigation
```

---

## Controlled Attack Simulation

The following command was executed from the Kali Linux lab system:

```bash
nmap -sT 192.168.130.130
```

The scan identified the following reachable TCP ports:

```text
PORT      STATE   SERVICE
135/tcp   open    msrpc
139/tcp   open    netbios-ssn
445/tcp   open    microsoft-ds
7070/tcp  open    realserver
```

The service names are Nmap identifications and should be independently validated before being treated as confirmed services.

---

## Sysmon Telemetry

Sysmon Event ID 3 recorded network activity involving the Kali Linux source system.

Example observed event:

```text
Event ID:          3
Protocol:          tcp
Source IP:         192.168.130.141
Source Port:       35052
Destination IP:    192.168.130.130
Destination Port:  7070
Initiated:         false
```

The Windows process associated with the connection was:

```text
C:\Users\soc-analyst\Downloads\AnyDesk.exe
```

The value:

```text
Initiated: false
```

indicates that the monitored Windows process did not initiate the connection.

---

## Wazuh Detection Logic

A custom Wazuh rule was created to identify the controlled network activity.

```text
Rule ID:     100100
Severity:    Level 7
```

Detection groups:

```text
custom_network_recon
network_reconnaissance
lab_detection
```

The rule identifies network activity involving the Kali testing host and maps the activity to MITRE ATT&CK **T1046 - Network Service Discovery**.

The rule implementation is available at:

```text
rules/network_recon_rules.xml
```

---

## Detection Result

Wazuh successfully generated the custom alert:

```text
Rule ID:           100100
Level:             7
Source IP:         192.168.130.141
Destination IP:    192.168.130.130
Destination Port:  7070
MITRE ID:          T1046
Technique:         Network Service Discovery
Tactic:            Discovery
```

Alert description:

```text
LAB: External network connection from Kali testing host
192.168.130.141 to Windows endpoint 192.168.130.130:7070
```

---

## MITRE ATT&CK Mapping

| Field | Mapping |
|---|---|
| Tactic | Discovery |
| Technique | Network Service Discovery |
| Technique ID | T1046 |

Network reconnaissance can be used to identify reachable systems and exposed network services before subsequent activity.

---

## SOC Investigation Workflow

When this alert is generated, an analyst should review:

1. Source IP address
2. Destination IP address
3. Source and destination ports
4. Network protocol
5. Associated process
6. User context
7. Sysmon Event ID
8. Connection direction
9. Related network events
10. Repeated connections from the same source

The analyst should determine whether the activity represents expected administrative traffic, legitimate application behavior, authorized security testing, reconnaissance, or potentially malicious activity.

---

## Detection Limitations

Rule `100100` is intentionally designed as a learning rule for this isolated SOC lab.

The source IP is currently hard-coded:

```text
192.168.130.141
```

Therefore, the rule demonstrates the detection pipeline but should not be considered a production-grade port-scan detector.

Additionally, a single Sysmon Event ID 3 network connection does not independently prove that a complete port scan occurred.

Reliable reconnaissance detection generally requires correlation across multiple network events, ports, or other telemetry.

---

## Evolution to Detection 002

Detection 001 establishes the basic detection pipeline:

```text
Network Activity
      |
      v
Sysmon Telemetry
      |
      v
Wazuh Rule
      |
      v
Alert
      |
      v
MITRE Mapping
      |
      v
SOC Investigation
```

Detection 002 extends this concept by introducing:

```text
Repeated Blocked Connections
          +
Same Source IP
          +
Short Time Window
          |
          v
Correlation Detection
          |
          v
Automated Containment
```

Detection 002 adds:

- Windows Filtering Platform telemetry
- Event ID 5157
- Time-based event correlation
- Higher-severity detection
- Automated Windows Firewall containment
- Duplicate-response handling
- Automatic recovery

---

## Skills Demonstrated

- Wazuh SIEM administration
- Sysmon telemetry analysis
- Custom detection engineering
- Windows network-event analysis
- MITRE ATT&CK mapping
- Alert investigation
- Network reconnaissance analysis
- Detection validation
- Detection documentation

---

## Learning Outcome

This detection demonstrates the complete foundational detection-engineering workflow:

```text
Generate Activity
      |
      v
Collect Telemetry
      |
      v
Analyze Event
      |
      v
Create Detection Rule
      |
      v
Generate Alert
      |
      v
Map to MITRE ATT&CK
      |
      v
Investigate
```

This detection provides the foundation for the correlation and automated-response capabilities implemented in Detection 002.