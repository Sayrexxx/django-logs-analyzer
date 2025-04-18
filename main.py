import argparse
import os
import sys
from reports.handlers_report import process_logs, generate_report


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


def main():
    """
    Entry point for the CLI application.
    """
    args = parse_arguments()
    print(f"Processing log files: {', '.join(args.log_files)}")
    print(f"Generating '{args.report}' report...")
    if args.report == "handlers":
        data = process_logs(args.log_files)
        generate_report(data)
    else:
        print(f"Error: Unsupported report type '{args.report}'.")


if __name__ == "__main__":
    main()
