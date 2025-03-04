from kaggle.api.kaggle_api_extended import KaggleApi
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
from rich.table import Table
from rich.style import Style
from typing import Dict
import os
import sys


# Initialize Rich console
console = Console()

class DatasetUploader:
    def __init__(self, dataset_id: str):
        """
        Initialize the Kaggle dataset uploader.
        
        Args:
            dataset_id (str): The Kaggle dataset identifier (username/dataset-slug)
        """
        self.dataset_id = dataset_id
        self.api = KaggleApi()
        self.success_style = Style(color="green", bold=True)
        self.error_style = Style(color="red", bold=True)
        self.warning_style = Style(color="yellow", bold=True)
        self.base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    def authenticate(self) -> bool:
        """Authenticate with Kaggle API."""
        try:
            with console.status("[bold blue]Authenticating with Kaggle..."):
                # Set Kaggle config directory to local .kaggle folder
                os.environ['KAGGLE_CONFIG_DIR'] = os.path.join(self.base_path, '.kaggle')
                self.api.authenticate()
                user = self.api.get_current_user_info()
                console.print(f"✓ Authenticated as [bold green]{user.username}[/]")
                return True
        except Exception as e:
            console.print(f"[bold red]Authentication failed: {str(e)}[/]")
            return False

    def upload_file(self, local_path: str, dataset_path: str) -> bool:
        """Upload a single file to Kaggle dataset."""
        try:
            # Create the directory if it doesn't exist
            os.makedirs(os.path.dirname(dataset_path), exist_ok=True)
            
            # Copy file to the dataset directory
            with open(local_path, 'rb') as src, open(dataset_path, 'wb') as dst:
                dst.write(src.read())
            return True
        except Exception as e:
            console.print(f"[red]Error uploading {local_path}: {str(e)}[/]")
            return False

    def get_file_status(self) -> Table:
        """Create a table showing the status of all files."""
        table = Table(title="Files Status", show_header=True, header_style="bold magenta")
        table.add_column("File", style="cyan")
        table.add_column("Status", justify="center")
        table.add_column("Size", justify="right", style="green")
        return table

    def format_size(self, size_bytes: int) -> str:
        """Format file size in human-readable format."""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024:
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024
        return f"{size_bytes:.1f} GB"

    def upload_files(self, files_map: Dict[str, str]) -> None:
        """Upload multiple files with progress tracking."""
        table = self.get_file_status()
        total_files = len(files_map)
        uploaded = 0

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
            console=console
        ) as progress:
            task = progress.add_task("[cyan]Uploading files...", total=total_files)

            for local_file, dataset_file in files_map.items():
                full_path = os.path.join(self.base_path, local_file)
                dataset_path = os.path.join(self.base_path, "data", dataset_file)
                
                if os.path.exists(full_path):
                    size = self.format_size(os.path.getsize(full_path))
                    success = self.upload_file(full_path, dataset_path)
                    status = "[green]✓[/]" if success else "[red]✗[/]"
                    table.add_row(local_file, status, size)
                    if success:
                        uploaded += 1
                else:
                    table.add_row(local_file, "[yellow]Not Found[/]", "-")
                progress.update(task, advance=1)

        console.print(table)
        console.print(f"\nUploaded [green]{uploaded}[/] out of [blue]{total_files}[/] files")

        if uploaded > 0:
            try:
                # Create new version of the dataset
                self.api.dataset_create_version(
                    self.dataset_id,
                    f"Updated dataset metadata - {uploaded} files",
                    dir_mode="zip"
                )
                console.print("[green]Successfully created new dataset version![/]")
            except Exception as e:
                console.print(f"[red]Error creating dataset version: {str(e)}[/]")

def display_welcome_message():
    console.print(Panel.fit(
        "[bold blue]Dataset Metadata Uploader[/]\n"
        "[cyan]Updating metadata for Kaggle dataset repository[/]",
        border_style="green"
    ))

def get_files_to_upload():
    return {
        # Core metadata files
        "README.md": "README.md",
        "config/dataset-metadata.json": "dataset-metadata.json",
        "docs/CITATION.cff": "CITATION.cff",
        "docs/LICENSE": "LICENSE",
        "docs/CONTRIBUTING.md": "CONTRIBUTING.md",
        "docs/CHANGELOG.md": "CHANGELOG.md",
        "config/requirements.txt": "requirements.txt",
        ".kaggle/README.md": ".kaggle/README.md",
    }

def show_excluded_files():
    console.print("\n[yellow]Note: The following files are not uploaded:[/]")
    excluded = [
        ".git/ (version control)",
        ".venv/ (virtual environment)",
        "*.ipynb (Jupyter notebooks)",
        "scripts/ (Python source files)",
        "*.pyc (Python cache files)",
        "__pycache__/ (Python cache directory)"
    ]
    for item in excluded:
        console.print(f"• [dim]{item}[/]")

def main():
    DATASET_ID = "meddata/medium-articles-dataset"  # Update this with your dataset ID

    uploader = DatasetUploader(DATASET_ID)

    display_welcome_message()

    if not uploader.authenticate():
        sys.exit(1)

    files_to_upload = get_files_to_upload()
    uploader.upload_files(files_to_upload)

    show_excluded_files()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n[yellow]Upload cancelled by user[/]")
        sys.exit(1)
    except Exception as e:
        console.print(f"\n[bold red]Error: {str(e)}[/]")
        sys.exit(1)
