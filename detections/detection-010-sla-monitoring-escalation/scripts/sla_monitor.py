import argparse
import json
from datetime import datetime, timezone
from pathlib import Path


def load_json(path):
    with open(path, "r", encoding="utf-8-sig") as file:
        return json.load(file)


def parse_timestamp(value):
    return datetime.fromisoformat(
        value.replace("Z", "+00:00")
    )


def determine_sla_status(case_data, evaluation_time):
    sla = case_data["sla"]

    created_at = parse_timestamp(
        sla["created_at_utc"]
    )

    due_at = parse_timestamp(
        sla["due_at_utc"]
    )

    case_age_minutes = round(
        (evaluation_time - created_at).total_seconds() / 60,
        2
    )

    remaining_minutes = round(
        (due_at - evaluation_time).total_seconds() / 60,
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


def determine_escalation(status, priority):
    if status == "BREACHED":
        return {
            "required": True,
            "level": "Management Escalation",
            "reason": "Case SLA has been breached"
        }

    if status == "AT_RISK":
        if priority in ("P1", "P2"):
            level = "Immediate SOC Lead Escalation"
        else:
            level = "SOC Lead Warning"

        return {
            "required": True,
            "level": level,
            "reason": (
                "Case is approaching the SLA deadline"
            )
        }

    return {
        "required": False,
        "level": "No Escalation",
        "reason": "Case remains within SLA"
    }


def monitor_case(case_data, evaluation_time):
    priority = case_data.get(
        "priority",
        "UNKNOWN"
    )

    sla_result = determine_sla_status(
        case_data,
        evaluation_time
    )

    escalation = determine_escalation(
        sla_result["status"],
        priority
    )

    return {
        "evaluation_timestamp_utc": (
            evaluation_time.isoformat()
        ),
        "case_id": case_data.get("case_id"),
        "priority": priority,
        "case_status": case_data.get(
            "case_status"
        ),
        "assigned_queue": case_data.get(
            "assigned_queue"
        ),
        "sla": {
            "sla_hours": case_data[
                "sla"
            ].get("sla_hours"),
            "created_at_utc": case_data[
                "sla"
            ].get("created_at_utc"),
            "due_at_utc": case_data[
                "sla"
            ].get("due_at_utc"),
            "status": sla_result["status"],
            "case_age_minutes": (
                sla_result["case_age_minutes"]
            ),
            "remaining_minutes": (
                sla_result["remaining_minutes"]
            )
        },
        "escalation": escalation
    }


def main():
    parser = argparse.ArgumentParser(
        description=(
            "Automated SOC SLA monitoring "
            "and escalation engine"
        )
    )

    parser.add_argument(
        "--input",
        required=True,
        help="SOC case JSON file"
    )

    parser.add_argument(
        "--output",
        required=True,
        help="Output SLA monitoring JSON file"
    )

    parser.add_argument(
        "--evaluation-time",
        help=(
            "Controlled ISO 8601 evaluation time. "
            "If omitted, current UTC time is used."
        )
    )

    args = parser.parse_args()

    case_data = load_json(args.input)

    if args.evaluation_time:
        evaluation_time = parse_timestamp(
            args.evaluation_time
        )
    else:
        evaluation_time = datetime.now(
            timezone.utc
        )

    result = monitor_case(
        case_data,
        evaluation_time
    )

    output_path = Path(args.output)

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(
        output_path,
        "w",
        encoding="utf-8"
    ) as file:
        json.dump(
            result,
            file,
            indent=4
        )

    print("SLA monitoring completed.")
    print(f"Case ID: {result['case_id']}")
    print(f"Priority: {result['priority']}")
    print(
        f"SLA Status: "
        f"{result['sla']['status']}"
    )
    print(
        f"Remaining Minutes: "
        f"{result['sla']['remaining_minutes']}"
    )
    print(
        f"Escalation Required: "
        f"{result['escalation']['required']}"
    )
    print(
        f"Escalation Level: "
        f"{result['escalation']['level']}"
    )
    print(f"Output: {output_path}")


if __name__ == "__main__":
    main()