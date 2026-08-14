import argparse
import hashlib
import json
from datetime import datetime
from pathlib import Path


def load_json(path):
    with open(path, "r", encoding="utf-8-sig") as file:
        return json.load(file)


def parse_timestamp(timestamp):
    return datetime.fromisoformat(
        timestamp.replace("Z", "+00:00")
    )


def generate_correlation_key(alert):
    mitre_ids = alert.get("mitre_ids", [])

    correlation_fields = [
        str(alert.get("rule_id", "")),
        str(alert.get("source_ip", "")),
        str(alert.get("destination_ip", "")),
        str(alert.get("destination_port", "")),
        ",".join(sorted(mitre_ids))
    ]

    raw_key = "|".join(correlation_fields)

    return hashlib.sha256(
        raw_key.encode("utf-8")
    ).hexdigest()[:16]


def create_incident_id(alert, correlation_key):
    timestamp = parse_timestamp(alert["timestamp"])

    return (
        f"INC-{timestamp.strftime('%Y%m%d-%H%M%S')}"
        f"-{correlation_key[:8].upper()}"
    )


def correlate_alerts(alerts, window_minutes):
    incidents = []
    results = []

    sorted_alerts = sorted(
        alerts,
        key=lambda item: parse_timestamp(
            item["timestamp"]
        )
    )

    for alert in sorted_alerts:
        alert_time = parse_timestamp(
            alert["timestamp"]
        )

        correlation_key = generate_correlation_key(
            alert
        )

        matched_incident = None
        time_difference_minutes = None

        for incident in reversed(incidents):
            if (
                incident["correlation_key"]
                != correlation_key
            ):
                continue

            last_seen = parse_timestamp(
                incident["last_seen"]
            )

            difference = (
                alert_time - last_seen
            ).total_seconds() / 60

            if 0 <= difference <= window_minutes:
                matched_incident = incident
                time_difference_minutes = round(
                    difference,
                    2
                )
                break

        if matched_incident:
            matched_incident["last_seen"] = (
                alert["timestamp"]
            )

            matched_incident["alert_count"] += 1

            matched_incident[
                "related_alert_timestamps"
            ].append(
                alert["timestamp"]
            )

            result = {
                "timestamp": alert["timestamp"],
                "rule_id": alert["rule_id"],
                "source_ip": alert["source_ip"],
                "destination_ip": (
                    alert["destination_ip"]
                ),
                "destination_port": (
                    alert["destination_port"]
                ),
                "correlation_key": correlation_key,
                "decision": "CORRELATED",
                "incident_id": (
                    matched_incident["incident_id"]
                ),
                "time_since_previous_alert_minutes": (
                    time_difference_minutes
                ),
                "reason": (
                    "Matching alert observed within "
                    f"{window_minutes}-minute "
                    "correlation window"
                )
            }

        else:
            incident_id = create_incident_id(
                alert,
                correlation_key
            )

            new_incident = {
                "incident_id": incident_id,
                "correlation_key": correlation_key,
                "rule_id": alert["rule_id"],
                "source_ip": alert["source_ip"],
                "destination_ip": (
                    alert["destination_ip"]
                ),
                "destination_port": (
                    alert["destination_port"]
                ),
                "mitre_ids": alert.get(
                    "mitre_ids",
                    []
                ),
                "first_seen": alert["timestamp"],
                "last_seen": alert["timestamp"],
                "alert_count": 1,
                "related_alert_timestamps": [
                    alert["timestamp"]
                ]
            }

            incidents.append(new_incident)

            result = {
                "timestamp": alert["timestamp"],
                "rule_id": alert["rule_id"],
                "source_ip": alert["source_ip"],
                "destination_ip": (
                    alert["destination_ip"]
                ),
                "destination_port": (
                    alert["destination_port"]
                ),
                "correlation_key": correlation_key,
                "decision": "NEW",
                "incident_id": incident_id,
                "time_since_previous_alert_minutes": None,
                "reason": (
                    "No matching incident found within "
                    f"{window_minutes}-minute "
                    "correlation window"
                )
            }

        results.append(result)

    return {
        "correlation_window_minutes": (
            window_minutes
        ),
        "alerts_processed": len(
            sorted_alerts
        ),
        "incidents_created": len(
            incidents
        ),
        "duplicates_correlated": sum(
            1
            for result in results
            if result["decision"] == "CORRELATED"
        ),
        "results": results,
        "incidents": incidents
    }


def main():
    parser = argparse.ArgumentParser(
        description=(
            "SOC incident deduplication and "
            "correlation engine"
        )
    )

    parser.add_argument(
        "--input-dir",
        required=True,
        help=(
            "Directory containing alert JSON files"
        )
    )

    parser.add_argument(
        "--output",
        required=True,
        help="Output correlation result JSON"
    )

    parser.add_argument(
        "--window",
        type=int,
        default=5,
        help=(
            "Correlation window in minutes "
            "(default: 5)"
        )
    )

    args = parser.parse_args()

    input_dir = Path(args.input_dir)

    alert_files = sorted(
        input_dir.glob("*.json")
    )

    if not alert_files:
        raise FileNotFoundError(
            f"No JSON alerts found in {input_dir}"
        )

    alerts = [
        load_json(alert_file)
        for alert_file in alert_files
    ]

    output = correlate_alerts(
        alerts,
        args.window
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
            output,
            file,
            indent=4
        )

    print("Incident deduplication completed.")
    print(
        f"Alerts processed: "
        f"{output['alerts_processed']}"
    )
    print(
        f"Incidents created: "
        f"{output['incidents_created']}"
    )
    print(
        f"Duplicates correlated: "
        f"{output['duplicates_correlated']}"
    )
    print(
        f"Output: {output_path}"
    )


if __name__ == "__main__":
    main()