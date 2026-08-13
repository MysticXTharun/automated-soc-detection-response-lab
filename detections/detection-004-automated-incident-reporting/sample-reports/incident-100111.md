# SOC Incident Report

## Incident Overview

| Field | Value |
|---|---|
| Incident ID | INC-20260813-094052-R100111 |
| Detection Timestamp | 2026-08-13T05:14:03.915+0000 |
| Report Generated UTC | 2026-08-13T09:40:52.153545+00:00 |
| Severity | HIGH |
| Wazuh Rule ID | 100111 |
| Wazuh Rule Level | 10 |
| Detection | LAB: Repeated blocked TCP connections detected from Kali 192.168.130.141 - possible network reconnaissance |
| Agent | DESKTOP-D316EOG |
| Agent ID | 001 |

## Network Context

| Field | Value |
|---|---|
| Source IP | 192.168.130.141 |
| Destination IP | 192.168.130.130 |
| Destination Port | 445 |

## MITRE ATT&CK Mapping

| Field | Value |
|---|---|
| Tactic | Discovery |
| Technique | Network Service Discovery |
| Technique ID | T1046 |

## IOC Enrichment

| Field | Value |
|---|---|
| IOC | 192.168.130.141 |
| IOC Type | ip |
| Classification | Private IP |
| Reverse DNS | 192.168.130.141 |
| Public TI Lookup | False |
| Threat Intelligence Status | Not applicable |
| Abuse Confidence Score | Not applicable |

## SOC Assessment

| Field | Value |
|---|---|
| Verdict | INTERNAL |
| Risk Level | INFO |
| Assessment Reason | Private or non-public IP; public reputation lookup not applicable |
| Incident Disposition | Confirmed Lab Security Activity |
| Escalation Recommendation | No production escalation required - controlled lab activity |

## Investigation Summary

The monitored endpoint `DESKTOP-D316EOG` generated Wazuh Rule `100111`
after detecting activity from source IP `192.168.130.141` targeting
`192.168.130.130:445`.

The activity maps to MITRE ATT&CK technique `T1046` -
`Network Service Discovery` under the `Discovery` tactic.

IOC enrichment classified `192.168.130.141` as `Private IP`.

The automated SOC assessment returned a verdict of `INTERNAL`
with a risk level of `INFO`.

Incident disposition:

`Confirmed Lab Security Activity`

## Recommended Analyst Actions

1. Validate whether the source system is authorized.
2. Review related alerts from the same source IP.
3. Review destination ports and associated services.
4. Correlate Windows, Sysmon, and network telemetry.
5. Confirm whether automated containment was triggered.
6. Review related MITRE ATT&CK activity.
7. Escalate according to the recommendation below.

Escalation recommendation:

`No production escalation required - controlled lab activity`

## Evidence Summary

Incident ID: `INC-20260813-094052-R100111`

Wazuh Rule: `100111`

Severity: `HIGH`

Source IOC: `192.168.130.141`

Destination: `192.168.130.130:445`

MITRE ATT&CK: `T1046`

Technique: `Network Service Discovery`

IOC Classification: `Private IP`

SOC Verdict: `INTERNAL`

Risk Level: `INFO`

Disposition: `Confirmed Lab Security Activity`

---

Generated automatically by the Automated SOC Detection & Response Lab.
