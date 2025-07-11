#!/usr/bin/env python3
"""
MedData Printer Module - Enhanced terminal output for MedData Engineering Hub.

This module provides a robust printing utility that enhances terminal output
using the rich library. It supports various message formats and displays
helpful, informative error messages.
"""
from __future__ import annotations

import os
import platform
import sys
import textwrap
from datetime import datetime
from types import TracebackType
from typing import Any, Dict, List, Optional, Union, Type, TypeVar

from typing_extensions import Literal

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table
    from rich.syntax import Syntax
    from rich.markdown import Markdown
    from rich.progress import Progress, SpinnerColumn, TextColumn
    from rich.traceback import install as install_rich_traceback
    from rich.theme import Theme

    HAS_RICH = True
except ImportError:
    HAS_RICH = False

__all__ = ["printer", "Printer"]

MessageType = Literal["info", "success", "warning", "error", "guide", "header"]
ErrorType = Literal[
    "missing_file", "permission", "network", "missing_dependency", "dataset_config", "dataset_processing"]

# Type variable for the progress context
T = TypeVar('T', bound='Progress')


# Return a simple context manager when rich is not available
class DummyProgress:
    def __init__(self, description):
        self.description = description

    def __enter__(self) -> 'DummyProgress':
        print(f"{self.description}...")
        return self

    def __exit__(self, exc_type: Optional[Type[BaseException]],
                 exc_val: Optional[BaseException],
                 exc_tb: Optional[TracebackType]) -> None:
        print("Done!")

    @staticmethod
    def add_task(description: str, total: Optional[int] = None) -> int:
        return 0

    def update(self, task_id: int, advance: int = 1,
               description: Optional[str] = None) -> None:
        pass


