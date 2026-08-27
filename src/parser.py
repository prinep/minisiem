import re
from event import LogEvent


def parse_log(log):
    ssh_match = re.search(
        r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) sshd: (Failed|Accepted) password for (\w+) from (\d+\.\d+\.\d+\.\d+)",
        log
    )

    if ssh_match:
        return LogEvent(
            ssh_match.group(1),
            ssh_match.group(2),
            ssh_match.group(3),
            ssh_match.group(4)
        )

    web_match = re.search(
        r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) web: GET (\S+) from (\d+\.\d+\.\d+\.\d+)",
        log
    )

    if web_match:
        return LogEvent(
            web_match.group(1),
            f"GET {web_match.group(2)}",
            "web",
            web_match.group(3)
        )

    return None