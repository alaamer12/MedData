#!/usr/bin/env python3
"""
MedData Config Manager - Environment and configuration management.

This module provides utilities for loading and accessing configuration settings
from .env files, environment variables, and other sources. It centralizes
configuration management for the MedData platform.
"""
from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Optional, Union

__all__ = ["ConfigManager", "config_manager"]


@dataclass
class TokenConfig:
    """
    Configuration for API tokens and authentication.
    
    Attributes:
        huggingface: Hugging Face API token
        kaggle: Kaggle API token
        github: GitHub API token
    """
    huggingface: Optional[str] = None
    kaggle: Optional[str] = None
    github: Optional[str] = None


@dataclass
class PathConfig:
    """
    Configuration for important file paths.
    
    Attributes:
        project_root: Root directory of the project
        datasets_dir: Directory containing dataset configurations
        templates_dir: Directory containing templates
        data_dir: Directory containing data files
        raw_data_dir: Directory containing raw data files
        processed_data_dir: Directory containing processed data files
        docs_dir: Directory containing documentation files
    """
    project_root: Path
    datasets_dir: Path
    templates_dir: Path
    data_dir: Path
    raw_data_dir: Path
    processed_data_dir: Path
    docs_dir: Path


class ConfigManager:
    """
    Manages configuration settings for the MedData platform.
    
    This class handles loading configuration from .env files and environment
    variables, and provides access to tokens, paths, and other settings.
    
    Attributes:
        tokens: Configuration for API tokens
        paths: Configuration for file paths
        env_vars: Dictionary of all loaded environment variables
    """

    def __init__(self, env_file: Optional[Union[str, Path]] = None, debug: bool = False) -> None:
        """
        Initialize the ConfigManager.
        
        Args:
            env_file: Path to the .env file to load (defaults to project_root/.env)
            debug: Whether to enable debug mode
        """
        self.debug_mode = debug
        self.env_vars: Dict[str, str] = {}

        # Set up paths
        self.project_root = Path(__file__).parent.parent.parent.absolute()
        self.paths = PathConfig(
            project_root=self.project_root,
            datasets_dir=self.project_root / "_datasets",
            templates_dir=self.project_root / "templates",
            data_dir=self.project_root / "_data",
            raw_data_dir=self.project_root / "_data" / "raw",
            processed_data_dir=self.project_root / "_data" / "processed",
            docs_dir=self.project_root / "docs"
        )

        # Load environment variables
        self._load_env_vars(env_file)

        # Set up tokens
        self.tokens = TokenConfig(
            huggingface=self.get_env("HF_TOKEN") or self.get_env("HUGGINGFACE_TOKEN"),
            kaggle=self.get_env("KAGGLE_TOKEN") or self.get_env("KAGGLE_KEY"),
            github=self.get_env("GITHUB_TOKEN")
        )

        # Set up Kaggle configuration if token is available
        if self.tokens.kaggle:
            self._setup_kaggle_config()

    def _load_env_vars(self, env_file: Optional[Union[str, Path]] = None) -> None:
        """
        Load environment variables from .env file.
        
        Args:
            env_file: Path to the .env file to load
        """
        # Default to .env in project root if not specified
        if env_file is None:
            env_file = self.project_root / ".env"

        env_path = Path(env_file)

        # Load from .env file if it exists
        if env_path.exists():
            if self.debug_mode:
                print(f"Loading environment variables from {env_path}")

            with open(env_path, 'r') as f:
                for line in f:
                    line = line.strip()
                    # Skip comments and empty lines
                    if not line or line.startswith('#'):
                        continue

                    # Parse key-value pairs
                    if '=' in line:
                        key, value = line.split('=', 1)
                        key = key.strip()
                        value = value.strip()

                        # Remove quotes if present
                        if value.startswith('"') and value.endswith('"'):
                            value = value[1:-1]
                        elif value.startswith("'") and value.endswith("'"):
                            value = value[1:-1]

                        # Store in our env_vars dict and set as environment variable
                        self.env_vars[key] = value
                        os.environ[key] = value

        # Also load existing environment variables into our dict
        for key, value in os.environ.items():
            if key not in self.env_vars:
                self.env_vars[key] = value

    def get_env(self, key: str, default: Optional[str] = None) -> Optional[str]:
        """
        Get an environment variable.
        
        Args:
            key: Name of the environment variable
            default: Default value if not found
            
        Returns:
            Value of the environment variable or default
        """
        return self.env_vars.get(key, default)

    def _setup_kaggle_config(self) -> None:
        """Set up Kaggle configuration if token is available."""
        if not self.tokens.kaggle:
            return

        # Create Kaggle directory if it doesn't exist
        kaggle_dir = Path.home() / ".kaggle"
        kaggle_dir.mkdir(exist_ok=True)

        # Create kaggle.json if it doesn't exist
        kaggle_json = kaggle_dir / "kaggle.json"
        if not kaggle_json.exists():
            username = self.get_env("KAGGLE_USERNAME", "meddata")
            key = self.tokens.kaggle

            with open(kaggle_json, 'w') as f:
                f.write(f'{{"username":"{username}","key":"{key}"}}')

            # Set permissions to avoid warning
            kaggle_json.chmod(0o600)

    def get_token_for_platform(self, platform: str) -> Optional[str]:
        """
        Get the API token for a specific platform.
        
        Args:
            platform: Name of the platform ('huggingface', 'kaggle', 'github')
            
        Returns:
            API token for the platform or None if not available
        """
        if platform == 'huggingface':
            return self.tokens.huggingface
        elif platform == 'kaggle':
            return self.tokens.kaggle
        elif platform == 'github':
            return self.tokens.github
        return None

    def ensure_directories_exist(self) -> None:
        """Create all required directories if they don't exist."""
        self.paths.datasets_dir.mkdir(exist_ok=True, parents=True)
        self.paths.templates_dir.mkdir(exist_ok=True, parents=True)
        self.paths.data_dir.mkdir(exist_ok=True, parents=True)
        self.paths.raw_data_dir.mkdir(exist_ok=True, parents=True)
        self.paths.processed_data_dir.mkdir(exist_ok=True, parents=True)
        self.paths.docs_dir.mkdir(exist_ok=True, parents=True)


# Create global instance for easy imports
config_manager = ConfigManager()
