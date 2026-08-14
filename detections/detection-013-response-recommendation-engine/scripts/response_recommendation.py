import argparse
import json
from datetime import datetime, timezone
from pathlib import Path


def normalize(value):
    if value is None:
        return ""
    return str(value).strip().upper()


def add_unique(items, value):
    if value and value not in items:
        items.append(value)


def determine_urgency(
    risk_level,
    priority,
    containment_status,
    sla_status
):
    if (
        risk_level == "CRITICAL"
        or priority == "P1"
        or containment_status == "FAILED"
        or sla_status == "BREACHED"
    ):
        return "IMMEDIATE"

    if (
        risk_level == "HIGH"
        or priority == "P2"
        or sla_status == "AT_RISK"
    ):
        return "HIGH"

    if risk_level == "MEDIUM" or priority == "P3":
        return "STANDARD"

    return "LOW"


def determine_escalation(
    risk_level,
    priority,
    containment_status,
    sla_status
):
    if sla_status == "BREACHED":
        return {
            "required": True,
            "level": "Management Escalation",
            "reason": "Incident SLA has been breached"
        }

    if containment_status == "FAILED":
        return {
            "required": True,
            "level": "L2/L3 Escalation",
            "reason": "Automated containment failed"
        }

    if risk_level == "CRITICAL" or priority == "P1":
        return {
            "required": True,
            "level": "L2/L3 Escalation",
            "reason": "Critical incident context requires senior analyst review"
        }

    if (
        risk_level == "HIGH"
        or priority == "P2"
        or sla_status == "AT_RISK"
    ):
        return {
            "required": True,
            "level": "SOC Lead Escalation",
            "reason": "Elevated incident context requires expedited review"
        }

    return {
        "required": False,
        "level": "No Immediate Escalation",
        "reason": "Current incident context supports standard analyst review"
    }


def build_recommendations(data):
    context = data.get("incident_context") or {}
    containment = data.get("containment") or {}
    sla = data.get("sla") or {}
    asset = data.get("asset_context") or {}
    mitre = data.get("mitre_context") or {}
    correlation = data.get("correlation") or {}

    risk_score = context.get("risk_score", 0)
    risk_level = normalize(context.get("risk_level"))
    priority = normalize(context.get("priority"))
    case_status = context.get("case_status")

    containment_status = normalize(
        containment.get("status")
    )

    sla_status = normalize(
        sla.get("status")
    )

    asset_criticality = normalize(
        asset.get("criticality")
    )

    alert_count = correlation.get(
        "alert_count",
        0
    ) or 0

    duplicate_alerts = correlation.get(
        "duplicate_alerts",
        0
    ) or 0

    technique_ids = (
        mitre.get("technique_ids", [])
        if isinstance(mitre, dict)
        else []
    )

    urgency = determine_urgency(
        risk_level,
        priority,
        containment_status,
        sla_status
    )

    escalation = determine_escalation(
        risk_level,
        priority,
        containment_status,
        sla_status
    )

    investigation_actions = []
    containment_actions = []
    evidence_actions = []
    closure_actions = []

    add_unique(
        investigation_actions,
        "Review the originating security alert and validate the detection context"
    )

    add_unique(
        investigation_actions,
        "Review source and destination activity around the detection timestamp"
    )

    if technique_ids:
        add_unique(
            investigation_actions,
            "Investigate activity associated with MITRE ATT&CK techniques: "
            + ", ".join(technique_ids)
        )

    if alert_count > 1:
        add_unique(
            investigation_actions,
            "Review correlated alerts to determine whether activity is repeated or expanding"
        )

    if duplicate_alerts > 0:
        add_unique(
            investigation_actions,
            "Validate that correlated duplicate alerts belong to the same incident"
        )

    if asset_criticality in ("HIGH", "CRITICAL"):
        add_unique(
            investigation_actions,
            "Prioritize investigation because the affected asset has elevated business criticality"
        )

    if containment_status == "FAILED":
        add_unique(
            containment_actions,
            "Perform manual containment immediately"
        )
        add_unique(
            containment_actions,
            "Validate endpoint and network isolation controls"
        )
        add_unique(
            containment_actions,
            "Confirm whether suspicious activity remains active after containment attempts"
        )

    elif containment_status == "SUCCESS":
        add_unique(
            containment_actions,
            "Validate that automated containment remains effective"
        )
        add_unique(
            containment_actions,
            "Confirm that no additional suspicious activity is observed after containment"
        )

    else:
        add_unique(
            containment_actions,
            "Determine containment status before incident closure"
        )

    add_unique(
        evidence_actions,
        "Preserve the original alert and enrichment results"
    )

    add_unique(
        evidence_actions,
        "Preserve triage, case-management, notification, SLA, and risk-scoring artifacts"
    )

    add_unique(
        evidence_actions,
        "Record analyst findings and response actions in the incident case"
    )

    if sla_status == "AT_RISK":
        add_unique(
            investigation_actions,
            "Expedite investigation because the case is approaching its SLA deadline"
        )

    elif sla_status == "BREACHED":
        add_unique(
            investigation_actions,
            "Document the SLA breach and prioritize immediate case review"
        )

    if risk_level == "CRITICAL":
        add_unique(
            investigation_actions,
            "Initiate full incident-response investigation for critical-risk activity"
        )

    if (
        containment_status == "SUCCESS"
        and risk_level not in ("HIGH", "CRITICAL")
        and sla_status != "BREACHED"
    ):
        add_unique(
            closure_actions,
            "Consider closure only after analyst validation confirms no additional suspicious activity"
        )
    else:
        add_unique(
            closure_actions,
            "Keep the case open until investigation, containment, and escalation requirements are completed"
        )

    if escalation["required"]:
        analyst_summary = (
            f"{urgency} response recommended. "
            f"{escalation['level']} is required because "
            f"{escalation['reason'].lower()}."
        )
    else:
        analyst_summary = (
            f"{urgency} analyst review recommended. "
            "Continue investigation and validate containment "
            "before considering case closure."
        )

    return {
        "recommendation_timestamp_utc": datetime.now(
            timezone.utc
        ).isoformat(),
        "incident_id": data.get("incident_id"),
        "case_id": data.get("case_id"),
        "input_context": {
            "risk_score": risk_score,
            "risk_level": risk_level,
            "priority": priority,
            "case_status": case_status,
            "asset_criticality": asset_criticality,
            "containment_status": containment_status,
            "sla_status": sla_status,
            "alert_count": alert_count,
            "duplicate_alerts": duplicate_alerts,
            "mitre_techniques": technique_ids
        },
        "response_decision": {
            "urgency": urgency,
            "escalation_required": escalation["required"],
            "escalation_level": escalation["level"]
        },
        "investigation_actions": investigation_actions,
        "containment_actions": containment_actions,
        "evidence_collection_actions": evidence_actions,
        "closure_guidance": closure_actions,
        "analyst_summary": analyst_summary
    }


def main():
    parser = argparse.ArgumentParser(
        description=(
            "Automated SOC incident response "
            "recommendation engine"
        )
    )

    parser.add_argument(
        "--input",
        required=True,
        help="Incident context JSON"
    )

    parser.add_argument(
        "--output",
        required=True,
        help="Recommendation JSON output"
    )

    args = parser.parse_args()

    with open(
        args.input,
        "r",
        encoding="utf-8-sig"
    ) as file:
        data = json.load(file)

    result = build_recommendations(data)

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

    print(
        f"Response recommendation generated: {output_path}"
    )


if __name__ == "__main__":
    main()