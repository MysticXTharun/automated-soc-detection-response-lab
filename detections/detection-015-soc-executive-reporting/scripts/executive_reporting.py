import argparse
import json
from datetime import datetime, timezone
from pathlib import Path


def safe_dict(value):
    return value if isinstance(value, dict) else {}


def safe_list(value):
    return value if isinstance(value, list) else []


def build_report(data):
    sources = safe_dict(data.get("source_context"))

    case = safe_dict(sources.get("case_management"))
    dedup = safe_dict(sources.get("incident_deduplication"))
    sla_result = safe_dict(sources.get("sla_monitoring"))
    risk = safe_dict(sources.get("incident_risk"))
    timeline = safe_dict(sources.get("incident_timeline"))
    response = safe_dict(sources.get("response_recommendation"))
    metrics = safe_dict(sources.get("soc_metrics"))

    sla = safe_dict(sla_result.get("sla"))
    sla_escalation = safe_dict(sla_result.get("escalation"))
    response_decision = safe_dict(response.get("response_decision"))

    alert_metrics = safe_dict(metrics.get("alert_metrics"))
    sla_metrics = safe_dict(metrics.get("sla_metrics"))
    risk_metrics = safe_dict(metrics.get("risk_metrics"))
    response_metrics = safe_dict(metrics.get("response_metrics"))
    timeline_metrics = safe_dict(metrics.get("timeline_metrics"))

    dedup_results = safe_list(dedup.get("results"))

    correlated_alerts = sum(
        1
        for result in dedup_results
        if str(result.get("decision", "")).upper() == "CORRELATED"
    )

    new_incidents = sum(
        1
        for result in dedup_results
        if str(result.get("decision", "")).upper() == "NEW"
    )

    risk_score = risk.get("risk_score")
    risk_level = risk.get("risk_level")

    escalation_required = bool(
        response_decision.get("escalation_required", False)
    )

    escalation_level = response_decision.get(
        "escalation_level",
        "No Immediate Escalation"
    )

    urgency = response_decision.get(
        "urgency",
        "STANDARD"
    )

    sla_status = sla.get(
        "status",
        "UNKNOWN"
    )

    executive_status = "MONITOR"

    if str(sla_status).upper() == "BREACHED":
        executive_status = "CRITICAL ATTENTION REQUIRED"
    elif str(risk_level).upper() == "CRITICAL":
        executive_status = "CRITICAL ATTENTION REQUIRED"
    elif escalation_required:
        executive_status = "ESCALATION REQUIRED"
    elif str(risk_level).upper() == "HIGH":
        executive_status = "PRIORITY REVIEW REQUIRED"

    report = {
        "generated_at_utc": datetime.now(
            timezone.utc
        ).isoformat(),

        "report_name": data.get(
            "report_name",
            "SOC Executive Report"
        ),

        "executive_status": executive_status,

        "incident_overview": {
            "case_id": case.get("case_id"),
            "case_status": case.get("case_status"),
            "priority": case.get("priority"),
            "assigned_queue": case.get("assigned_queue"),
            "risk_score": risk_score,
            "risk_level": risk_level,
            "sla_status": sla_status,
            "response_urgency": urgency
        },

        "escalation_summary": {
            "required": escalation_required,
            "level": escalation_level,
            "sla_escalation_required": bool(
                sla_escalation.get("required", False)
            ),
            "sla_escalation_level": sla_escalation.get(
                "level",
                "No Escalation"
            ),
            "reason": sla_escalation.get("reason")
        },

        "correlation_summary": {
            "alerts_processed": len(dedup_results),
            "new_incidents": new_incidents,
            "correlated_alerts": correlated_alerts
        },

        "soc_metrics": {
            "alerts_processed": alert_metrics.get(
                "alerts_processed"
            ),
            "incidents_created": alert_metrics.get(
                "incidents_created"
            ),
            "deduplication_rate_percent": alert_metrics.get(
                "deduplication_rate_percent"
            ),
            "sla_compliance_rate_percent": sla_metrics.get(
                "sla_compliance_rate_percent"
            ),
            "sla_breach_rate_percent": sla_metrics.get(
                "sla_breach_rate_percent"
            ),
            "average_risk_score": risk_metrics.get(
                "average_risk_score"
            ),
            "highest_risk_score": risk_metrics.get(
                "highest_risk_score"
            ),
            "escalation_rate_percent": response_metrics.get(
                "escalation_rate_percent"
            )
        },

        "timeline_summary": {
            "event_count": timeline_metrics.get(
                "event_count"
            ),
            "timeline_start_utc": timeline_metrics.get(
                "timeline_start_utc"
            ),
            "timeline_end_utc": timeline_metrics.get(
                "timeline_end_utc"
            ),
            "observed_duration_minutes": timeline_metrics.get(
                "total_timeline_duration_minutes"
            )
        },

        "management_summary": (
            f"Incident risk is {risk_level} with a score of "
            f"{risk_score}. SLA state is {sla_status}. "
            f"Response urgency is {urgency}. "
            f"Escalation required: {escalation_required}. "
            f"Current escalation level: {escalation_level}."
        ),

        "interpretation_note": (
            "Metrics are generated from controlled SOC lab scenarios "
            "and demonstrate reporting logic rather than production "
            "SOC performance."
        )
    }

    return report


