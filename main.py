import argparse
import os
import sys
from collections import defaultdict
from multiprocessing import Manager, Pool

from reports import get_available_reports
from typing import Generator, Dict, DefaultDict, List


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


def read_logs_line_by_line(file_path: str) -> Generator[str, None, None]:
    """
    Read a log file line by line.

    :param file_path: Path to the log file.
    :yield: Lines from the log file one by one.
    """
    try:
        with open(file_path, "r") as file:
            for line in file:
                yield line
    except FileNotFoundError:
        print(f"Error: File not found - {file_path}", file=sys.stderr)
    except IsADirectoryError:
        message = f"Error: Unable to read file {file_path} - Is a directory"
        print(message, file=sys.stderr)
    except Exception as e:
        print(f"Error: Unable to read file {file_path} - {e}", file=sys.stderr)


def process_file_in_parallel(file_path: str, report_class) -> Dict:
    """
    Process a single log file using the given report class.

    :param file_path: Path to the log file.
    :param report_class: Report class to process the log data.
    :return: Processed data as a dictionary.
    """
    print(f"Process {os.getpid()} is processing file: {file_path}")
    log_lines = read_logs_line_by_line(file_path)
    report = report_class()
    return report.process_logs(log_lines)


def merge_results(results: List[Dict]) -> Dict:
    """
    Merge results from multiple processed files.

    :param results: List of dictionaries containing processed data.
    :return: Merged dictionary with combined data.
    """
    final_result: DefaultDict[str, DefaultDict[str, int]] = defaultdict(
        lambda: defaultdict(int)
    )
    for result in results:
        for endpoint, levels in result.items():
            for level, count in levels.items():
                final_result[endpoint][level] += count

    return {key: dict(value) for key, value in final_result.items()}


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
    with Manager():
        with Pool(processes=4) as pool:
            results = pool.starmap(
                process_file_in_parallel,
                [(file, report_class) for file in args.log_files],
            )

    final_data = merge_results(results)
    report = report_class()
    report.generate_report(final_data)


if __name__ == "__main__":
    main()
