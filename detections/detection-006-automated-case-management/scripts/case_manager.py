import argparse
import json
import os
import sys
from datetime import datetime, timedelta, timezone


def load_json(file_path):
    try:
        with open(file_path, "r", encoding="utf-8-sig") as file:
            return json.load(file)

    except FileNotFoundError:
        raise ValueError(f"Input file not found: {file_path}")

    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON file: {exc}")


def generate_case_id(rule_id):
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    return f"CASE-{timestamp}-R{rule_id}"


def determine_queue(priority):
    queues = {
        "P1": "SOC L2/L3 Escalation Queue",
        "P2": "SOC High Priority Queue",
        "P3": "SOC Standard Investigation Queue",
        "P4": "SOC Monitoring Queue"
    }

    return queues.get(
        priority,
        "SOC Manual Review Queue"
    )


def determine_sla(priority):
    sla_hours = {
        "P1": 1,
        "P2": 4,
        "P3": 8,
        "P4": 24
    }

    hours = sla_hours.get(priority, 24)

    created_at = datetime.now(timezone.utc)
    due_at = created_at + timedelta(hours=hours)

    return {
        "sla_hours": hours,
        "created_at_utc": created_at.isoformat(),
        "due_at_utc": due_at.isoformat()
    }


def determine_case_status(containment_status):
    status = str(containment_status).upper()

    if status == "SUCCESS":
        return "Contained - Analyst Review Required"

    if status == "FAILED":
        return "Open - Containment Required"

    return "Open - Investigation Required"


def determine_assignment(priority):
    assignments = {
        "P1": {
            "owner": "UNASSIGNED",
            "assignment_state": "Immediate L2/L3 Assignment Required"
        },
        "P2": {
            "owner": "UNASSIGNED",
            "assignment_state": "Priority Analyst Assignment Required"
        },
        "P3": {
            "owner": "UNASSIGNED",
            "assignment_state": "Awaiting SOC Analyst Assignment"
        },
        "P4": {
            "owner": "UNASSIGNED",
            "assignment_state": "Monitoring Queue"
        }
    }

    return assignments.get(
        priority,
        {
            "owner": "UNASSIGNED",
            "assignment_state": "Manual Assignment Required"
        }
    )


def determine_sla_status(sla):
    now = datetime.now(timezone.utc)

    created_at = datetime.fromisoformat(
        sla["created_at_utc"]
    )

    due_at = datetime.fromisoformat(
        sla["due_at_utc"]
    )

    case_age_minutes = round(
        (now - created_at).total_seconds() / 60,
        2
    )

    remaining_minutes = round(
        (due_at - now).total_seconds() / 60,
        2
    )

    if remaining_minutes < 0:
        status = "BREACHED"

    elif remaining_minutes <= 60:
        status = "AT_RISK"

    else:
        status = "WITHIN_SLA"

    return {
        "status": status,
        "case_age_minutes": case_age_minutes,
        "remaining_minutes": remaining_minutes
    }


def determine_closure_recommendation(
    priority,
    containment_status
):
    containment_status = str(
        containment_status
    ).upper()

    if containment_status == "FAILED":
        return (
            "Keep case open and perform manual containment "
            "before considering closure"
        )

    if priority in ("P1", "P2"):
        return (
            "Keep case open until investigation and "
            "escalation requirements are completed"
        )

    if containment_status == "SUCCESS":
        return (
            "Eligible for closure after analyst validation "
            "confirms no additional suspicious activity"
        )

    return (
        "Keep case open until investigation and "
        "containment status are validated"
    )


