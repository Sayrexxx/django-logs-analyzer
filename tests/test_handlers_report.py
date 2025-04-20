from typing import Generator
import pytest
from reports.handlers_report import HandlersReport


@pytest.fixture
def sample_log_lines() -> Generator[str, None, None]:
    return (
        line
        for line in [
            "2023-04-20 12:34:56,789 INFO django.request: /api/v1/users",
            "2023-04-20 12:35:00,123 ERROR django.request: /api/v1/orders",
            "2023-04-20 12:36:01,456 INFO django.request: /api/v1/users",
            "2023-04-20 12:37:10,789 WARNING django.request: /api/v1/orders",
        ]
    )


def test_process_logs(sample_log_lines):
    report = HandlersReport()
    result = report.process_logs(sample_log_lines)

    expected_result = {
        "/api/v1/users": {"INFO": 2},
        "/api/v1/orders": {"ERROR": 1, "WARNING": 1},
    }

    assert result == expected_result


def test_generate_report(capsys):
    report = HandlersReport()
    data = {
        "/api/v1/users": {"INFO": 2},
        "/api/v1/orders": {"ERROR": 1, "WARNING": 1},
    }

    report.generate_report(data)

    captured = capsys.readouterr()
    print(captured.out)
    assert "HANDLER\t\t\tDEBUG\tINFO\tWARNING ERROR\tCRITICAL" in captured.out
    assert "Total requests: 4" in captured.out