class Printer:
    """
    Enhanced terminal output handler for MedData Engineering Hub.
    
    This class provides methods for printing messages with different formats,
    displaying guides and error messages in a user-friendly way.
    
    Attributes:
        debug_mode (bool): Whether debug mode is enabled for more detailed output
        use_rich (bool): Whether rich formatting is available and enabled
        console (Optional[Console]): Rich console instance if available
    """

    # ASCII art for MEDDATA logo
    MEDDATA_ASCII: str = """
    ███╗   ███╗███████╗██████╗ ██████╗  █████╗ ████████╗ █████╗ 
    ████╗ ████║██╔════╝██╔══██╗██╔══██╗██╔══██╗╚══██╔══╝██╔══██╗
    ██╔████╔██║█████╗  ██║  ██║██║  ██║███████║   ██║   ███████║
    ██║╚██╔╝██║██╔══╝  ██║  ██║██║  ██║██╔══██║   ██║   ██╔══██║
    ██║ ╚═╝ ██║███████╗██████╔╝██████╔╝██║  ██║   ██║   ██║  ██║
    ╚═╝     ╚═╝╚══════╝╚═════╝ ╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝
                                                                 
    Engineering Hub
    """

    # Color theme for console output
    MEDDATA_THEME: Dict[str, str] = {
        "info": "cyan",
        "warning": "yellow",
        "danger": "bold red",
        "success": "bold green",
        "primary": "#6366f1",  # Match brand color from CSS
        "secondary": "#14b8a6",  # Match brand color from CSS
        "header": "bold #6366f1",
        "guide": "bold yellow",
        "code": "blue",
        "path": "italic cyan",
        "date": "magenta",
    }

    def __init__(self, use_rich: bool = True, debug: bool = False) -> None:
        """
        Initialize the Printer.
        
        Args:
            use_rich: Whether to use rich formatting (if available)
            debug: Enable debug mode for more detailed output
        """
        self.debug_mode: bool = debug
        self.use_rich: bool = use_rich and HAS_RICH

        if self.use_rich:
            # Setup rich with our custom theme
            custom_theme = Theme(self.MEDDATA_THEME)
            self.console: Optional[Console] = Console(theme=custom_theme)

            # Install rich traceback handler for better error display
            if debug:
                install_rich_traceback(show_locals=True)
            else:
                install_rich_traceback(show_locals=False)
        else:
            # Fallback mode if rich is not available
            self.console: Optional[Console] = None

        # Handle character encoding issues
        self._setup_encoding()

    @staticmethod
    def _setup_encoding() -> None:
        """Configure terminal encoding to handle special characters properly."""
        if platform.system() == "Windows":
            # Fix common encoding issues on Windows
            try:
                # Try to use UTF-8 on Windows
                if sys.stdout.encoding != 'utf-8':
                    if hasattr(sys.stdout, 'reconfigure'):
                        sys.stdout.reconfigure(encoding='utf-8')
                    # elif hasattr(sys.stdout, 'encoding'):
            except Exception:
                # Fallback if reconfigure is not available
                os.environ['PYTHONIOENCODING'] = 'utf-8'

    @staticmethod
    def _format_plain(message: str, msg_type: MessageType = "info") -> str:
        """
        Format a message for plain text output (no rich formatting).
        
        Args:
            message: The message to format
            msg_type: Type of message for appropriate formatting
            
        Returns:
            Formatted message string
        """
        prefix = {
            "info": "[INFO] ",
            "success": "[SUCCESS] ",
            "warning": "[WARNING] ",
            "error": "[ERROR] ",
            "guide": "[GUIDE] ",
            "header": "=== ",
        }.get(msg_type, "")

        suffix = {
            "header": " ===",
        }.get(msg_type, "")

        return f"{prefix}{message}{suffix}"

    def print(self, message: str, msg_type: MessageType = "info") -> None:
        """
        Print a message with appropriate formatting.
        
        Args:
            message: The message to print
            msg_type: Message type (info, success, warning, error, guide, header)
        """
        if self.use_rich:
            self.console.print(message, style=msg_type)
        else:
            print(self._format_plain(message, msg_type))

    def header(self, message: str, width: int = 80) -> None:
        """
        Print a header message.
        
        Args:
            message: The header message
            width: Width of the header panel
        """
        if self.use_rich:
            self.console.print(Panel(message, width=width, style="header"))
        else:
            print("\n" + "=" * width)
            print(self._format_plain(message, "header"))
            print("=" * width)

    def success(self, message: str) -> None:
        """
        Print a success message.
        
        Args:
            message: The success message to display
        """
        self.print(message, "success")

    def warning(self, message: str) -> None:
        """
        Print a warning message.
        
        Args:
            message: The warning message to display
        """
        self.print(message, "warning")

    def error(self, message: str, exception: Optional[Exception] = None) -> None:
        """
        Print an error message with optional exception details.
        
        Args:
            message: The error message
            exception: Optional exception to display
        """
        if self.use_rich:
            self.console.print(Panel(
                f"{message}\n\n" +
                (f"[italic]{str(exception)}[/italic]" if exception else ""),
                title="[danger]ERROR",
                border_style="danger",
                expand=False
            ))

            # Show exception traceback in debug mode
            if exception and self.debug_mode:
                self.console.print_exception(show_locals=True)
        else:
            print(f"\n{self._format_plain(message, 'error')}")
            if exception:
                print(f"  → {str(exception)}")

    def guide(self, title: str, steps: List[str]) -> None:
        """
        Print a user guide with steps.
        
        Args:
            title: Guide title
            steps: List of steps to display
        """
        if self.use_rich:
            guide_content = "\n".join(f"{i + 1}. {step}" for i, step in enumerate(steps))
            self.console.print(Panel(
                guide_content,
                title=f"[guide]{title}",
                border_style="guide",
                expand=False
            ))
        else:
            print(f"\n{self._format_plain(title, 'guide')}")
            for i, step in enumerate(steps):
                print(f"  {i + 1}. {step}")

    def code(self, code: str, language: str = "python") -> None:
        """
        Print code with syntax highlighting.
        
        Args:
            code: The code to display
            language: Programming language for syntax highlighting
        """
        if self.use_rich:
            self.console.print(Syntax(code, language, theme="monokai"))
        else:
            print("\n--- Code ---")
            print(textwrap.indent(code, "  "))
            print("------------")

    def file_path(self, path: str, exists: bool = True) -> None:
        """
        Print a file path with existence indicator.
        
        Args:
            path: The file path to display
            exists: Whether the file exists
        """
        if self.use_rich:
            icon = "✓" if exists else "✗"
            self.console.print(f"{icon} [path]{path}[/path]")
        else:
            icon = "[EXISTS]" if exists else "[NOT FOUND]"
            print(f"{icon} {path}")

    def table(self, columns: List[str], rows: List[List[str]], title: Optional[str] = None) -> None:
        """
        Print a table of information.
        
        Args:
            columns: Column headers
            rows: Row data
            title: Optional table title
        """
        if self.use_rich:
            table = Table(title=title)
            for column in columns:
                table.add_column(column)

            for row in rows:
                table.add_row(*row)

            self.console.print(table)
        else:
            if title:
                print(f"\n{title}")

            # Simple ASCII table
            col_widths = [max(len(col), max((len(row[i]) for row in rows), default=0))
                          for i, col in enumerate(columns)]

            # Header
            header = " | ".join(col.ljust(width) for col, width in zip(columns, col_widths))
            print(header)
            print("-" * len(header))

            # Rows
            for row in rows:
                print(" | ".join(cell.ljust(width) for cell, width in zip(row, col_widths)))

    def progress_context(self, description: str = "Processing") -> Union[Progress, 'DummyProgress']:
        """
        Create a progress context for tracking operations.
        
        Args:
            description: Description of the operation
            
        Returns:
            A progress context manager (when rich is available)
            or a dummy context manager (when rich is not available)
        """
        if self.use_rich:
            return Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=self.console
            )
        else:

            return DummyProgress(description)

    def dataset_created(self, dataset_id: str, config_path: str) -> None:
        """
        Print a success message for dataset creation with next steps guide.
        
        Args:
            dataset_id: ID of the created dataset
            config_path: Path to the dataset configuration file
        """
        if self.use_rich:
            self.console.print(Panel(
                f"[success]Dataset [bold]{dataset_id}[/bold] created successfully![/success]\n\n"
                f"Configuration file: [path]{config_path}[/path]",
                title="Dataset Created",
                border_style="success",
                expand=False
            ))

            # Guide for next steps
            next_steps = [
                f"Edit [path]{config_path}[/path] to customize dataset properties",
                f"Run [code]python meddata.py assets {dataset_id}[/code] to generate assets",
                f"Create dataset directory: [code]mkdir -p dataset/{dataset_id}[/code]",
                f"Create dataset page: [path]dataset/{dataset_id}/index.md[/path]",
                f"Run [code]python meddata.py process {dataset_id}[/code] to process your dataset",
                f"Run [code]python meddata.py docs {dataset_id}[/code] to generate documentation"
            ]

            self.console.print(Panel(
                "\n".join(f"{i + 1}. {step}" for i, step in enumerate(next_steps)),
                title="Next Steps",
                border_style="guide",
                expand=False
            ))
        else:
            print(f"\n[SUCCESS] Dataset '{dataset_id}' created successfully!")
            print(f"Configuration file: {config_path}")
            print("\nNext steps:")
            print(f"1. Edit {config_path} to customize dataset properties")
            print(f"2. Run 'python meddata.py assets {dataset_id}' to generate assets")
            print(f"3. Create dataset directory: mkdir -p dataset/{dataset_id}")
            print(f"4. Create dataset page: dataset/{dataset_id}/index.md")
            print(f"5. Run 'python meddata.py process {dataset_id}' to process your dataset")
            print(f"6. Run 'python meddata.py docs {dataset_id}' to generate documentation")

    def dataset_processed(self, dataset_id: str, stats: Dict[str, Any]) -> None:
        """
        Print a success message for dataset processing with statistics.
        
        Args:
            dataset_id: ID of the processed dataset
            stats: Dictionary containing dataset statistics
        """
        if self.use_rich:
            # Format stats into a table
            stats_table = Table(show_header=True)
            stats_table.add_column("Metric")
            stats_table.add_column("Value")

            for key, value in stats.items():
                stats_table.add_row(key, str(value))

            self.console.print(Panel(
                f"[success]Dataset [bold]{dataset_id}[/bold] processed successfully![/success]\n",
                title="Dataset Processed",
                border_style="success",
                expand=False
            ))

            self.console.print(Panel(stats_table, title="Dataset Statistics"))
        else:
            print(f"\n[SUCCESS] Dataset '{dataset_id}' processed successfully!")
            print("\nDataset Statistics:")
            for key, value in stats.items():
                print(f"  {key}: {value}")

    def dataset_published(self, dataset_id: str, platforms: List[str], urls: List[str]) -> None:
        """
        Print a success message for dataset publishing with platform URLs.
        
        Args:
            dataset_id: ID of the published dataset
            platforms: List of platforms the dataset was published to
            urls: List of URLs where the dataset can be accessed
        """
        if self.use_rich:
            # Create a table of platforms and URLs
            urls_table = Table(show_header=True)
            urls_table.add_column("Platform")
            urls_table.add_column("URL")

            for platform, url in zip(platforms, urls):
                urls_table.add_row(platform, url)

            self.console.print(Panel(
                f"[success]Dataset [bold]{dataset_id}[/bold] published successfully![/success]\n",
                title="Dataset Published",
                border_style="success",
                expand=False
            ))

            self.console.print(Panel(urls_table, title="Access URLs"))
        else:
            print(f"\n[SUCCESS] Dataset '{dataset_id}' published successfully!")
            print("\nAccess URLs:")
            for platform, url in zip(platforms, urls):
                print(f"  {platform}: {url}")

    def logo(self) -> None:
        """Display the MEDDATA ASCII logo."""
        if self.use_rich:
            self.console.print(self.MEDDATA_ASCII, style="primary")
        else:
            print(self.MEDDATA_ASCII)

    def timestamp(self) -> None:
        """Print the current timestamp."""
        now = datetime.now()
        timestamp = now.strftime("%Y-%m-%d %H:%M:%S")

        if self.use_rich:
            self.console.print(f"[date]{timestamp}[/date]")
        else:
            print(timestamp)

    def smart_error(self, error_type: ErrorType, context: Optional[Dict[str, Any]] = None) -> None:
        """
        Display a smart error message based on error type and context.
        
        Args:
            error_type: Type of error (missing_file, permission, network, etc.)
            context: Dictionary with context information
        """
        context = context or {}

        error_templates: Dict[ErrorType, tuple[str, str, List[str]]] = {
            "missing_file": (
                "File not found",
                f"The file [path]{context.get('path', 'unknown')}[/path] does not exist.",
                [
                    f"Check if the path is correct",
                    f"Make sure you're in the right directory",
                    f"Try creating the file: [code]touch {context.get('path', 'file_path')}[/code]"
                ]
            ),
            "permission": (
                "Permission denied",
                f"You don't have permission to access [path]{context.get('path', 'unknown')}[/path]",
                [
                    f"Check file permissions: [code]ls -la {context.get('path', 'file_path')}[/code]",
                    f"Try running with elevated permissions"
                ]
            ),
            "network": (
                "Network error",
                f"Could not connect to {context.get('service', 'remote service')}",
                [
                    f"Check your internet connection",
                    f"Verify that {context.get('service', 'the service')} is available",
                    f"Check API credentials if applicable"
                ]
            ),
            "missing_dependency": (
                "Missing dependency",
                f"The required dependency [code]{context.get('dependency', 'unknown')}[/code] is not installed",
                [
                    f"Install the dependency: [code]pip install {context.get('dependency', 'package_name')}[/code]",
                    f"Make sure you're using the correct virtual environment"
                ]
            ),
            "dataset_config": (
                "Invalid dataset configuration",
                f"The dataset configuration for [bold]{context.get('dataset_id', 'unknown')}[/bold] is invalid",
                [
                    f"Check the YAML syntax in [path]{context.get('config_path', '_datasets/dataset_id.yml')}[/path]",
                    f"Ensure all required fields are present",
                    f"Validate the YAML file with a linter"
                ]
            ),
            "dataset_processing": (
                "Error processing dataset",
                f"Failed to process dataset [bold]{context.get('dataset_id', 'unknown')}[/bold]",
                [
                    f"Check source configuration in [path]{context.get('config_path', '_datasets/dataset_id.yml')}[/path]",
                    f"Ensure source APIs are accessible",
                    f"Check logs for detailed error information"
                ]
            )
        }

        if error_type not in error_templates:
            # Generic error
            title = "Error occurred"
            message = str(context.get('message', 'An unknown error occurred'))
            solutions = [
                "Check the application logs for more details",
                "Run in debug mode for more information"
            ]
        else:
            title, message, solutions = error_templates[error_type]

        if self.use_rich:
            self.console.print(Panel(
                f"{message}\n\n[guide]Possible solutions:[/guide]",
                title=f"[danger]{title}",
                border_style="danger",
                expand=False
            ))

            for i, solution in enumerate(solutions):
                self.console.print(f"  {i + 1}. {solution}")
        else:
            print(f"\n[ERROR] {title}")
            print(f"  {message}")
            print("\nPossible solutions:")
            for i, solution in enumerate(solutions):
                print(f"  {i + 1}. {solution}")