def build_timeline(data):
    alert = data.get("alert", {})
    containment = data.get("containment", {})
    triage = data.get("triage_result", {})

    alert_timestamp = alert.get("timestamp")
    triage_timestamp = data.get("triage_timestamp_utc")
    processing_timestamp = datetime.now(
        timezone.utc
    ).isoformat()

    return [
        {
            "timestamp_utc": alert_timestamp or "UNKNOWN",
            "event": "Security alert detected",
            "details": (
                f"Wazuh Rule {alert.get('rule_id')} detected activity "
                f"from {alert.get('source_ip')} to "
                f"{alert.get('destination_ip')}:"
                f"{alert.get('destination_port')}"
            )
        },
        {
            "timestamp_utc": triage_timestamp or "UNKNOWN",
            "event": "Automated triage completed",
            "details": (
                f"Priority assigned: {triage.get('priority')}. "
                f"Recommended action: "
                f"{triage.get('recommended_action')}"
            )
        },
        {
            "timestamp_utc": processing_timestamp,
            "event": "Containment status evaluated",
            "details": (
                f"Containment response: "
                f"{containment.get('response')}. "
                f"Status: {containment.get('status')}"
            )
        },
        {
            "timestamp_utc": processing_timestamp,
            "event": "SOC case created",
            "details": (
                "Automated case-management workflow created "
                "the incident case for analyst tracking."
            )
        }
    ]


def generate_case(data):
    alert = data.get("alert", {})
    triage = data.get("triage_result", {})
    containment = data.get("containment", {})
    asset = data.get("asset_context", {})
    ioc = data.get("ioc_assessment", {})

    rule_id = alert.get("rule_id", "N/A")
    priority = triage.get("priority", "P4")

    case_id = generate_case_id(rule_id)
    queue = determine_queue(priority)
    sla = determine_sla(priority)

    case_status = determine_case_status(
        containment.get("status", "UNKNOWN")
    )

    assignment = determine_assignment(priority)

    sla_status = determine_sla_status(sla)

    closure_recommendation = determine_closure_recommendation(
        priority,
        containment.get("status", "UNKNOWN")
    )

    case = {
        "case_id": case_id,
        "case_status": case_status,
        "priority": priority,
        "assigned_queue": queue,

        "assignment": {
            "owner": assignment["owner"],
            "state": assignment["assignment_state"]
        },

        "sla": {
            "sla_hours": sla["sla_hours"],
            "created_at_utc": sla["created_at_utc"],
            "due_at_utc": sla["due_at_utc"],
            "status": sla_status["status"],
            "case_age_minutes": sla_status[
                "case_age_minutes"
            ],
            "remaining_minutes": sla_status[
                "remaining_minutes"
            ]
        },

        "closure_recommendation": (
            closure_recommendation
        ),

        "detection": {
            "timestamp": alert.get("timestamp"),
            "rule_id": rule_id,
            "rule_level": alert.get("rule_level"),
            "rule_description": alert.get(
                "rule_description"
            ),
            "source_ip": alert.get("source_ip"),
            "destination_ip": alert.get(
                "destination_ip"
            ),
            "destination_port": alert.get(
                "destination_port"
            ),
            "mitre_ids": alert.get(
                "mitre_ids",
                []
            ),
            "mitre_tactics": alert.get(
                "mitre_tactics",
                []
            ),
            "mitre_techniques": alert.get(
                "mitre_techniques",
                []
            )
        },

        "asset_context": asset,

        "ioc_assessment": ioc,

        "containment": containment,

        "triage": {
            "priority": priority,
            "recommended_action": triage.get(
                "recommended_action",
                "Manual review required"
            )
        },

        "investigation_summary": (
            f"Rule {rule_id} detected activity from "
            f"{alert.get('source_ip')} targeting "
            f"{alert.get('destination_ip')}:"
            f"{alert.get('destination_port')}. "
            f"The alert was triaged as {priority}. "
            f"Containment status is "
            f"{containment.get('status')}."
        ),

        "timeline": build_timeline(data)
    }

    return case


def main():
    parser = argparse.ArgumentParser(
        description="Automated SOC case management engine"
    )

    parser.add_argument(
        "--input",
        required=True,
        help="Path to Detection 005 triage JSON"
    )

    parser.add_argument(
        "--output",
        required=True,
        help="Path for generated case JSON"
    )

    args = parser.parse_args()

    try:
        data = load_json(args.input)

        case = generate_case(data)

        output_directory = os.path.dirname(
            args.output
        )

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
            json.dump(
                case,
                file,
                indent=4
            )

        print(
            f"Case generated: {args.output}"
        )

    except ValueError as exc:
        print(f"ERROR: {exc}")
        sys.exit(1)

    except Exception as exc:
        print(
            f"ERROR: Unexpected failure: {exc}"
        )
        sys.exit(1)


if __name__ == "__main__":
    main()