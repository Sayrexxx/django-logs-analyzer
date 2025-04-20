from abc import ABC, abstractmethod
from typing import Dict, List


class BaseReport(ABC):
    """
    Abstract base class for all reports.
    Each report must inherit this class and implement its methods.
    """

    @abstractmethod
    def process_logs(self, log_files: List[str]) -> Dict:
        """
        Process log files and extract necessary data for the report.
        :param log_files: List of log file paths.
        :return: Processed data for the report.
        """
        pass

    @abstractmethod
    def generate_report(self, data: Dict) -> None:
        """
        Generate and print the report based on the processed data.
        :param data: The processed log data.
        """
        pass