# Initialize a global printer instance for easy import
printer = Printer()

# If the script is run directly, show a demo
if __name__ == "__main__":
    print("MedData Printer Demo")
    print("-------------------")

    # Create a printer instance
    p = Printer()

    # Show logo
    p.logo()

    # Examples of different message types
    p.header("MedData Printer Demo")
    p.print("This is a regular info message")
    p.success("Operation completed successfully!")
    p.warning("This might cause issues")

    # Show an error
    p.error("Something went wrong", Exception("Invalid configuration"))

    # Smart error
    p.smart_error("missing_file", {"path": "config.yml"})

    # Guide
    p.guide("Getting Started", [
        "Install dependencies with pip install -r requirements.txt",
        "Configure your settings in config.yml",
        "Run the application with python app.py"
    ])

    # Code example
    p.code("def hello():\n    print('Hello, world!')")

    # Table example
    p.table(
        ["Dataset", "Size", "Status"],
        [
            ["medium", "500K+", "Published"],
            ["devto", "200K+", "Development"]
        ],
        title="Available Datasets"
    )

    # Example of dataset operations
    p.dataset_created("example", "_datasets/example.yml")

    p.dataset_processed("example", {
        "Total rows": 10000,
        "Fields": 15,
        "Size": "25MB"
    })

    p.dataset_published(
        "example",
        ["Hugging Face", "GitHub"],
        ["https://huggingface.co/datasets/example", "https://github.com/example/dataset"]
    )
