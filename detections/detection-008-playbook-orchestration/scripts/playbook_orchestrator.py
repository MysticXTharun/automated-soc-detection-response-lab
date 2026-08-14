import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


def run_command(command, step_name):
    print(f"[START] {step_name}")

    result = subprocess.run(
        command,
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        print(f"[FAILED] {step_name}")

        if result.stdout:
            print(result.stdout)

        if result.stderr:
            print(result.stderr)

        raise RuntimeError(
            f"{step_name} failed with exit code "
            f"{result.returncode}"
        )

    print(f"[SUCCESS] {step_name}")

    return result


def load_json(path):
    with open(path, "r", encoding="utf-8-sig") as file:
        return json.load(file)


def main():
    parser = argparse.ArgumentParser(
        description=(
            "Orchestrate the Automated SOC Detection "
            "& Response Lab workflow"
        )
    )

    parser.add_argument(
        "--alert",
        required=True,
        help="Original Wazuh alert JSON"
    )

    parser.add_argument(
        "--assets",
        required=True,
        help="Asset context JSON"
    )

    parser.add_argument(
        "--response",
        required=True,
        help="Containment response JSON"
    )

    parser.add_argument(
        "--output-dir",
        required=True,
        help="Directory for playbook-generated artifacts"
    )

    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[3]

    output_dir = Path(args.output_dir)
    output_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    python_executable = sys.executable

    enrichment_script = (
        repo_root
        / "detections"
        / "detection-003-ioc-enrichment"
        / "scripts"
        / "ioc_enrichment.py"
    )

    triage_script = (
        repo_root
        / "detections"
        / "detection-005-automated-alert-triage"
        / "scripts"
        / "alert_triage.py"
    )

    report_script = (
        repo_root
        / "detections"
        / "detection-004-automated-incident-reporting"
        / "scripts"
        / "incident_report_generator.py"
    )

    case_script = (
        repo_root
        / "detections"
        / "detection-006-automated-case-management"
        / "scripts"
        / "case_manager.py"
    )

    notification_script = (
        repo_root
        / "detections"
        / "detection-007-soc-notification-escalation"
        / "scripts"
        / "notification_engine.py"
    )

    enrichment_output = (
        output_dir / "01-enrichment.json"
    )

    triage_output = (
        output_dir / "02-triage.json"
    )

    incident_report = (
        output_dir / "03-incident-report.md"
    )

    case_output = (
        output_dir / "04-case.json"
    )

    notification_output = (
        output_dir / "05-notification.json"
    )

    # Detection 003
    enrichment_result = run_command(
        [
            python_executable,
            str(enrichment_script),
            "--alert",
            str(Path(args.alert).resolve())
        ],
        "IOC Enrichment"
    )

    enrichment_output.write_text(
        enrichment_result.stdout,
        encoding="utf-8"
    )

    # Detection 005
    triage_result = run_command(
        [
            python_executable,
            str(triage_script),
            "--input",
            str(enrichment_output),
            "--assets",
            str(Path(args.assets).resolve()),
            "--response",
            str(Path(args.response).resolve())
        ],
        "Automated Alert Triage"
    )

    triage_output.write_text(
        triage_result.stdout,
        encoding="utf-8"
    )

    # Detection 004
    run_command(
        [
            python_executable,
            str(report_script),
            "--input",
            str(enrichment_output),
            "--output",
            str(incident_report)
        ],
        "Automated Incident Reporting"
    )

    # Detection 006
    run_command(
        [
            python_executable,
            str(case_script),
            "--input",
            str(triage_output),
            "--output",
            str(case_output)
        ],
        "Automated Case Management"
    )

    # Detection 007
    run_command(
        [
            python_executable,
            str(notification_script),
            "--input",
            str(case_output),
            "--output",
            str(notification_output)
        ],
        "SOC Notification and Escalation"
    )

    triage_data = load_json(triage_output)
    case_data = load_json(case_output)
    notification_data = load_json(
        notification_output
    )

    summary = {
        "playbook": (
            "Automated SOC Detection & Response"
        ),
        "execution_timestamp_utc": datetime.now(
            timezone.utc
        ).isoformat(),
        "status": "COMPLETED",
        "rule_id": (
            triage_data
            .get("alert", {})
            .get("rule_id")
        ),
        "priority": (
            triage_data
            .get("triage_result", {})
            .get("priority")
        ),
        "case_id": case_data.get("case_id"),
        "case_status": case_data.get(
            "case_status"
        ),
        "notification_level": (
            notification_data
            .get("notification", {})
            .get("level")
        ),
        "escalation_required": (
            notification_data
            .get("escalation", {})
            .get("required")
        ),
        "escalation_level": (
            notification_data
            .get("escalation", {})
            .get("level")
        ),
        "artifacts": {
            "enrichment": str(
                enrichment_output
            ),
            "triage": str(triage_output),
            "incident_report": str(
                incident_report
            ),
            "case": str(case_output),
            "notification": str(
                notification_output
            )
        }
    }

    summary_output = (
        output_dir / "playbook-summary.json"
    )

    with open(
        summary_output,
        "w",
        encoding="utf-8"
    ) as file:
        json.dump(
            summary,
            file,
            indent=4
        )

    print()
    print("=== PLAYBOOK COMPLETED ===")
    print(
        f"Rule ID: {summary['rule_id']}"
    )
    print(
        f"Priority: {summary['priority']}"
    )
    print(
        f"Case ID: {summary['case_id']}"
    )
    print(
        "Notification Level: "
        f"{summary['notification_level']}"
    )
    print(
        "Escalation Required: "
        f"{summary['escalation_required']}"
    )
    print(
        "Summary: "
        f"{summary_output}"
    )


if __name__ == "__main__":
    main()