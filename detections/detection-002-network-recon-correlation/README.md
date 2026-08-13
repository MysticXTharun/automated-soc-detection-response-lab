# Detection 002 - Correlated Network Reconnaissance with Automated Containment

## Overview

This detection extends Detection 001 by correlating repeated blocked inbound TCP connections from a controlled Kali Linux host against a monitored Windows 11 endpoint.

Windows Filtering Platform telemetry is collected by the Wazuh agent. Multiple matching events are correlated by Wazuh, producing a higher-severity reconnaissance alert and triggering a custom automated containment response.

The source IP is temporarily blocked using Windows Firewall and automatically unblocked after the active-response timeout.

---

## Detection Summary

| Field | Value |
|---|---|
| Detection ID | DET-002 |
| Detection Name | Correlated Network Reconnaissance |
| Base Rule | 100110 |
| Correlation Rule | 100111 |
| Correlation Severity | Level 10 |
| Data Source | Windows Security |
| Event ID | 5157 |
| MITRE ATT&CK | T1046 - Network Service Discovery |
| Tactic | Discovery |
| Correlation Threshold | 3 events within 10 seconds |
| Automated Response | Temporary Windows Firewall block |
| Response Executable | `block-recon-ip.exe` |
| Recovery | Automatic unblock |

---

## Lab Environment

| System | IP Address | Purpose |
|---|---|---|
| Kali Linux | `192.168.130.141` | Controlled reconnaissance source |
| Windows 11 | `192.168.130.130` | Monitored and protected endpoint |
| Wazuh Server | `192.168.130.129` | SIEM, correlation and response orchestration |

---

## Detection and Response Architecture

```text
Kali Linux
192.168.130.141
      |
      | Nmap TCP reconnaissance
      v
Windows 11
192.168.130.130
      |
      v
Windows Filtering Platform
Event ID 5157
      |
      v
Wazuh Agent
      |
      v
Wazuh Manager
      |
      v
Rule 100110
Blocked Inbound TCP Connection
      |
      | 3 matching events / 10 seconds
      v
Rule 100111
Level 10 Correlation Alert
      |
      v
MITRE ATT&CK T1046
      |
      v
Wazuh Active Response
      |
      v
block-recon-ip.exe
      |
      v
Windows Firewall
      |
      v
Temporary Source-IP Containment
      |
      v
Automatic Unblock
```

---

## Controlled Attack Simulation

A TCP connect scan was generated from the Kali Linux testing host:

```bash
nmap -sT -p 22,23,80,135,139,443,445,3389,7070 192.168.130.130
```

Observed services included:

```text
135/tcp   open
139/tcp   open
445/tcp   open
7070/tcp  open
```

This activity generated Windows Filtering Platform events on the monitored endpoint.

---

## Windows Telemetry

Windows Filtering Platform auditing was enabled to capture permitted and blocked network connections.

The detection uses:

```text
Windows Security Event ID: 5157
Event: Windows Filtering Platform blocked a connection
Protocol: TCP
Direction: Inbound
```

Example activity:

```text
Source Address:       192.168.130.141
Destination Address:  192.168.130.130
Destination Port:     22
Protocol:             6
Direction:            Inbound
```

---

## Base Detection - Rule 100110

Rule `100110` identifies blocked inbound TCP connections from the controlled Kali testing host.

```text
Rule ID:  100110
Level:    3
```

Example alert:

```text
LAB: Blocked inbound TCP connection from Kali
192.168.130.141 to Windows 192.168.130.130:445
```

---

## Correlation Detection - Rule 100111

Rule `100111` correlates repeated Rule `100110` events.

Correlation logic:

```text
Same Source IP
      +
3 Matching Events
      +
10-Second Window
      |
      v
Potential Network Reconnaissance
```

Detection result:

```text
Rule ID:     100111
Level:       10
Source IP:   192.168.130.141
MITRE ID:    T1046
```

Alert description:

```text
LAB: Repeated blocked TCP connections detected from Kali
192.168.130.141 - possible network reconnaissance
```

The rule implementation is available at:

```text
rules/network_scan_correlation.xml
```

---

## MITRE ATT&CK Mapping

| Field | Mapping |
|---|---|
| Tactic | Discovery |
| Technique | Network Service Discovery |
| Technique ID | T1046 |

---

## Automated Containment

The Level 10 correlation alert triggers a custom Wazuh Active Response:

```text
block-recon-ip.exe
```

The executable was developed from:

```text
active-response/block-recon-ip.py
```

The response extracts the source IP from the Wazuh alert and creates a temporary inbound Windows Firewall blocking rule.

Example response:

```text
block-recon-ip: BLOCKED 192.168.130.141
```

Windows Firewall validation:

```text
DisplayName: Wazuh-Recon-Block-192-168-130-141
Enabled:     True
Direction:   Inbound
Action:      Block
```

---

## Duplicate Response Handling

Additional correlation alerts can occur while containment is already active.

The custom response prevents duplicate firewall actions:

```text
block-recon-ip: Action aborted for 192.168.130.141
```

This prevents unnecessary duplicate containment rules from being created.

---

## Containment Validation

Before automated containment:

```text
PORT      STATE
135/tcp   open
139/tcp   open
445/tcp   open
7070/tcp  open
```

During automated containment:

```text
PORT      STATE
135/tcp   filtered
139/tcp   filtered
445/tcp   filtered
7070/tcp  filtered
```

This validates that the automated response was enforcing network containment rather than simply generating a response log.

---

## Automatic Recovery

After the configured active-response timeout, the custom response removed the temporary firewall rule.

```text
block-recon-ip: UNBLOCKED 192.168.130.141
```

A subsequent query:

```powershell
Get-NetFirewallRule -DisplayName "Wazuh-Recon-Block-*"
```

returned no matching rule, confirming successful cleanup.

---

## Complete SOC Workflow

```text
Reconnaissance
      |
      v
Telemetry Collection
      |
      v
Base Detection
      |
      v
Event Correlation
      |
      v
Level 10 Alert
      |
      v
MITRE ATT&CK Mapping
      |
      v
Automated Containment
      |
      v
Containment Validation
      |
      v
Automatic Recovery
```

---

## Detection Limitations

This detection was developed specifically for an isolated SOC lab.

The source and destination IP addresses are intentionally constrained to the lab systems. A production implementation should avoid relying on hard-coded attacker addresses and should instead incorporate broader behavioral logic.

Potential production improvements include:

- Dynamic source-IP correlation
- Destination-port diversity tracking
- Allowlisting of approved vulnerability scanners
- Asset criticality
- Source reputation
- Risk scoring
- Longer-term correlation
- Threshold tuning
- False-positive suppression
- Response allowlists
- Protection against blocking trusted infrastructure

---

## Skills Demonstrated

- Wazuh SIEM administration
- Detection engineering
- Windows Filtering Platform analysis
- Windows Security Event analysis
- Event correlation
- MITRE ATT&CK mapping
- Python automation
- Wazuh Active Response
- Windows Firewall automation
- Automated incident containment
- Duplicate-response handling
- Detection validation
- Automated recovery
- SOC documentation

---

## Project Outcome

Detection 002 demonstrates an end-to-end detection-and-response lifecycle:

```text
Detect
  ↓
Correlate
  ↓
Prioritize
  ↓
Contain
  ↓
Validate
  ↓
Recover
```

The project progresses from the basic network detection implemented in Detection 001 to a correlated and automated SOC response workflow.