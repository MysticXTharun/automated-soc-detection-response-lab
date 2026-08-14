import argparse
import json
from datetime import datetime, timezone
from pathlib import Path


def parse_timestamp(value):
    if not value:
        raise ValueError("Missing timestamp")

    value = str(value).strip()

    # Handle timestamps ending in Z.
    if value.endswith("Z"):
        value = value[:-1] + "+00:00"

    # Handle offsets such as +0000.
    if (
        len(value) >= 5
        and value[-5] in ("+", "-")
        and value[-3] != ":"
    ):
        value = value[:-2] + ":" + value[-2:]

    parsed = datetime.fromisoformat(value)

    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)

    return parsed.astimezone(timezone.utc)


def format_timestamp(timestamp):
    return timestamp.isoformat()


def reconstruct_timeline(data):
    normalized_events = []

    for event in data["events"]:
        parsed_time = parse_timestamp(
            event["timestamp_utc"]
        )

        normalized_events.append({
            "parsed_time": parsed_time,
            "event_type": event["event_type"],
            "source": event["source"],
            "description": event["description"]
        })

    normalized_events.sort(
        key=lambda event: event["parsed_time"]
    )

    first_time = normalized_events[0]["parsed_time"]
    previous_time = None

    reconstructed_events = []

    for sequence, event in enumerate(
        normalized_events,
        start=1
    ):
        current_time = event["parsed_time"]

        elapsed_seconds = (
            current_time - first_time
        ).total_seconds()

        if previous_time is None:
            gap_seconds = 0
        else:
            gap_seconds = (
                current_time - previous_time
            ).total_seconds()

        reconstructed_events.append({
            "sequence": sequence,
            "timestamp_utc": format_timestamp(
                current_time
            ),
            "event_type": event["event_type"],
            "source": event["source"],
            "description": event["description"],
            "elapsed_from_initial_event_seconds": round(
                elapsed_seconds,
                3
            ),
            "elapsed_from_initial_event_minutes": round(
                elapsed_seconds / 60,
                2
            ),
            "gap_from_previous_event_seconds": round(
                gap_seconds,
                3
            ),
            "gap_from_previous_event_minutes": round(
                gap_seconds / 60,
                2
            )
        })

        previous_time = current_time

    total_duration_seconds = (
        normalized_events[-1]["parsed_time"]
        - first_time
    ).total_seconds()

    return {
        "reconstruction_timestamp_utc": datetime.now(
            timezone.utc
        ).isoformat(),
        "incident_id": data.get("incident_id"),
        "case_id": data.get("case_id"),
        "rule_id": data.get("rule_id"),
        "event_count": len(reconstructed_events),
        "timeline_start_utc": format_timestamp(
            normalized_events[0]["parsed_time"]
        ),
        "timeline_end_utc": format_timestamp(
            normalized_events[-1]["parsed_time"]
        ),
        "total_timeline_duration_seconds": round(
            total_duration_seconds,
            3
        ),
        "total_timeline_duration_minutes": round(
            total_duration_seconds / 60,
            2
        ),
        "events": reconstructed_events
    }


def generate_markdown(result):
    lines = []

    lines.append(
        "# Automated Incident Timeline Reconstruction"
    )
    lines.append("")
    lines.append(
        f"**Incident ID:** {result['incident_id']}"
    )
    lines.append(
        f"**Case ID:** {result['case_id']}"
    )
    lines.append(
        f"**Rule ID:** {result['rule_id']}"
    )
    lines.append(
        f"**Events:** {result['event_count']}"
    )
    lines.append(
        f"**Timeline Start:** {result['timeline_start_utc']}"
    )
    lines.append(
        f"**Timeline End:** {result['timeline_end_utc']}"
    )
    lines.append(
        "**Total Duration:** "
        f"{result['total_timeline_duration_minutes']} minutes"
    )

    lines.append("")
    lines.append("## Investigation Timeline")
    lines.append("")

    lines.append(
        "| # | Timestamp (UTC) | Event | Source | "
        "Elapsed (min) | Gap (min) |"
    )
    lines.append(
        "|---:|---|---|---|---:|---:|"
    )

    for event in result["events"]:
        lines.append(
            f"| {event['sequence']} "
            f"| {event['timestamp_utc']} "
            f"| {event['event_type']} "
            f"| {event['source']} "
            f"| {event['elapsed_from_initial_event_minutes']} "
            f"| {event['gap_from_previous_event_minutes']} |"
        )

    lines.append("")
    lines.append("## Event Details")
    lines.append("")

    for event in result["events"]:
        lines.append(
            f"### {event['sequence']}. "
            f"{event['event_type']}"
        )
        lines.append("")
        lines.append(
            f"- Timestamp: `{event['timestamp_utc']}`"
        )
        lines.append(
            f"- Source: {event['source']}"
        )
        lines.append(
            "- Elapsed from initial event: "
            f"{event['elapsed_from_initial_event_minutes']} minutes"
        )
        lines.append(
            "- Gap from previous event: "
            f"{event['gap_from_previous_event_minutes']} minutes"
        )
        lines.append(
            f"- Description: {event['description']}"
        )
        lines.append("")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description=(
            "Automated SOC incident timeline "
            "reconstruction engine"
        )
    )

    parser.add_argument(
        "--input",
        required=True,
        help="Timeline evidence JSON"
    )

    parser.add_argument(
        "--json-output",
        required=True,
        help="Reconstructed timeline JSON output"
    )

    parser.add_argument(
        "--markdown-output",
        required=True,
        help="Analyst-readable Markdown timeline"
    )

    args = parser.parse_args()

    with open(
        args.input,
        "r",
        encoding="utf-8-sig"
    ) as file:
        data = json.load(file)

    result = reconstruct_timeline(data)

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
            result,
            file,
            indent=4
        )

    with open(
        markdown_path,
        "w",
        encoding="utf-8"
    ) as file:
        file.write(
            generate_markdown(result)
        )

    print(
        f"Timeline JSON generated: {json_path}"
    )

    print(
        f"Timeline Markdown generated: {markdown_path}"
    )


if __name__ == "__main__":
    main()