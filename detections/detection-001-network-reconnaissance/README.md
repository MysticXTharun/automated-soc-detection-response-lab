\# Detection 001 - Network Reconnaissance



\## Overview



This detection demonstrates the identification of network activity originating from a controlled Kali Linux testing system and targeting a monitored Windows 11 endpoint.



The activity is captured using Sysmon Event ID 3 and analyzed by Wazuh using a custom detection rule.



\## MITRE ATT\&CK Mapping



| Field | Value |

|---|---|

| Tactic | Discovery |

| Technique | Network Service Discovery |

| Technique ID | T1046 |



\## Lab Environment



| System | IP Address | Purpose |

|---|---|---|

| Kali Linux | 192.168.130.141 | Controlled security testing |

| Windows 11 | 192.168.130.130 | Monitored endpoint |

| Wazuh Server | 192.168.130.129 | SIEM and detection |



\## Detection Flow



```text

Kali Linux

192.168.130.141

&#x20;     |

&#x20;     | Nmap TCP Connect Scan

&#x20;     v

Windows 11

192.168.130.130

&#x20;     |

&#x20;     v

Sysmon Event ID 3

&#x20;     |

&#x20;     v

Wazuh Agent

&#x20;     |

&#x20;     v

Wazuh Manager

&#x20;     |

&#x20;     v

Custom Rule 100100

&#x20;     |

&#x20;     v

Level 7 Alert

&#x20;     |

&#x20;     v

MITRE ATT\&CK T1046

```



\## Controlled Simulation



The following command was executed from the Kali Linux lab system:



```bash

nmap -sT 192.168.130.130

```



The scan identified the following reachable TCP ports:



```text

135/tcp   open   msrpc

139/tcp   open   netbios-ssn

445/tcp   open   microsoft-ds

7070/tcp  open   realserver

```



The service names shown above are Nmap identifications and should be independently verified before being treated as confirmed services.



\## Sysmon Telemetry



Sysmon Event ID 3 recorded network activity involving the Kali Linux source system.



Observed event:



```text

Event ID:        3

Protocol:        tcp

Source IP:       192.168.130.141

Source Port:     35052

Destination IP:  192.168.130.130

Destination Port: 7070

Initiated:       false

```



The Windows process associated with the accepted connection was:



```text

C:\\Users\\soc-analyst\\Downloads\\AnyDesk.exe

```



The value:



```text

Initiated: false

```



indicates that the monitored Windows process did not initiate the connection.



\## Wazuh Detection



A custom Wazuh rule was created to detect the controlled lab activity.



Rule ID:



```text

100100

```



Severity:



```text

Level 7

```



Detection groups:



```text

custom\_network\_recon

network\_reconnaissance

lab\_detection

```



\## Detection Result



The custom rule successfully generated a Wazuh alert.



```text

Rule ID:        100100

Level:          7

Source IP:      192.168.130.141

Destination IP: 192.168.130.130

Destination Port: 7070

MITRE ID:       T1046

Technique:      Network Service Discovery

Tactic:         Discovery

```



Alert description:



```text

LAB: External network connection from Kali testing host 192.168.130.141 to Windows endpoint 192.168.130.130:7070

```



\## SOC Investigation



During investigation, the analyst should review:



```text

Source IP

Destination IP

Source Port

Destination Port

Protocol

Associated Process

User

Sysmon Event ID

Connection Direction

Related Network Events

Repeated Connections

```



The analyst should then determine whether the activity represents expected administrative traffic, legitimate application behavior, reconnaissance, or potentially malicious activity.



\## Detection Limitation



Rule 100100 is intentionally designed as a learning rule for this isolated SOC lab.



The source address is currently hard-coded to:



```text

192.168.130.141

```



Therefore, this rule demonstrates the detection pipeline but is not yet a production-grade port-scan detector.



A single Sysmon Event ID 3 network connection also does not independently prove that a complete port scan occurred.



Future versions will investigate correlation of multiple connections and additional network telemetry.



\## Future Improvements



Detection 002 will investigate:



```text

Multiple destination ports

&#x20;       +

Same source IP

&#x20;       +

Short time window

&#x20;       |

&#x20;       v

Potential Network Reconnaissance

```



Future development will also include:



```text

Time-based correlation

Removal of hard-coded source IP

False-positive handling

Detection thresholds

MITRE ATT\&CK enrichment

Risk scoring

Automated response

```



\## Learning Outcome



This detection demonstrated the complete workflow:



```text

Generate Activity

&#x20;     |

&#x20;     v

Collect Telemetry

&#x20;     |

&#x20;     v

Analyze Sysmon Event

&#x20;     |

&#x20;     v

Create Wazuh Rule

&#x20;     |

&#x20;     v

Generate Alert

&#x20;     |

&#x20;     v

Map to MITRE ATT\&CK

&#x20;     |

&#x20;     v

Investigate

```



This establishes the foundation for more advanced detection engineering and SOC automation.

