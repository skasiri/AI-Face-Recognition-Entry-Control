### System Requirements

- Python version: 3.10.0

Ensure that you have Python 3.10.0 installed on your system. You can verify your Python version by running the following command:

```bash
python --version
```

If you do not have Python 3.10.0 installed, you can download it from the [official Python website](https://www.python.org/downloads/).

### Virtual Environment (venv)

A virtual environment is a self-contained directory that contains a Python interpreter and libraries. It is recommended to use a virtual environment to isolate your project's dependencies from the system Python environment.

To create a virtual environment, run the following command in your terminal:

```bash
python -m venv venv
```

Once the virtual environment is created, you can activate it by running the following command:

```bash
source venv/bin/activate
```

### Install requirements from requirements.txt

You can install all the requirements specified in the requirements.txt file using the following command:

```bash
pip install -r requirements.txt
```

This will install all the required packages and their dependencies.

### Run the Project

To run the project, execute the following command in your terminal:

```bash
python main.py
```
