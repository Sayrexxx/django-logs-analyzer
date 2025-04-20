from reports import get_available_reports


def test_get_available_reports():
    reports = get_available_reports()
    assert "handlers" in reports
    assert callable(reports["handlers"])
