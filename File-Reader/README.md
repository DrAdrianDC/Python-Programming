# File Reader

### Overview
This Python program demonstrates basic error handling using `try` and `except` blocks to manage common issues such as missing files, permission errors, and unexpected exceptions.

### Features

- **File Reading:** Reads the content of a specified text file and displays it in the terminal.
- **Error Handling:**
  - Handles the case where the file does not exist.
  - Manages permissions issues when trying to access a file.
  - Catches any other unexpected errors to ensure the program does not crash.

### How to use
 **Run the Program**
```bash
./File-Reader.py
```
or

```bash
python File-Reader.py
```
You will be prompted to enter the name of the file you wish to read. If the file exists and you have the necessary permissions, its content will be displayed in the terminal. If there are any issues (e.g., the file does not exist or you do not have permission), an appropriate error message will be displayed.

### Requirements

    Python 3.8.3
