# File Organizer

**Description:**

The File Organizer script is a Python tool that organizes files in a source directory by moving them into folders based on their types.

**Usage:**

```bash
python file_organizer.py SOURCE_DIR DESTINATION_DIR [--dry-run]
```

- **SOURCE_DIR**: The source directory containing files to be organized.
- **DESTINATION_DIR**: The destination directory where organized files will be moved.
- **--dry-run**: Optional flag to simulate the organization without actually moving files.

**Example:**

```bash
python file_organizer.py /path/to/source /path/to/destination --dry-run
```

This command will simulate the organization of files from the source directory to the destination directory without actually moving the files.

**Note:**

- If the source or destination directory is not provided, the script will display an error message.
- During a dry run, the script will print the intended file movements and ask for confirmation before proceeding with the actual move.

**Dependencies:**

- Click: This script uses the Click library for command-line interface handling. Install it using:

```bash
pip install click
```
