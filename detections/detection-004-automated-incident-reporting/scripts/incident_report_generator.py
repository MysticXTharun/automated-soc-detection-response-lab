import argparse
import json
import os
import sys
from datetime import datetime, timezone


def load_json(file_path):
    try:
        with open(file_path, "r", encoding="utf-8-sig") as file:
            return json.load(file)
    except FileNotFoundError:
        raise ValueError(f"Input file not found: {file_path}")
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON file: {exc}")


def severity_from_level(rule_level):
    try:
        level = int(rule_level)
    except (TypeError, ValueError):
        return "UNKNOWN"

    if level >= 12:
        return "CRITICAL"
    elif level >= 8:
        return "HIGH"
    elif level >= 4:
        return "MEDIUM"
    else:
        return "LOW"


def join_values(values):
    if not values:
        return "N/A"

    if isinstance(values, list):
        return ", ".join(str(value) for value in values)

    return str(values)


def generate_incident_id(rule_id):
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    return f"INC-{timestamp}-R{rule_id}"


def determine_disposition(alert, assessment):
    description = str(alert.get("rule_description", "")).lower()
    verdict = str(assessment.get("verdict", "")).upper()

    if "lab" in description:
        return "Confirmed Lab Security Activity"

    if verdict == "MALICIOUS":
        return "Confirmed Malicious Activity"

    if verdict == "SUSPICIOUS":
        return "Suspicious Activity - Investigation Required"

    if verdict == "BENIGN":
        return "Likely Benign"

    if verdict == "INTERNAL":
        return "Internal Source - Context Validation Required"

    return "Undetermined"


def determine_escalation(disposition, severity):
    if disposition == "Confirmed Lab Security Activity":
        return "No production escalation required - controlled lab activity"

    if severity in ("CRITICAL", "HIGH"):
        return "Escalate to L2/L3 SOC for further investigation"

    if severity == "MEDIUM":
        return "Analyst review required"

    return "Monitor and close if validated as benign"


