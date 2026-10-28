from pathlib import Path

def scan_directory(directory: Path) -> list[Path]:
    """
    Return sorted paths to files directly inside the given directory.

    Args:
        directory (Path): The directory to scan.

    Returns:
        List[Path]: A list of file paths.
    """
    paths = []
    for item in directory.iterdir():
        if item.is_file():
            paths.append(item)
    return sorted(paths)