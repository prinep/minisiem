import re
from event import LogEvent


def parse_log(log):
    match = re.search(
        r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) sshd: (Failed|Accepted) password for (\w+) from (\d+\.\d+\.\d+\.\d+)",
        log
    )

    if match:
        return LogEvent(
            match.group(1),
            match.group(2),
            match.group(3),
            match.group(4)
        )

    return None