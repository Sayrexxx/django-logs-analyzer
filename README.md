# Django Log Analysis CLI Tool

![Pre-commit](https://github.com/Sayrexxx/django-logs-analyzer/actions/workflows/pre-commit.yml/badge.svg)
![CI](https://github.com/Sayrexxx/django-logs-analyzer/actions/workflows/tests.yml/badge.svg)

## Overview
This project provides a command-line interface (CLI) tool to analyze Django log files and generate detailed reports. The tool is designed to handle large log files efficiently, supports parallel processing of multiple files, and provides modular architecture to easily add new report types.

---

## Features
- **Log Analysis**: Extracts and processes data from Django logs.
- **Report Generation**:
  - `handlers`: Counts requests grouped by API endpoints and log levels.
- **Large File Support**: Processes logs line by line to minimize memory usage.
- **Parallel Processing**: Handles multiple log files concurrently.
- **Modular Architecture**: Easily extendable to support new types of reports.
- **Error Handling**: Validates input paths and report types with clear error messages.

---

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Sayrexxx/django-logs-analyzer.git
   cd django-log-analysis-cli
   ```

2. **Set up a virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Linux/MacOS
   venv\Scripts\activate     # Windows
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

---

## Usage

### Command Syntax
```bash
python main.py [log_files] --report [report_type]
```

### Examples:
1. Generate a `handlers` report for a single file:
   ```bash
   python main.py logs/app1.log --report handlers
   ```

2. Generate a `handlers` report for multiple files:
   ```bash
   python main.py logs/app1.log logs/app2.log --report handlers
   ```

### Supported Report Types:
- **`handlers`**: Displays counts of requests grouped by API endpoints and log levels.

---

## Example Output
Command:
```bash
python main.py logs/app1.log logs/app2.log --report handlers
```

Output:
```
HANDLER               	DEBUG  	INFO   	WARNING	ERROR  	CRITICAL
------------------------------------------------------------
/admin/dashboard/     	20     	72     	19     	14     	18
/api/v1/auth/login/   	23     	78     	14     	15     	18
/api/v1/orders/       	26     	77     	12     	19     	22
------------------------------------------------------------
Total requests: 1000
```

---

## Adding a New Report

1. **Create a new report module**:
   - Add a file in the `reports/` directory named `<report_type>_report.py`.

2. **Inherit from `BaseReport`**:
   - Implement the `process_logs` and `generate_report` methods.

3. **Example**:
   ```python
   from reports.base_report import BaseReport

   class NewReport(BaseReport):
       def process_logs(self, log_files: List[str]) -> Dict:
           # Process log files and extract necessary data
           pass

       def generate_report(self, data: Dict) -> None:
           # Print the report based on the processed data
           pass
   ```

4. **Dynamic registration**:
   - The new report will be automatically detected and available through the CLI.

---

## Testing

1. **Install `pytest`**:
   ```bash
   pip install pytest
   ```

2. **Run tests**:
   ```bash
   pytest
   ```

Example output:
```
============================= test session starts ==============================
collected 15 items

tests/test_handlers_report.py ..                                                                                                                            [ 13%]
tests/test_main.py ............                                                                                                                             [ 93%]
tests/test_reports_init.py .                                                                                                                                [100%]

============================== 8 passed in 0.45s ===============================
```

---

## Example Log File Format
Example of a single log entry:
```
[2025-04-16 12:34:56] INFO django.request /api/v1/orders/ - User action
```

---

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
