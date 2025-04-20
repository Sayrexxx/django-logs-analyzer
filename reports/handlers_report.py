import re
from collections import defaultdict
from typing import Generator, Dict, DefaultDict
from reports.base_report import BaseReport

LOG_LEVELS = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]


class HandlersReport(BaseReport):
    """
    Implementation of the 'handlers' report.
    This report counts requests grouped by API endpoints and log levels.
    """

    def process_logs(
        self, log_lines: Generator[str, None, None]
    ) -> Dict[str, Dict[str, int]]:
        """
        Process log lines to count requests grouped by API
        endpoints and log levels.

        :param log_lines: Generator yielding log lines.
        :return: Processed data - a dictionary where keys are API endpoints
        and values are dictionaries of log levels with their respective counts.
        """
        report_data: DefaultDict[str, DefaultDict[str, int]] = defaultdict(
            lambda: defaultdict(int)
        )

        log_pattern = re.compile(
            r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3} "
            r"(?P<level>DEBUG|INFO|WARNING|ERROR|CRITICAL) "
            r"django\.request:.*?"
            r"(?P<endpoint>/[^\s]+)"
        )

        for line in log_lines:
            match = log_pattern.search(line)
            if match:
                level = match.group("level")
                endpoint = match.group("endpoint")
                report_data[endpoint][level] += 1

        return {key: dict(value) for key, value in report_data.items()}

    def generate_report(self, data: Dict[str, Dict[str, int]]) -> None:
        """
        Generate and print the 'handlers' report.

        :param data: The processed log data.
        """
        total_requests = 0
        sorted_handlers = sorted(data.keys())

        print("HANDLER\t\t\tDEBUG\tINFO\tWARNING ERROR\tCRITICAL")
        print("-" * 64)

        for handler in sorted_handlers:
            counts = data[handler]
            handler_total = sum(counts.get(level, 0) for level in LOG_LEVELS)
            total_requests += handler_total
            formatted_counts = "\t".join(
                f"{counts.get(level, 0):<6}" for level in LOG_LEVELS
            )
            print(f"{handler:<24}{formatted_counts}")

        print("-" * 64)
        print(f"Total requests: {total_requests}")
