import argparse
import json
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


def score_wazuh_level(level):
    try:
        level = int(level)
    except (TypeError, ValueError):
        return 0

    if level >= 12:
        return 50
    if level >= 8:
        return 40
    if level >= 4:
        return 25

    return 10


def score_ioc_risk(risk_level):
    scores = {
        "CRITICAL": 50,
        "HIGH": 40,
        "MEDIUM": 25,
        "LOW": 10,
        "INFO": 0,
        "UNKNOWN": 5
    }

    return scores.get(
        str(risk_level).upper(),
        5
    )


def score_mitre(mitre_ids):
    technique_scores = {
        "T1046": 10
    }

    if not mitre_ids:
        return 0

    if not isinstance(mitre_ids, list):
        mitre_ids = [mitre_ids]

    return max(
        (
            technique_scores.get(
                str(technique),
                5
            )
            for technique in mitre_ids
        ),
        default=0
    )


def score_asset_criticality(criticality):
    scores = {
        "CRITICAL": 30,
        "HIGH": 25,
        "MEDIUM": 15,
        "LOW": 5,
        "UNKNOWN": 0
    }

    return scores.get(
        str(criticality).upper(),
        0
    )


def score_containment(status):
    status = str(status).upper()

    if status == "SUCCESS":
        return -10

    if status == "FAILED":
        return 15

    if status == "NOT_ATTEMPTED":
        return 5

    return 0


def determine_priority(score):
    if score >= 100:
        return "P1"

    if score >= 70:
        return "P2"

    if score >= 40:
        return "P3"

    return "P4"


def recommended_action(priority, containment_status):
    containment_status = str(
        containment_status
    ).upper()

    if priority == "P1":
        return (
            "Immediate investigation and escalation "
            "to L2/L3 SOC"
        )

    if priority == "P2":
        if containment_status == "SUCCESS":
            return (
                "High-priority investigation; "
                "validate containment and scope"
            )

        return (
            "High-priority investigation and "
            "containment required"
        )

    if priority == "P3":
        return (
            "Standard SOC analyst review and "
            "validate related activity"
        )

    return "Low-priority review or monitoring"


def get_asset_context(asset_data, destination_ip):
    assets = asset_data.get("assets", {})

    return assets.get(
        destination_ip,
        {
            "hostname": "UNKNOWN",
            "asset_type": "UNKNOWN",
            "criticality": "UNKNOWN",
            "business_context": "No asset context available"
        }
    )


def triage_alert(data, asset_data, response_data):
    alert = data.get("alert_context", {})
    enrichment = data.get("enrichment", {})
    assessment = enrichment.get(
        "soc_assessment"
    ) or {}

    rule_level = alert.get("rule_level")
    risk_level = assessment.get(
        "risk_level",
        "UNKNOWN"
    )

    mitre_ids = alert.get(
        "mitre_ids",
        []
    )

    destination_ip = alert.get(
        "destination_ip"
    )

    asset = get_asset_context(
        asset_data,
        destination_ip
    )

    criticality = asset.get(
        "criticality",
        "UNKNOWN"
    )

    containment_status = response_data.get(
        "containment_status",
        "UNKNOWN"
    )

    wazuh_score = score_wazuh_level(
        rule_level
    )

    ioc_score = score_ioc_risk(
        risk_level
    )

    mitre_score = score_mitre(
        mitre_ids
    )

    asset_score = score_asset_criticality(
        criticality
    )

    containment_score = score_containment(
        containment_status
    )

    total_score = (
        wazuh_score
        + ioc_score
        + mitre_score
        + asset_score
        + containment_score
    )

    total_score = max(
        0,
        min(total_score, 100)
    )

    priority = determine_priority(
        total_score
    )

    return {
        "triage_timestamp_utc": datetime.now(
            timezone.utc
        ).isoformat(),

        "alert": {
            "timestamp": alert.get("timestamp"),
            "rule_id": alert.get("rule_id"),
            "rule_level": rule_level,
            "rule_description": alert.get(
                "rule_description"
            ),
            "source_ip": alert.get(
                "source_ip"
            ),
            "destination_ip": destination_ip,
            "destination_port": alert.get(
                "destination_port"
            ),
            "mitre_ids": mitre_ids,
            "mitre_tactics": alert.get(
                "mitre_tactics",
                []
            ),
            "mitre_techniques": alert.get(
                "mitre_techniques",
                []
            )
        },

        "ioc_assessment": {
            "verdict": assessment.get(
                "verdict",
                "UNKNOWN"
            ),
            "risk_level": risk_level,
            "reason": assessment.get(
                "reason",
                "No assessment available"
            )
        },

        "asset_context": {
            "hostname": asset.get(
                "hostname"
            ),
            "asset_type": asset.get(
                "asset_type"
            ),
            "criticality": criticality,
            "business_context": asset.get(
                "business_context"
            )
        },

        "containment": {
            "response": response_data.get(
                "response",
                "UNKNOWN"
            ),
            "status": containment_status,
            "automatic_recovery": response_data.get(
                "automatic_recovery",
                False
            )
        },

        "triage_scoring": {
            "wazuh_severity_score": wazuh_score,
            "ioc_risk_score": ioc_score,
            "mitre_technique_score": mitre_score,
            "asset_criticality_score": asset_score,
            "containment_score": containment_score,
            "total_score": total_score
        },

        "triage_result": {
            "priority": priority,
            "recommended_action": recommended_action(
                priority,
                containment_status
            )
        }
    }


def main():
    parser = argparse.ArgumentParser(
        description=(
            "Context-aware automated SOC "
            "alert triage engine"
        )
    )

    parser.add_argument(
        "--input",
        required=True,
        help="Path to enriched Wazuh alert JSON"
    )

    parser.add_argument(
        "--assets",
        required=True,
        help="Path to asset context JSON"
    )

    parser.add_argument(
        "--response",
        required=True,
        help="Path to containment response JSON"
    )

    args = parser.parse_args()

    try:
        data = load_json(args.input)
        asset_data = load_json(args.assets)
        response_data = load_json(
            args.response
        )

        result = triage_alert(
            data,
            asset_data,
            response_data
        )

        print(
            json.dumps(
                result,
                indent=4
            )
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