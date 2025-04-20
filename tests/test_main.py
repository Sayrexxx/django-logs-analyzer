import pytest
import sys
from unittest.mock import patch, mock_open
from main import (
    validate_file_paths,
    validate_report_type,
    parse_arguments,
    read_logs_line_by_line,
    process_file_in_parallel,
    merge_results,
)


def test_validate_file_paths_valid():
    with patch("os.path.exists", return_value=True):
        try:
            validate_file_paths(["logs/app1.log", "logs/app2.log"])
        except SystemExit:
            message = "validate_file_paths() raised SystemExit unexpectedly!"
            pytest.fail(message)


def test_validate_file_paths_invalid():
    with patch("os.path.exists", side_effect=[True, False]):
        with pytest.raises(SystemExit):
            validate_file_paths(["logs/app1.log", "logs/missing.log"])


def test_validate_report_type_valid():
    try:
        validate_report_type("handlers")
    except SystemExit:
        pytest.fail("validate_report_type() raised SystemExit unexpectedly!")


def test_validate_report_type_invalid():
    with pytest.raises(SystemExit):
        validate_report_type("unsupported_report")


def test_parse_arguments_valid():
    sys.argv = ["main.py", "--report", "handlers"]
    sys.argv.insert(1, "logs/app1.log")
    sys.argv.insert(2, "logs/app2.log")
    args = parse_arguments()

    assert args.log_files == ["logs/app1.log", "logs/app2.log"]
    assert args.report == "handlers"


def test_parse_arguments_missing_report():
    sys.argv = ["main.py", "logs/app1.log"]
    with pytest.raises(SystemExit):
        parse_arguments()


def test_read_logs_line_by_line_valid():
    file_content = "line1\nline2\nline3\n"
    with patch("builtins.open", mock_open(read_data=file_content)):
        lines = list(read_logs_line_by_line("logs/app1.log"))
        assert lines == ["line1\n", "line2\n", "line3\n"]


def test_read_logs_line_by_line_file_not_found():
    with patch("builtins.open", side_effect=FileNotFoundError):
        with pytest.raises(FileNotFoundError):
            list(read_logs_line_by_line("logs/missing.log"))


def test_read_logs_line_by_line_is_a_directory():
    with patch("builtins.open", side_effect=IsADirectoryError):
        with pytest.raises(IsADirectoryError):
            list(read_logs_line_by_line("logs/"))


def test_read_logs_line_by_line_general_exception():
    with patch("builtins.open", side_effect=Exception("General error")):
        with pytest.raises(Exception, match="General error"):
            list(read_logs_line_by_line("logs/error.log"))


def test_process_file_in_parallel():
    mock_log_lines = ["INFO django.request: /api/v1/users"]
    mock_report_class = type(
        "MockReport",
        (),
        {"process_logs": lambda self, logs: {"/api/v1/users": {"INFO": 1}}},
    )
    with patch("main.read_logs_line_by_line", return_value=mock_log_lines):
        result = process_file_in_parallel("logs/app1.log", mock_report_class)
        assert result == {"/api/v1/users": {"INFO": 1}}


def test_merge_results():
    results = [
        {"/api/v1/users": {"INFO": 2}, "/api/v1/orders": {"ERROR": 1}},
        {"/api/v1/users": {"INFO": 1}, "/api/v1/orders": {"WARNING": 1}},
    ]

    merged = merge_results(results)

    expected = {
        "/api/v1/users": {"INFO": 3},
        "/api/v1/orders": {"ERROR": 1, "WARNING": 1},
    }

    assert merged == expected
