# Contributing to MedData

First off, thank you for taking the time to contribute! We truly appreciate it.

The following guidelines will help you get up and running so you can get your changes merged in quickly.

## 📑 Table of Contents
1. [Code of Conduct](#code-of-conduct)
2. [How Can I Contribute?](#how-can-i-contribute)
3. [Development Setup](#development-setup)
4. [Running Tests](#running-tests)
5. [Submitting a Pull Request](#submitting-a-pull-request)
6. [Style Guide](#style-guide)

## Code of Conduct
This project and everyone participating in it is governed by the [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code.

## How Can I Contribute?
### Reporting Bugs
* Ensure the bug was not already reported by searching on GitHub under **Issues**.
* If you're unable to find an open issue addressing the problem, [open a new one](https://github.com/alaamer12/meddata/issues/new/choose).
* Provide **steps to reproduce** and, if applicable, attach logs or screenshots.

### Suggesting Enhancements
* Use the **Feature Request** template when opening a new issue.
* Provide a clear and concise description of the feature and why it is needed.

### Pull Requests
* Fork the repository and create your branch from `main`.
* If you've added code that should be tested, add tests.
* Ensure your code style adheres to `black` and `isort` (see Style Guide).
* If the pull request adds or changes functionality, update the documentation.

## Development Setup
```bash
# Clone your fork
$ git clone https://github.com/<your-username>/meddata.git
$ cd meddata

# Create virtual environment
$ python -m venv .venv
$ source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install the project in editable mode with dev dependencies
$ pip install -e .[dev]
```

## Running Tests
```bash
pytest -q
```

## Submitting a Pull Request
1. Ensure your branch is **up to date** with `main`.
2. Push your changes to your fork.
3. Open a [pull request](https://github.com/alaamer12/meddata/compare) on GitHub.
4. Fill in the PR template and describe your changes.

## Style Guide
* **Formatter**: [black](https://github.com/psf/black)
* **Imports**: [isort](https://github.com/pycqa/isort)
* **Linting**: [flake8](https://github.com/pycqa/flake8)

Run the following to apply formatting:
```bash
black . && isort .
```

Thank you for contributing! 🙌
