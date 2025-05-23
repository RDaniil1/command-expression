# Command-expression
A simple command-based application designed to evaluate mathematical expressions and perform calculations based on user inputs.

## Contents
1. Algorithm
2. Prerequisites
3. Usage
4. Testing

### 1. Algorithm
The application implements a parser for evaluating mathematical expressions. Key features include:
* Support for basic arithmetic operations (+, -, *, /)
* Parenthesis handling for complex expressions
* Error handling for invalid expressions

### 2. Prerequisites
Before running the application (requires python 3.10+):
```bash
git clone https://github.com/RDaniil1/command-expression.git
pip install -r requirements.txt
```
This application also requires an internet connection for voice input.

### 3. Usage
The application provides a graphical user interface for calculating expressions. To launch the application, simply:
```bash
python calculate.py
```
This program can calculate using either text or voice input. Both methods use the same command structure for creating and calculating mathematical expressions.

Available commands:
* 'разделить' - '/'
* 'умножить' - '*'
* 'плюс' - '+'
* 'минус' - '-'
* 'степень' - '**'
* 'начало' - '('
* 'конец' - ')'

Numbers are written in Russian language.
When using numbers higher than 10, it is important to use underscores between them.
For example, the value "начало тридцать_три плюс шесть конец минус семь" would yield an image with 32 in the result.
For voice input, the result will be the same if similar input is used.

### 4. Testing
Pytests are included in the tests directory. Simply:
```bash
pytest
```
to use the available tests.

Test coverage includes:
* Parser functionality
* Expression evaluation
* Error handling