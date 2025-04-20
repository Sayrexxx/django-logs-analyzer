import os
import importlib
from typing import Dict, Type
from reports.base_report import BaseReport


def get_available_reports() -> Dict[str, Type[BaseReport]]:
    """
    Dynamically discover and return a dictionary of available reports.
    :return: A dictionary where keys are report names
    and values are report classes.
    """
    reports = {}
    current_dir = os.path.dirname(__file__)

    print(f"Scanning directory: {current_dir}")

    for file in os.listdir(current_dir):
        if file.endswith("_report.py") and file != "base_report.py":
            module_name = f"reports.{file[:-3]}"
            print(f"Importing module: {module_name}")
            module = importlib.import_module(module_name)
            for attr_name in dir(module):
                attr = getattr(module, attr_name)
                if (
                    isinstance(attr, type)
                    and issubclass(attr, BaseReport)
                    and attr is not BaseReport
                ):
                    report_key = file.replace("_report.py", "").lower()
                    reports[report_key] = attr
                    print(f"Registered report: {report_key} -> {attr_name}")
    return reports
