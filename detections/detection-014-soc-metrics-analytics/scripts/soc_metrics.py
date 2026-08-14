import argparse
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path


def percentage(part, total):
    if not total:
        return 0.0

    return round((part / total) * 100, 2)


def calculate_metrics(data):
    dedup = data.get("deduplication") or {}
    sla_records = data.get("sla_evaluations") or []
    risk_records = data.get("risk_assessments") or []
    response_records = data.get("response_decisions") or []
    timeline = data.get("timeline") or {}

    alerts_processed = int(
        dedup.get("alerts_processed") or 0
    )

    incidents_created = int(
        dedup.get("incidents_created") or 0
    )

    correlated_alerts = int(
        dedup.get("correlated_alerts") or 0
    )

    deduplication_rate = percentage(
        correlated_alerts,
        alerts_processed
    )

    incident_creation_rate = percentage(
        incidents_created,
        alerts_processed
    )

    sla_counter = Counter(
        str(record.get("status", "UNKNOWN")).upper()
        for record in sla_records
    )

    sla_total = len(sla_records)

    within_sla = sla_counter.get(
        "WITHIN_SLA",
        0
    )

    at_risk = sla_counter.get(
        "AT_RISK",
        0
    )

    breached = sla_counter.get(
        "BREACHED",
        0
    )

    sla_compliance_rate = percentage(
        within_sla,
        sla_total
    )

    sla_breach_rate = percentage(
        breached,
        sla_total
    )

    risk_counter = Counter(
        str(record.get("level", "UNKNOWN")).upper()
        for record in risk_records
    )

    risk_scores = [
        float(record.get("score") or 0)
        for record in risk_records
    ]

    average_risk_score = (
        round(
            sum(risk_scores) / len(risk_scores),
            2
        )
        if risk_scores
        else 0.0
    )

    highest_risk_score = (
        max(risk_scores)
        if risk_scores
        else 0.0
    )

    escalated_responses = sum(
        1
        for record in response_records
        if record.get("escalation_required") is True
    )

    response_total = len(
        response_records
    )

    escalation_rate = percentage(
        escalated_responses,
        response_total
    )

    urgency_counter = Counter(
        str(record.get("urgency", "UNKNOWN")).upper()
        for record in response_records
    )

    return {
        "generated_at_utc": datetime.now(
            timezone.utc
        ).isoformat(),

        "dataset": data.get("dataset"),

        "alert_metrics": {
            "alerts_processed": alerts_processed,
            "incidents_created": incidents_created,
            "correlated_alerts": correlated_alerts,
            "deduplication_rate_percent": deduplication_rate,
            "incident_creation_rate_percent": incident_creation_rate
        },

        "sla_metrics": {
            "evaluations": sla_total,
            "within_sla": within_sla,
            "at_risk": at_risk,
            "breached": breached,
            "sla_compliance_rate_percent": sla_compliance_rate,
            "sla_breach_rate_percent": sla_breach_rate
        },

        "risk_metrics": {
            "assessments": len(risk_records),
            "average_risk_score": average_risk_score,
            "highest_risk_score": highest_risk_score,
            "risk_level_distribution": dict(
                risk_counter
            )
        },

        "response_metrics": {
            "decisions": response_total,
            "escalated_decisions": escalated_responses,
            "escalation_rate_percent": escalation_rate,
            "urgency_distribution": dict(
                urgency_counter
            )
        },

        "timeline_metrics": {
            "event_count": timeline.get(
                "event_count",
                0
            ),
            "total_timeline_duration_minutes": timeline.get(
                "total_timeline_duration_minutes",
                0
            ),
            "timeline_start_utc": timeline.get(
                "timeline_start_utc"
            ),
            "timeline_end_utc": timeline.get(
                "timeline_end_utc"
            )
        }
    }


def generate_markdown(metrics):
    alert = metrics["alert_metrics"]
    sla = metrics["sla_metrics"]
    risk = metrics["risk_metrics"]
    response = metrics["response_metrics"]
    timeline = metrics["timeline_metrics"]

    lines = [
        "# Automated SOC Metrics & Analytics Report",
        "",
        f"Generated: {metrics['generated_at_utc']}",
        "",
        "## Alert and Incident Metrics",
        "",
        f"- Alerts processed: {alert['alerts_processed']}",
        f"- Incidents created: {alert['incidents_created']}",
        f"- Correlated alerts: {alert['correlated_alerts']}",
        (
            "- Deduplication rate: "
            f"{alert['deduplication_rate_percent']}%"
        ),
        (
            "- Incident creation rate: "
            f"{alert['incident_creation_rate_percent']}%"
        ),
        "",
        "## SLA Metrics",
        "",
        f"- SLA evaluations: {sla['evaluations']}",
        f"- Within SLA: {sla['within_sla']}",
        f"- At risk: {sla['at_risk']}",
        f"- Breached: {sla['breached']}",
        (
            "- SLA compliance rate: "
            f"{sla['sla_compliance_rate_percent']}%"
        ),
        (
            "- SLA breach rate: "
            f"{sla['sla_breach_rate_percent']}%"
        ),
        "",
        "## Risk Metrics",
        "",
        f"- Risk assessments: {risk['assessments']}",
        (
            "- Average risk score: "
            f"{risk['average_risk_score']}"
        ),
        (
            "- Highest risk score: "
            f"{risk['highest_risk_score']}"
        ),
        (
            "- Risk distribution: "
            f"{risk['risk_level_distribution']}"
        ),
        "",
        "## Response Metrics",
        "",
        f"- Response decisions: {response['decisions']}",
        (
            "- Escalated decisions: "
            f"{response['escalated_decisions']}"
        ),
        (
            "- Escalation rate: "
            f"{response['escalation_rate_percent']}%"
        ),
        (
            "- Urgency distribution: "
            f"{response['urgency_distribution']}"
        ),
        "",
        "## Timeline Metrics",
        "",
        f"- Timeline events: {timeline['event_count']}",
        (
            "- Total observed timeline duration: "
            f"{timeline['total_timeline_duration_minutes']} minutes"
        ),
        f"- Timeline start: {timeline['timeline_start_utc']}",
        f"- Timeline end: {timeline['timeline_end_utc']}",
        "",
        "## Interpretation Note",
        "",
        (
            "Timeline duration represents the elapsed time across "
            "the generated lab artifacts. It is not presented as "
            "production MTTD or MTTR."
        )
    ]

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Automated SOC metrics and analytics engine"
    )

    parser.add_argument(
        "--input",
        required=True,
        help="SOC metrics evidence JSON"
    )

    parser.add_argument(
        "--json-output",
        required=True,
        help="Metrics JSON output"
    )

    parser.add_argument(
        "--markdown-output",
        required=True,
        help="Metrics Markdown report"
    )

    args = parser.parse_args()

    with open(
        args.input,
        "r",
        encoding="utf-8-sig"
    ) as file:
        data = json.load(file)

    metrics = calculate_metrics(
        data
    )

    json_path = Path(
        args.json_output
    )

    markdown_path = Path(
        args.markdown_output
    )

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
            metrics,
            file,
            indent=4
        )

    with open(
        markdown_path,
        "w",
        encoding="utf-8"
    ) as file:
        file.write(
            generate_markdown(metrics)
        )

    print(
        f"SOC metrics JSON generated: {json_path}"
    )

    print(
        f"SOC metrics report generated: {markdown_path}"
    )


if __name__ == "__main__":
    main()