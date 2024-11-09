from pathlib import Path
import shutil
import os

def remove_redundant_files():
    """Remove redundant and empty files"""
    files_to_remove = [
        "tests/integration/__init__.py",
        "tests/__init__.py",
        "config/local.env",
        "config/test.env",
        "src/utils/db_connection.py",
        "src/utils/db_helper.py",
        "tests/unit/test_helpers.py",
        "tests/integration/test_db.py",
        "src/utils/logging.py",
        "src/utils/log_helper.py"
    ]
    
    for file_path in files_to_remove:
        path = Path(file_path)
        if path.exists():
            path.unlink()
            print(f"Removed: {file_path}")
        else:
            print(f"Already removed or not found: {file_path}")

if __name__ == "__main__":
    remove_redundant_files() 