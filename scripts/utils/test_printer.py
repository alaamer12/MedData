#!/usr/bin/env python3
"""
Tests for the Printer class.
Simple tests to ensure the Printer functionality works as expected.
"""

import unittest
from contextlib import redirect_stdout
from io import StringIO
from scripts.utils.printer import Printer, HAS_RICH


class TestPrinter(unittest.TestCase):
    """Test cases for the Printer class."""

    def setUp(self):
        """Set up for each test case."""
        # Create a printer with rich disabled for consistent output
        self.printer = Printer(use_rich=False)
        # StringIO object to capture stdout
        self.stdout = StringIO()

    def test_basic_output(self):
        """Test basic output methods."""
        with redirect_stdout(self.stdout):
            self.printer.print("Test message")
            self.printer.success("Success message")
            self.printer.warning("Warning message")
            self.printer.error("Error message")

        output = self.stdout.getvalue()
        self.assertIn("Test message", output)
        self.assertIn("[SUCCESS] Success message", output)
        self.assertIn("[WARNING] Warning message", output)
        self.assertIn("[ERROR] Error message", output)

    def test_header(self):
        """Test header output."""
        with redirect_stdout(self.stdout):
            self.printer.header("Test Header")

        output = self.stdout.getvalue()
        self.assertIn("=== Test Header ===", output)

    def test_guide(self):
        """Test guide output."""
        steps = ["Step 1", "Step 2", "Step 3"]

        with redirect_stdout(self.stdout):
            self.printer.guide("Test Guide", steps)

        output = self.stdout.getvalue()
        self.assertIn("[GUIDE] Test Guide", output)
        for i, step in enumerate(steps):
            self.assertIn(f"{i + 1}. {step}", output)

    def test_smart_error(self):
        """Test smart error output."""
        with redirect_stdout(self.stdout):
            self.printer.smart_error("missing_file", {
                "path": "test.yml",
                "message": "File not found"
            })

        output = self.stdout.getvalue()
        self.assertIn("[ERROR] File not found", output)
        self.assertIn("File not found", output)

    def test_dataset_created(self):
        """Test dataset_created output."""
        with redirect_stdout(self.stdout):
            self.printer.dataset_created("test", "_datasets/test.yml")

        output = self.stdout.getvalue()
        self.assertIn("[SUCCESS] Dataset 'test' created successfully", output)
        self.assertIn("Next steps:", output)

    def test_dataset_processed(self):
        """Test dataset_processed output."""
        stats = {"rows": 100, "columns": 5}

        with redirect_stdout(self.stdout):
            self.printer.dataset_processed("test", stats)

        output = self.stdout.getvalue()
        self.assertIn("[SUCCESS] Dataset 'test' processed successfully", output)
        self.assertIn("rows: 100", output)
        self.assertIn("columns: 5", output)

    def test_fallback_when_rich_unavailable(self):
        """Test that the printer works even when rich is unavailable."""
        # Create a printer that thinks rich is not available
        original_has_rich = HAS_RICH
        setattr(Printer, 'HAS_RICH', False)

        try:
            fallback_printer = Printer(use_rich=False)
            with redirect_stdout(self.stdout):
                fallback_printer.header("Fallback Header")
                fallback_printer.success("Fallback Success")

            output = self.stdout.getvalue()
            self.assertEqual(output, """\n================================================================================\n=== Fallback Header ===\n================================================================================\n[SUCCESS] Fallback Success\n""")
        finally:
            # Restore the original value
            setattr(Printer, 'HAS_RICH', original_has_rich)


if __name__ == "__main__":
    unittest.main()
