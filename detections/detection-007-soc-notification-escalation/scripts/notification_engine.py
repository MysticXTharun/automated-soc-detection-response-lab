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


def determine_notification_level(
    priority,
    containment_status,
    sla_status
):
    priority = str(priority).upper()
    containment_status = str(containment_status).upper()
    sla_status = str(sla_status).upper()

    if sla_status == "BREACHED":
        return "CRITICAL"

    if priority == "P1":
        return "CRITICAL"

    if containment_status == "FAILED":
        return "HIGH"

    if priority == "P2":
        return "HIGH"

    if sla_status == "AT_RISK":
        return "HIGH"

    if priority == "P3":
        return "STANDARD"

    return "LOW"


def determine_recipients(notification_level):
    recipients = {
        "CRITICAL": [
            "SOC L2/L3",
            "SOC Manager",
            "Incident Response Team"
        ],
        "HIGH": [
            "SOC L2",
            "SOC Shift Lead"
        ],
        "STANDARD": [
            "SOC Analyst Queue"
        ],
        "LOW": [
            "SOC Monitoring Queue"
        ]
    }

    return recipients.get(
        notification_level,
        ["SOC Analyst Queue"]
    )


def determine_escalation(
    priority,
    containment_status,
    sla_status
):
    priority = str(priority).upper()
    containment_status = str(containment_status).upper()
    sla_status = str(sla_status).upper()

    if sla_status == "BREACHED":
        return {
            "required": True,
            "level": "Management Escalation",
            "reason": "Case SLA has been breached"
        }

    if priority == "P1":
        return {
            "required": True,
            "level": "Immediate L2/L3 Escalation",
            "reason": "P1 critical-priority security case"
        }

    if containment_status == "FAILED":
        return {
            "required": True,
            "level": "L2 Escalation",
            "reason": "Automated containment failed"
        }

    if priority == "P2":
        return {
            "required": True,
            "level": "L2 Escalation",
            "reason": "P2 high-priority security case"
        }

    if sla_status == "AT_RISK":
        return {
            "required": True,
            "level": "SOC Shift Lead Escalation",
            "reason": "Case is approaching its SLA deadline"
        }

    return {
        "required": False,
        "level": "No Immediate Escalation",
        "reason": "Current case context does not require escalation"
    }


def build_notification_message(
    case_id,
    priority,
    case_status,
    queue,
    containment_status,
    sla_status,
    escalation
):
    return (
        f"SOC Case {case_id} is currently classified as {priority}. "
        f"Case status: {case_status}. "
        f"Assigned queue: {queue}. "
        f"Containment status: {containment_status}. "
        f"SLA status: {sla_status}. "
        f"Escalation: {escalation['level']}."
    )


def generate_notification(data):
    case_id = data.get("case_id", "UNKNOWN")
    case_status = data.get("case_status", "UNKNOWN")
    priority = data.get("priority", "P4")
    queue = data.get(
        "assigned_queue",
        "SOC Manual Review Queue"
    )

    containment = data.get("containment", {})
    sla = data.get("sla", {})
    detection = data.get("detection", {})

    containment_status = containment.get(
        "status",
        "UNKNOWN"
    )

    sla_status = sla.get(
        "status",
        "UNKNOWN"
    )

    notification_level = determine_notification_level(
        priority,
        containment_status,
        sla_status
    )

    recipients = determine_recipients(
        notification_level
    )

    escalation = determine_escalation(
        priority,
        containment_status,
        sla_status
    )

    message = build_notification_message(
        case_id,
        priority,
        case_status,
        queue,
        containment_status,
        sla_status,
        escalation
    )

    return {
        "notification_timestamp_utc": datetime.now(
            timezone.utc
        ).isoformat(),

        "case_id": case_id,

        "notification": {
            "level": notification_level,
            "recipients": recipients,
            "message": message
        },

        "escalation": escalation,

        "case_context": {
            "priority": priority,
            "case_status": case_status,
            "assigned_queue": queue,
            "sla_status": sla_status,
            "containment_status": containment_status
        },

        "detection_context": {
            "rule_id": detection.get("rule_id"),
            "source_ip": detection.get("source_ip"),
            "destination_ip": detection.get(
                "destination_ip"
            ),
            "destination_port": detection.get(
                "destination_port"
            ),
            "mitre_ids": detection.get(
                "mitre_ids",
                []
            )
        }
    }


def main():
    parser = argparse.ArgumentParser(
        description=(
            "Generate SOC notification and escalation "
            "decisions from a case-management JSON file"
        )
    )

    parser.add_argument(
        "--input",
        required=True,
        help="Path to Detection 006 case JSON"
    )

    parser.add_argument(
        "--output",
        required=True,
        help="Path for generated notification JSON"
    )

    args = parser.parse_args()

    try:
        data = load_json(args.input)

        notification = generate_notification(data)

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
                notification,
                file,
                indent=4
            )

        print(
            f"SOC notification generated: {args.output}"
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