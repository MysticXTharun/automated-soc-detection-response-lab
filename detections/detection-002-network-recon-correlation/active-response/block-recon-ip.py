import sys
import json
import subprocess
import datetime

LOG_FILE = r"C:\Program Files (x86)\ossec-agent\active-response\active-responses.log"
RULE_PREFIX = "Wazuh-Recon-Block-"

def log(message):
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        timestamp = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
        f.write(f"{timestamp} block-recon-ip: {message}\n")

def run_powershell(command):
    return subprocess.run(
        ["powershell.exe", "-NoProfile", "-NonInteractive", "-Command", command],
        capture_output=True,
        text=True
    )

def main():
    input_line = sys.stdin.readline().strip()

    if not input_line:
        log("No input received")
        return

    try:
        data = json.loads(input_line)
    except Exception as exc:
        log(f"Invalid JSON: {exc}")
        return

    command = data.get("command")

    try:
        source_ip = (
            data["parameters"]["alert"]["data"]["win"]["eventdata"]["sourceAddress"]
        )
    except Exception:
        log("sourceAddress not found in alert JSON")
        return

    if not source_ip:
        log("Empty sourceAddress")
        return

    rule_name = RULE_PREFIX + source_ip.replace(".", "-")

    if command == "add":

        check_message = {
            "version": 1,
            "origin": {
                "name": "block-recon-ip",
                "module": "active-response"
            },
            "command": "check_keys",
            "parameters": {
                "keys": [source_ip]
            }
        }

        print(json.dumps(check_message), flush=True)

        response_line = sys.stdin.readline().strip()

        try:
            response = json.loads(response_line)
        except Exception as exc:
            log(f"Invalid check_keys response: {exc}")
            return

        if response.get("command") != "continue":
            log(f"Action aborted for {source_ip}")
            return

        ps_command = (
            f'New-NetFirewallRule '
            f'-DisplayName "{rule_name}" '
            f'-Direction Inbound '
            f'-Action Block '
            f'-RemoteAddress "{source_ip}" '
            f'-Profile Any'
        )

        result = run_powershell(ps_command)

        if result.returncode == 0:
            log(f"BLOCKED {source_ip}")
        else:
            log(f"BLOCK FAILED {source_ip}: {result.stderr}")

    elif command == "delete":

        ps_command = (
            f'Get-NetFirewallRule '
            f'-DisplayName "{rule_name}" '
            f'-ErrorAction SilentlyContinue | '
            f'Remove-NetFirewallRule'
        )

        result = run_powershell(ps_command)

        if result.returncode == 0:
            log(f"UNBLOCKED {source_ip}")
        else:
            log(f"UNBLOCK FAILED {source_ip}: {result.stderr}")

    else:
        log(f"Unsupported command: {command}")


if __name__ == "__main__":
    main()