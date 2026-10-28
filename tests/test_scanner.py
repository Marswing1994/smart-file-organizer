from unittest.mock import patch
from smart_file_organizer.scanner import scan_directory
import pytest

def test_scan_directory_returns_only_top_level_files(tmp_path):
    # Create a temporary directory with some files and subdirectories
    file1 = tmp_path / "file1.txt"
    file1.touch()
    
    file2 = tmp_path / "file2.txt"
    file2.touch()
    
    subdir = tmp_path / "subdir"
    subdir.mkdir()
    
    file3 = subdir / "file3.txt"
    file3.touch()

    # Call the scan_directory function
    result = scan_directory(tmp_path)

    # Assert that only the files directly inside the directory are returned
    assert len(result) == 2
    assert set(result) == {file1, file2}

def test_scan_directory_missing_directory(tmp_path):
    # Create a temporary directory and remove it to simulate a missing directory
    missing_dir = tmp_path / "does_not_exist"
    
    with pytest.raises(FileNotFoundError):
        scan_directory(missing_dir)  # This should raise an exception since the directory does not exist

def test_scan_path_rejects_file_path(tmp_path):
    # Create a temporary file to simulate a path that is not a directory
    file_path = tmp_path / "file.txt"
    file_path.touch()
    
    with pytest.raises(NotADirectoryError):
        scan_directory(file_path)  # This should raise an exception since the path is not a directory

def test_scan_directory_permission_denied(tmp_path):
    with patch("pathlib.Path.iterdir", side_effect=PermissionError("Access denied.")):
        with pytest.raises(PermissionError):
            scan_directory(tmp_path)  # This should raise an exception due to permission issues

def test_scan_directory_empty_directory(tmp_path):
    # Create an empty temporary directory
    empty_dir = tmp_path / "empty_dir"
    empty_dir.mkdir()

    # Call the scan_directory function
    result = scan_directory(empty_dir)

    # Assert that the result is an empty list
    assert result == []

def test_scan_directory_returns_sorted_files(tmp_path):
    # Create a temporary directory with some files
    file1 = tmp_path / "z.txt"
    file1.touch()
    
    file2 = tmp_path / "a.txt"
    file2.touch()

    file3 = tmp_path / "m.txt"
    file3.touch()

    result = scan_directory(tmp_path)
    filenames = [file.name for file in result]

    # Assert that the result is sorted
    assert filenames == ["a.txt", "m.txt", "z.txt"]