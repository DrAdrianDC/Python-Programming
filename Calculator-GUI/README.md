# Calculator using Python and Tkinter


### Overview

This project is a simple calculator built with Python using the Tkinter library to create a graphical user interface (GUI). The calculator allows basic arithmetic operations, including addition, subtraction, multiplication, and division, with a clear display to show the result. The GUI consists of digit buttons (0-9), basic operation buttons (+, -, *, /), a "clear" button to reset the display, and an "=" button to calculate the result.

### Features

   - **Simple GUI:** Built using Tkinter for an interactive and easy-to-use interface.
   - **Basic Operations:** Supports addition, subtraction, multiplication, and division.
   - **Clear Function:** A button to clear the current input and reset the calculator.
   - **Responsive Display:** Shows current input, operations, and results.

----

### Using PyInstaller to Create an Executable

PyInstaller is a Python library that can package your script into a standalone executable.
Step-by-Step Guide:

**1- Install PyInstaller:** You can install PyInstaller using pip:
    
```bash
pip install pyinstaller
```

**2- Navigate to the Directory of Your Script:** Open a terminal or command prompt and navigate to the folder where your calculator Python script is saved.

**3- Create Executable:** Run the following command in the terminal:

```bash
pyinstaller --onefile --windowed calculator-gui.py
```





### How to Use

   1 - **Enter Numbers:** Click on the digit buttons (0-9) to input numbers.
   
   2 - **Select an Operation:** Use the operation buttons (+, -, *, /) to perform calculations.
   
   3 - **Get the Result:** Click the = button to compute and display the result.
   
   4 - **Clear the Display:** Use the C button to reset the display for a new calculation.
   





### Future Improvements

- Add support for decimal points.
- Create more advanced operations like square root, percentage, etc.
