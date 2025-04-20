from typing import Generator, List


def read_log_file_in_chunks(
    file_path: str, chunk_size: int = 1024
) -> Generator[str, None, None]:
    """
    Read a log file in chunks to handle large files efficiently.

    :param file_path: Path to the log file.
    :param chunk_size: The size of each chunk to read (in bytes).
    :yield: Lines from the file, one by one.
    """
    with open(file_path, "r") as file:
        buffer = ""
        while chunk := file.read(chunk_size):
            buffer += chunk
            while "\n" in buffer:
                line, buffer = buffer.split("\n", 1)
                yield line
        if buffer:
            yield buffer


def process_large_logs(log_files: List[str]) -> None:
    """
    Process multiple large log files efficiently by reading them in chunks.

    :param log_files: List of log file paths.
    """
    for file_path in log_files:
        print(f"Processing file: {file_path}")
        for line in read_log_file_in_chunks(file_path):
            # Placeholder for further log processing logic
            if line.strip():
                print(
                    f"Processed line: {line[:50]}..."
                )  # Example: print first 50 chars of each line
