import argparse
import json
from datetime import datetime, timezone


def severity_score(level):
    level = int(level)

    if level >= 12:
        return 25
    elif level >= 8:
        return 20
    elif level >= 4:
        return 12
    else:
        return 5


def ioc_score(risk):
    scores = {
        "CRITICAL": 20,
        "HIGH": 16,
        "MEDIUM": 10,
        "LOW": 5,
        "UNKNOWN": 2,
        "INFO": 0
    }

    return scores.get(str(risk).upper(), 2)


def mitre_score(technique_ids):
    technique_scores = {
        "T1046": 8
    }

    scores = [
        technique_scores.get(technique, 5)
        for technique in technique_ids
    ]

    return min(max(scores, default=0), 15)


def asset_score(criticality):
    scores = {
        "CRITICAL": 15,
        "HIGH": 12,
        "MEDIUM": 8,
        "LOW": 3,
        "UNKNOWN": 0
    }

    return scores.get(str(criticality).upper(), 0)


def containment_score(status):
    scores = {
        "FAILED": 15,
        "NOT_ATTEMPTED": 8,
        "UNKNOWN": 5,
        "SUCCESS": 0
    }

    return scores.get(str(status).upper(), 5)


def sla_score(status):
    scores = {
        "BREACHED": 10,
        "AT_RISK": 5,
        "WITHIN_SLA": 0
    }

    return scores.get(str(status).upper(), 0)


def correlation_score(alert_count):
    alert_count = int(alert_count)

    if alert_count >= 10:
        return 10
    elif alert_count >= 5:
        return 7
    elif alert_count >= 2:
        return 4
    else:
        return 0


def determine_risk_level(score):
    if score >= 75:
        return "CRITICAL"
    elif score >= 50:
        return "HIGH"
    elif score >= 30:
        return "MEDIUM"
    else:
        return "LOW"


def determine_action(risk_level):
    actions = {
        "CRITICAL": (
            "Immediate SOC escalation, containment validation, "
            "and incident-response investigation required"
        ),
        "HIGH": (
            "Prioritize SOC investigation and validate containment "
            "and related activity"
        ),
        "MEDIUM": (
            "Standard SOC investigation with contextual validation"
        ),
        "LOW": (
            "Monitor and perform routine analyst validation"
        )
    }

    return actions[risk_level]


def calculate_risk(data):
    components = {
        "wazuh_severity": severity_score(
            data["alert"]["rule_level"]
        ),
        "ioc_risk": ioc_score(
            data["ioc_assessment"]["risk_level"]
        ),
        "mitre_context": mitre_score(
            data["mitre_context"]["technique_ids"]
        ),
        "asset_criticality": asset_score(
            data["asset_context"]["criticality"]
        ),
        "containment_status": containment_score(
            data["containment"]["status"]
        ),
        "sla_status": sla_score(
            data["sla"]["status"]
        ),
        "correlated_activity": correlation_score(
            data["correlation"]["alert_count"]
        )
    }

    raw_score = sum(components.values())
    final_score = max(0, min(raw_score, 100))

    risk_level = determine_risk_level(final_score)

    return {
        "evaluation_timestamp_utc": datetime.now(
            timezone.utc
        ).isoformat(),
        "incident_id": data["incident_id"],
        "case_id": data["case_id"],
        "rule_id": data["alert"]["rule_id"],
        "risk_score": final_score,
        "risk_level": risk_level,
        "recommended_action": determine_action(risk_level),
        "risk_components": components,
        "context": {
            "source_ip": data["alert"]["source_ip"],
            "destination_ip": data["alert"]["destination_ip"],
            "destination_port": data["alert"]["destination_port"],
            "mitre_ids": data["mitre_context"]["technique_ids"],
            "asset_criticality": data[
                "asset_context"
            ]["criticality"],
            "containment_status": data[
                "containment"
            ]["status"],
            "sla_status": data["sla"]["status"],
            "alert_count": data[
                "correlation"
            ]["alert_count"]
        }
    }


def main():
    parser = argparse.ArgumentParser(
        description="Automated SOC incident risk scoring engine"
    )

    parser.add_argument(
        "--input",
        required=True,
        help="Input incident context JSON"
    )

    parser.add_argument(
        "--output",
        required=True,
        help="Output risk assessment JSON"
    )

    args = parser.parse_args()

    with open(args.input, "r", encoding="utf-8-sig") as file:
        data = json.load(file)

    result = calculate_risk(data)

    with open(args.output, "w", encoding="utf-8") as file:
        json.dump(result, file, indent=4)

    print(f"Incident risk assessment generated: {args.output}")


if __name__ == "__main__":
    main()