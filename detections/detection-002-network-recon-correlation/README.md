\# Detection 002 - Correlated Network Reconnaissance with Automated Containment



\## Objective



Detect repeated inbound TCP reconnaissance activity against a Windows endpoint, correlate multiple Windows Filtering Platform events in Wazuh, and automatically contain the source IP using Windows Firewall.



\## Lab Environment



\- Attacker: Kali Linux - 192.168.130.141

\- Target: Windows 11 - 192.168.130.130

\- SIEM/XDR: Wazuh

\- Telemetry: Windows Security Event 5157

\- Detection Rule: 100110

\- Correlation Rule: 100111

\- Severity: Level 10

\- MITRE ATT\&CK: T1046 - Network Service Discovery



\## Detection Logic



Rule 100110 identifies blocked inbound TCP connections originating from the Kali testing host.



Rule 100111 correlates three matching events within 10 seconds from the same source address.



\## Attack Simulation



Nmap was used from Kali Linux to scan selected TCP ports on the Windows endpoint.



```bash

nmap -sT -p 22,23,80,135,139,443,445,3389,7070 192.168.130.130

