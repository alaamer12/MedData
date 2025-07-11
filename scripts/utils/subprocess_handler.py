#!/usr/bin/env python3
"""
MedData Subprocess Handler - Safe subprocess execution with platform compatibility.

This module provides a unified interface for running subprocess commands with
proper encoding handling, error management, and platform-specific adaptations.
"""
from __future__ import annotations

import os
import platform
import shlex
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Optional, Union, Tuple, Callable

__all__ = ["SubprocessHandler", "subprocess_handler"]


class SubprocessHandler:
    """
    Handles subprocess execution with platform-aware encoding and error management.
    
    This class provides methods to run shell commands safely across different
    platforms, handling encoding issues and providing detailed error information.
    
    Attributes:
        debug_mode (bool): Whether to print additional debug information
    """

    def __init__(self, debug: bool = False) -> None:
        """
        Initialize the SubprocessHandler.
        
        Args:
            debug: Whether to enable debug mode
        """
        self.debug_mode = debug
        self._setup_environment()

    def _setup_environment(self) -> None:
        """Configure the environment for proper encoding and command execution."""
        if platform.system() == "Windows":
            # Fix common encoding issues on Windows
            os.environ['PYTHONIOENCODING'] = 'utf-8'
            # Prefer PowerShell over cmd.exe if available
            self.shell_executable = "powershell.exe" if os.path.exists(
                r"C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe") else None
        else:
            # Use standard shell on Unix-like systems
            self.shell_executable = None

    @staticmethod
    def _get_encoding() -> str:
        """Get the appropriate encoding for the current platform."""
        if platform.system() == "Windows":
            return 'utf-8'  # Standardize on UTF-8 for Windows
        else:
            return sys.getdefaultencoding()

    def run(self,
            cmd: Union[str, List[str]],
            check: bool = True,
            capture_output: bool = False,
            cwd: Optional[Union[str, Path]] = None,
            env: Optional[Dict[str, str]] = None,
            shell: bool = False,
            callback: Optional[Callable[[str], None]] = None) -> subprocess.CompletedProcess:
        """
        Run a command in a subprocess with proper encoding and error handling.
        
        Args:
            cmd: Command to run (string or list of arguments)
            check: Whether to raise an exception on non-zero exit code
            capture_output: Whether to capture command output
            cwd: Working directory for the command
            env: Environment variables for the command
            shell: Whether to use shell execution mode
            callback: Optional callback function for real-time output processing
        
        Returns:
            CompletedProcess instance containing command result
            
        Raises:
            subprocess.CalledProcessError: If the command returns a non-zero exit code and check=True
        """
        encoding = self._get_encoding()

        # Prepare command
        if isinstance(cmd, str) and not shell:
            cmd_list = shlex.split(cmd)
        else:
            cmd_list = cmd

        if self.debug_mode:
            cmd_str = cmd if isinstance(cmd, str) else " ".join(cmd)
            print(f"Running command: {cmd_str}")
            if cwd:
                print(f"Working directory: {cwd}")

        # Set shell parameters
        shell_args = {}
        if platform.system() == "Windows" and shell and self.shell_executable:
            shell_args = {"executable": self.shell_executable}

        # Create merged environment
        merged_env = None
        if env:
            merged_env = os.environ.copy()
            merged_env.update(env)

        # Callback handling requires different approach than capture_output
        if callback and not capture_output:
            process = subprocess.Popen(
                cmd_list,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                shell=shell,
                cwd=cwd,
                env=merged_env,
                text=True,
                encoding=encoding,
                **shell_args
            )

            stdout_lines = []
            stderr_lines = []

            # Process output in real-time
            while True:
                stdout_line = process.stdout.readline()
                stderr_line = process.stderr.readline()

                if stdout_line:
                    stdout_lines.append(stdout_line)
                    if callback:
                        callback(stdout_line)

                if stderr_line:
                    stderr_lines.append(stderr_line)
                    if callback:
                        callback(stderr_line)

                # Check if process has finished
                if process.poll() is not None:
                    # Get remaining output
                    for line in process.stdout:
                        stdout_lines.append(line)
                        if callback:
                            callback(line)

                    for line in process.stderr:
                        stderr_lines.append(line)
                        if callback:
                            callback(line)

                    break

            # Create CompletedProcess for consistent return
            result = subprocess.CompletedProcess(
                args=cmd_list,
                returncode=process.returncode,
                stdout="".join(stdout_lines),
                stderr="".join(stderr_lines)
            )

            if check and process.returncode != 0:
                raise subprocess.CalledProcessError(
                    process.returncode,
                    cmd_list,
                    output=result.stdout,
                    stderr=result.stderr
                )

            return result
        else:
            # Use run for simpler cases
            return subprocess.run(
                cmd_list,
                check=check,
                capture_output=capture_output,
                cwd=cwd,
                env=merged_env,
                shell=shell,
                text=True,
                encoding=encoding,
                **shell_args
            )

    def run_python_script(self,
                          script_path: Union[str, Path],
                          args: List[str] = None,
                          **kwargs) -> subprocess.CompletedProcess:
        """
        Run a Python script with the correct Python interpreter.
        
        Args:
            script_path: Path to the Python script
            args: Arguments to pass to the script
            **kwargs: Additional keyword arguments for run()
            
        Returns:
            CompletedProcess instance containing command result
        """
        args = args or []

        # Use sys.executable to ensure we use the same Python interpreter
        return self.run(
            [sys.executable, str(script_path)] + args,
            **kwargs
        )

    def run_module(self,
                   module: str,
                   args: List[str] = None,
                   **kwargs) -> subprocess.CompletedProcess:
        """
        Run a Python module using the -m flag.
        
        Args:
            module: Name of the module to run
            args: Arguments to pass to the module
            **kwargs: Additional keyword arguments for run()
            
        Returns:
            CompletedProcess instance containing command result
        """
        args = args or []

        return self.run(
            [sys.executable, "-m", module] + args,
            **kwargs
        )

    def run_and_get_output(self,
                           cmd: Union[str, List[str]],
                           shell: bool = False) -> Tuple[str, str, int]:
        """
        Run a command and return its stdout, stderr and return code.
        
        Args:
            cmd: Command to run (string or list of arguments)
            shell: Whether to use shell execution mode
            
        Returns:
            Tuple containing (stdout, stderr, return_code)
        """
        try:
            result = self.run(cmd, check=False, capture_output=True, shell=shell)
            return result.stdout, result.stderr, result.returncode
        except Exception as e:
            return "", str(e), 1


# Create global instance for easy imports
subprocess_handler = SubprocessHandler()
