import argparse
import os
import sys
from reports import get_available_reports
from typing import Generator


def validate_file_paths(file_paths):
    """
    Validate that all provided file paths exist.
    :param file_paths: List of file paths to validate.
    """
    for file_path in file_paths:
        if not os.path.exists(file_path):
            print(f"Error: File '{file_path}' does not exist.")
            sys.exit(1)


def validate_report_type(report_type):
    """
    Validate that the provided report type is supported.
    :param report_type: The report type to validate.
    """
    supported_reports = ["handlers"]
    if report_type not in supported_reports:
        print(
            f"Error: Unsupported report type '{report_type}'.\n"
            f" Supported types: {', '.join(supported_reports)}"
        )
        sys.exit(1)


def parse_arguments():
    """
    Parse and validate command-line arguments.
    :return: Parsed arguments.
    """
    parser = argparse.ArgumentParser(
        description="CLI tool for analyzing Django \n"
        "log files and generating reports."
    )
    help_message = "Paths to one or more log files."
    parser.add_argument("log_files", nargs="+", help=help_message)
    parser.add_argument(
        "--report",
        required=True,
        help="The type of report to generate (e.g., 'handlers').",
    )
    args = parser.parse_args()

    validate_file_paths(args.log_files)
    validate_report_type(args.report)

    return args


def read_logs_line_by_line(file_paths: list) -> Generator[str, None, None]:
    """
    Read log files line by line.

    :param file_paths: List of file paths.
    :yield: Lines from the log files one by one.
    """
    for file_path in file_paths:
        try:
            with open(file_path, "r") as file:
                for line in file:
                    yield line
        except FileNotFoundError:
            print(f"Error: File not found - {file_path}", file=sys.stderr)
        except Exception as e:
            ex_message = f"Error: Unable to read file {file_path} - {e}"
            print(ex_message, file=sys.stderr)


def main():
    """
    Entry point for the CLI application.
    """
    args = parse_arguments()
    available_reports = get_available_reports()
    report_type = args.report.lower()

    if report_type not in available_reports:
        print(
            f"Error: Unsupported report type '{args.report}'. "
            f"Supported types: {', '.join(available_reports.keys())}"
        )
        sys.exit(1)

    print(f"Processing log files: {', '.join(args.log_files)}")
    print(f"Generating '{args.report}' report...")
    report_class = available_reports[report_type]
    report = report_class()
    log_lines = read_logs_line_by_line(args.log_files)
    data = report.process_logs(log_lines)
    report.generate_report(data)


if __name__ == "__main__":
    main()
