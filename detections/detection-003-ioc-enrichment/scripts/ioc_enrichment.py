import argparse
import ipaddress
import json
import os
import socket
import sys
from datetime import datetime, timezone
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


def reverse_dns_lookup(ip):
    try:
        return socket.gethostbyaddr(ip)[0]
    except (socket.herror, socket.gaierror):
        return "Not resolved"


def abuseipdb_lookup(ip):
    api_key = os.getenv("ABUSEIPDB_API_KEY")

    if not api_key:
        return {
            "status": "skipped",
            "reason": "ABUSEIPDB_API_KEY environment variable is not configured"
        }

    url = (
        "https://api.abuseipdb.com/api/v2/check"
        f"?ipAddress={ip}&maxAgeInDays=90&verbose=true"
    )

    request = Request(
        url,
        headers={
            "Key": api_key,
            "Accept": "application/json"
        }
    )

    try:
        with urlopen(request, timeout=10) as response:
            body = response.read().decode("utf-8")
            api_response = json.loads(body)
            data = api_response.get("data", {})

            return {
                "status": "success",
                "abuse_confidence_score": data.get("abuseConfidenceScore"),
                "country_code": data.get("countryCode"),
                "usage_type": data.get("usageType"),
                "isp": data.get("isp"),
                "domain": data.get("domain"),
                "total_reports": data.get("totalReports"),
                "last_reported_at": data.get("lastReportedAt"),
                "is_whitelisted": data.get("isWhitelisted")
            }

    except HTTPError as exc:
        return {
            "status": "error",
            "reason": f"HTTP error {exc.code}"
        }

    except URLError as exc:
        return {
            "status": "error",
            "reason": f"Network error: {exc.reason}"
        }

    except Exception as exc:
        return {
            "status": "error",
            "reason": str(exc)
        }


def calculate_verdict(classification, threat_intelligence):
    if classification != "Public IP":
        return {
            "verdict": "INTERNAL",
            "risk_level": "INFO",
            "reason": "Private or non-public IP; public reputation lookup not applicable"
        }

    if not threat_intelligence:
        return {
            "verdict": "UNKNOWN",
            "risk_level": "UNKNOWN",
            "reason": "No threat intelligence result available"
        }

    if threat_intelligence.get("status") != "success":
        return {
            "verdict": "UNKNOWN",
            "risk_level": "UNKNOWN",
            "reason": threat_intelligence.get(
                "reason",
                "Threat intelligence lookup unavailable"
            )
        }

    score = threat_intelligence.get("abuse_confidence_score") or 0
    whitelisted = threat_intelligence.get("is_whitelisted")

    if whitelisted is True:
        return {
            "verdict": "BENIGN",
            "risk_level": "LOW",
            "reason": "IP is whitelisted by the threat intelligence provider"
        }

    if score >= 75:
        return {
            "verdict": "MALICIOUS",
            "risk_level": "HIGH",
            "reason": f"High abuse confidence score: {score}"
        }

    if score >= 25:
        return {
            "verdict": "SUSPICIOUS",
            "risk_level": "MEDIUM",
            "reason": f"Elevated abuse confidence score: {score}"
        }

    return {
        "verdict": "LOW_RISK",
        "risk_level": "LOW",
        "reason": f"Low abuse confidence score: {score}"
    }


def enrich_ip(ip):
    result = {
        "ioc": ip,
        "ioc_type": "ip",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "classification": None,
        "reverse_dns": None,
        "public_threat_intel_lookup": False,
        "threat_intelligence": None,
        "soc_assessment": None
    }

    try:
        address = ipaddress.ip_address(ip)

    except ValueError:
        result["classification"] = "Invalid IP"
        result["error"] = "IOC is not a valid IPv4 or IPv6 address"

        result["soc_assessment"] = {
            "verdict": "INVALID",
            "risk_level": "UNKNOWN",
            "reason": "The supplied IOC is not a valid IP address"
        }

        return result

    result["reverse_dns"] = reverse_dns_lookup(ip)

    if address.is_loopback:
        result["classification"] = "Loopback IP"

    elif address.is_multicast:
        result["classification"] = "Multicast IP"

    elif address.is_private:
        result["classification"] = "Private IP"

    else:
        result["classification"] = "Public IP"
        result["public_threat_intel_lookup"] = True
        result["threat_intelligence"] = abuseipdb_lookup(ip)

    result["soc_assessment"] = calculate_verdict(
        result["classification"],
        result["threat_intelligence"]
    )

    return result


def extract_ioc_from_alert(alert_file):
    try:
        with open(alert_file, "r", encoding="utf-8") as file:
            alert = json.load(file)

    except FileNotFoundError:
        raise ValueError(f"Alert file not found: {alert_file}")

    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON alert file: {exc}")

    try:
        source_ip = alert["data"]["win"]["eventdata"]["sourceAddress"]

    except (KeyError, TypeError):
        raise ValueError(
            "Could not locate data.win.eventdata.sourceAddress in alert"
        )

    context = {
        "rule_id": alert.get("rule", {}).get("id"),
        "rule_level": alert.get("rule", {}).get("level"),
        "rule_description": alert.get("rule", {}).get("description"),
        "agent_id": alert.get("agent", {}).get("id"),
        "agent_name": alert.get("agent", {}).get("name"),
        "source_ip": source_ip,
        "destination_ip": (
            alert.get("data", {})
            .get("win", {})
            .get("eventdata", {})
            .get("destAddress")
        ),
        "destination_port": (
            alert.get("data", {})
            .get("win", {})
            .get("eventdata", {})
            .get("destPort")
        )
    }

    return source_ip, context


def main():
    parser = argparse.ArgumentParser(
        description="SOC IOC enrichment utility"
    )

    group = parser.add_mutually_exclusive_group(required=True)

    group.add_argument(
        "--ip",
        help="IP address to enrich"
    )

    group.add_argument(
        "--alert",
        help="Wazuh alert JSON file"
    )

    args = parser.parse_args()

    try:
        if args.alert:
            ip, alert_context = extract_ioc_from_alert(args.alert)

            output = {
                "input_type": "wazuh_alert",
                "alert_context": alert_context,
                "enrichment": enrich_ip(ip)
            }

        else:
            output = {
                "input_type": "manual_ip",
                "enrichment": enrich_ip(args.ip)
            }

        print(json.dumps(output, indent=4))

    except ValueError as exc:
        print(
            json.dumps(
                {
                    "status": "error",
                    "reason": str(exc)
                },
                indent=4
            )
        )
        sys.exit(1)


if __name__ == "__main__":
    main()