def generate_markdown(report):
    incident = report["incident_overview"]
    escalation = report["escalation_summary"]
    metrics = report["soc_metrics"]
    correlation = report["correlation_summary"]
    timeline = report["timeline_summary"]

    lines = [
        "# SOC Executive Incident Report",
        "",
        f"Generated: {report['generated_at_utc']}",
        "",
        "## Executive Status",
        "",
        f"**{report['executive_status']}**",
        "",
        "## Management Summary",
        "",
        report["management_summary"],
        "",
        "## Incident Overview",
        "",
        "| Field | Value |",
        "|---|---|",
        f"| Case ID | {incident['case_id']} |",
        f"| Case Status | {incident['case_status']} |",
        f"| Priority | {incident['priority']} |",
        f"| Assigned Queue | {incident['assigned_queue']} |",
        f"| Risk Score | {incident['risk_score']} |",
        f"| Risk Level | {incident['risk_level']} |",
        f"| SLA Status | {incident['sla_status']} |",
        f"| Response Urgency | {incident['response_urgency']} |",
        "",
        "## Escalation Summary",
        "",
        f"- Escalation required: {escalation['required']}",
        f"- Escalation level: {escalation['level']}",
        (
            "- SLA escalation required: "
            f"{escalation['sla_escalation_required']}"
        ),
        (
            "- SLA escalation level: "
            f"{escalation['sla_escalation_level']}"
        ),
        f"- Reason: {escalation['reason']}",
        "",
        "## Correlation Summary",
        "",
        f"- Alerts processed: {correlation['alerts_processed']}",
        f"- New incidents: {correlation['new_incidents']}",
        f"- Correlated alerts: {correlation['correlated_alerts']}",
        "",
        "## SOC Metrics",
        "",
        (
            "- Deduplication rate: "
            f"{metrics['deduplication_rate_percent']}%"
        ),
        (
            "- SLA compliance rate: "
            f"{metrics['sla_compliance_rate_percent']}%"
        ),
        (
            "- SLA breach rate: "
            f"{metrics['sla_breach_rate_percent']}%"
        ),
        (
            "- Average risk score: "
            f"{metrics['average_risk_score']}"
        ),
        (
            "- Highest risk score: "
            f"{metrics['highest_risk_score']}"
        ),
        (
            "- Escalation rate: "
            f"{metrics['escalation_rate_percent']}%"
        ),
        "",
        "## Timeline Summary",
        "",
        f"- Events: {timeline['event_count']}",
        f"- Start: {timeline['timeline_start_utc']}",
        f"- End: {timeline['timeline_end_utc']}",
        (
            "- Observed duration: "
            f"{timeline['observed_duration_minutes']} minutes"
        ),
        "",
        "## Interpretation",
        "",
        report["interpretation_note"]
    ]

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="SOC executive reporting engine"
    )

    parser.add_argument(
        "--input",
        required=True
    )

    parser.add_argument(
        "--json-output",
        required=True
    )

    parser.add_argument(
        "--markdown-output",
        required=True
    )

    args = parser.parse_args()

    with open(
        args.input,
        "r",
        encoding="utf-8-sig"
    ) as file:
        data = json.load(file)

    report = build_report(data)

    json_path = Path(args.json_output)
    markdown_path = Path(args.markdown_output)

    json_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    markdown_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(
        json_path,
        "w",
        encoding="utf-8"
    ) as file:
        json.dump(
            report,
            file,
            indent=4
        )

    with open(
        markdown_path,
        "w",
        encoding="utf-8"
    ) as file:
        file.write(
            generate_markdown(report)
        )

    print(
        f"Executive dashboard JSON generated: {json_path}"
    )

    print(
        f"Executive report generated: {markdown_path}"
    )


if __name__ == "__main__":
    main()