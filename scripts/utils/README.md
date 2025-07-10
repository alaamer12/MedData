# MedData Utilities

This directory contains utility modules for the MedData Engineering Hub project.

## Printer Module

The `printer.py` module provides an enhanced terminal output utility that makes the MedData CLI more user-friendly. It uses the [rich](https://github.com/Textualize/rich) library to provide colorful, formatted output with visual elements like panels, tables, and progress bars.

### Features

- Colorful formatted output with different styles for different message types
- Smart error messages with contextual troubleshooting suggestions
- Progress indicators for long-running operations
- Tables for structured data display
- Code blocks with syntax highlighting
- ASCII art logo display
- Cross-platform support with Unicode handling

### Usage

```python
from utils.printer import printer

# Basic usage
printer.header("Processing Dataset")
printer.success("Operation completed successfully!")
printer.warning("This might cause performance issues")
printer.error("Failed to connect to API", Exception("Connection timeout"))

# Display a user guide with steps
printer.guide("Getting Started", [
    "Install dependencies with pip install -r requirements.txt",
    "Configure your dataset in _datasets/example.yml",
    "Process your dataset with python meddata.py process example"
])

# Display dataset statistics in a table
stats = {
    "Total rows": 10000,
    "Fields": 15,
    "Size": "25MB"
}
printer.dataset_processed("example", stats)

# Show smart error messages
printer.smart_error("missing_file", {
    "path": "config.yml",
    "message": "Configuration file is missing"
})

# Display progress for long operations
with printer.progress_context() as progress:
    task = progress.add_task("Processing...", total=100)
    for i in range(100):
        # Do some work
        progress.update(task, advance=1)
```

### Demo

To see all the features in action, run the included demo script:

```bash
python utils/demo.py
```

### Fallback Mode

If the `rich` library is not available, the Printer class falls back to plain text output with simple formatting, ensuring the CLI remains usable even without the dependency.

## Installation

The Printer requires the `rich` library:

```bash
pip install rich
```

Or simply install all project dependencies:

```bash
pip install -r requirements.txt
``` 