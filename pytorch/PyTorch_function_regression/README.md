# PyTorch Function Regression

This project trains a simple neural network to **approximate a nonlinear mathematical function** using **PyTorch**.

---

## Overview

The model learns to fit the following function:

$$
y = \sin(x) + 0.3x + \text{noise}
$$

It demonstrates how PyTorch can be used for regression tasks, showing concepts such as:
- Dataset creation and data splitting  
- Neural network design using `nn.Module`  
- Training loop implementation  
- Loss tracking and visualization  

---


## File Structure

``` bash
PyTorch_function_regression/
├─ results/
├─ pytorch-function-regression.py
├─ requirements.txt
└─ README.md
```
---

## Requirements

Install the required dependencies:
```bash
pip install -r requirements.txt

```
---

## Usage

Run the Project
To train the model, simply run:

```bash
python pytorch-function-regression.py
```