def generate_report(data):
    alert = data.get("alert_context", {})
    enrichment = data.get("enrichment", {})
    assessment = enrichment.get("soc_assessment") or {}
    threat_intel = enrichment.get("threat_intelligence") or {}

    generated_at = datetime.now(timezone.utc).isoformat()

    rule_id = alert.get("rule_id", "N/A")
    rule_level = alert.get("rule_level", "N/A")
    description = alert.get("rule_description", "N/A")

    incident_id = generate_incident_id(rule_id)
    severity = severity_from_level(rule_level)

    detection_timestamp = alert.get("timestamp", "N/A")

    mitre_ids = join_values(alert.get("mitre_ids"))
    mitre_tactics = join_values(alert.get("mitre_tactics"))
    mitre_techniques = join_values(alert.get("mitre_techniques"))

    agent_name = alert.get("agent_name", "N/A")
    agent_id = alert.get("agent_id", "N/A")

    source_ip = alert.get(
        "source_ip",
        enrichment.get("ioc", "N/A")
    )

    destination_ip = alert.get("destination_ip", "N/A")
    destination_port = alert.get("destination_port", "N/A")

    classification = enrichment.get("classification", "N/A")
    reverse_dns = enrichment.get("reverse_dns", "N/A")

    verdict = assessment.get("verdict", "UNKNOWN")
    risk_level = assessment.get("risk_level", "UNKNOWN")
    reason = assessment.get(
        "reason",
        "No assessment available"
    )

    ti_status = threat_intel.get(
        "status",
        "Not applicable"
    )

    abuse_score = threat_intel.get(
        "abuse_confidence_score",
        "Not applicable"
    )

    disposition = determine_disposition(
        alert,
        assessment
    )

    escalation = determine_escalation(
        disposition,
        severity
    )

    report = f"""# SOC Incident Report

## Incident Overview

| Field | Value |
|---|---|
| Incident ID | {incident_id} |
| Detection Timestamp | {detection_timestamp} |
| Report Generated UTC | {generated_at} |
| Severity | {severity} |
| Wazuh Rule ID | {rule_id} |
| Wazuh Rule Level | {rule_level} |
| Detection | {description} |
| Agent | {agent_name} |
| Agent ID | {agent_id} |

## Network Context

| Field | Value |
|---|---|
| Source IP | {source_ip} |
| Destination IP | {destination_ip} |
| Destination Port | {destination_port} |

## MITRE ATT&CK Mapping

| Field | Value |
|---|---|
| Tactic | {mitre_tactics} |
| Technique | {mitre_techniques} |
| Technique ID | {mitre_ids} |

## IOC Enrichment

| Field | Value |
|---|---|
| IOC | {enrichment.get("ioc", "N/A")} |
| IOC Type | {enrichment.get("ioc_type", "N/A")} |
| Classification | {classification} |
| Reverse DNS | {reverse_dns} |
| Public TI Lookup | {enrichment.get("public_threat_intel_lookup", False)} |
| Threat Intelligence Status | {ti_status} |
| Abuse Confidence Score | {abuse_score} |

## SOC Assessment

| Field | Value |
|---|---|
| Verdict | {verdict} |
| Risk Level | {risk_level} |
| Assessment Reason | {reason} |
| Incident Disposition | {disposition} |
| Escalation Recommendation | {escalation} |

## Investigation Summary

The monitored endpoint `{agent_name}` generated Wazuh Rule `{rule_id}`
after detecting activity from source IP `{source_ip}` targeting
`{destination_ip}:{destination_port}`.

The activity maps to MITRE ATT&CK technique `{mitre_ids}` -
`{mitre_techniques}` under the `{mitre_tactics}` tactic.

IOC enrichment classified `{source_ip}` as `{classification}`.

The automated SOC assessment returned a verdict of `{verdict}`
with a risk level of `{risk_level}`.

Incident disposition:

`{disposition}`

## Recommended Analyst Actions

1. Validate whether the source system is authorized.
2. Review related alerts from the same source IP.
3. Review destination ports and associated services.
4. Correlate Windows, Sysmon, and network telemetry.
5. Confirm whether automated containment was triggered.
6. Review related MITRE ATT&CK activity.
7. Escalate according to the recommendation below.

Escalation recommendation:

`{escalation}`

## Evidence Summary

Incident ID: `{incident_id}`

Wazuh Rule: `{rule_id}`

Severity: `{severity}`

Source IOC: `{source_ip}`

Destination: `{destination_ip}:{destination_port}`

MITRE ATT&CK: `{mitre_ids}`

Technique: `{mitre_techniques}`

IOC Classification: `{classification}`

SOC Verdict: `{verdict}`

Risk Level: `{risk_level}`

Disposition: `{disposition}`

---

Generated automatically by the Automated SOC Detection & Response Lab.
"""

    return report


def main():
    parser = argparse.ArgumentParser(
        description=(
            "Generate a SOC incident report from "
            "enriched Wazuh alert JSON"
        )
    )

    parser.add_argument(
        "--input",
        required=True,
        help="Path to enriched Wazuh alert JSON"
    )

    parser.add_argument(
        "--output",
        required=True,
        help="Path for generated Markdown incident report"
    )

    args = parser.parse_args()

    try:
        data = load_json(args.input)
        report = generate_report(data)

        output_directory = os.path.dirname(args.output)

        if output_directory:
            os.makedirs(
                output_directory,
                exist_ok=True
            )

        with open(
            args.output,
            "w",
            encoding="utf-8"
        ) as file:
            file.write(report)

        print(
            f"Incident report generated: {args.output}"
        )

    except ValueError as exc:
        print(f"ERROR: {exc}")
        sys.exit(1)

    except Exception as exc:
        print(f"ERROR: Unexpected failure: {exc}")
        sys.exit(1)


if __name__ == "__main__":
    main()