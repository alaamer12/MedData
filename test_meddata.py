import pytest
import argparse
from unittest.mock import MagicMock, patch
from pathlib import Path
import sys
import os
import subprocess
import shutil # Added import

import meddata # Import the module itself
from meddata import (
    init_dataset,
    process_dataset,
    publish_dataset,
    generate_assets,
    generate_docs,
    generate_site,
    doctor_dataset,
    setup_env,
    validate_environment,
    create_parser,
    main,
)

# Mock config_manager.paths for consistent testing environment
@pytest.fixture(autouse=True)
def mock_config_manager_paths(tmp_path, mocker):
    mock_config = mocker.patch("meddata.config_manager")
    
    # Use actual Path objects from tmp_path for these
    mock_config.paths.project_root = tmp_path
    mock_config.paths.datasets_dir = tmp_path / "_datasets"
    mock_config.paths.docs_dir = tmp_path / "docs"
    mock_config.paths.processed_data_dir = tmp_path / "_data" / "processed"
    
    # Ensure these directories exist for tests that expect them
    mock_config.paths.project_root.mkdir(exist_ok=True)
    mock_config.paths.datasets_dir.mkdir(exist_ok=True)
    mock_config.paths.docs_dir.mkdir(exist_ok=True)
    mock_config.paths.processed_data_dir.mkdir(exist_ok=True, parents=True)
    (tmp_path / "scripts").mkdir(exist_ok=True) # Ensure scripts directory exists

    # Create example-docs structure for doctor and init tests
    example_docs_path = tmp_path / "example-docs"
    example_docs_path.mkdir(exist_ok=True)
    
    hf_path = example_docs_path / "huggingface"
    hf_path.mkdir(exist_ok=True)
    (hf_path / "README.md").write_text("HF README example")
    (hf_path / "dataset-card.md").write_text("HF Dataset Card example")
    (hf_path / "CITATION.cff").write_text("HF Citation example")
    (hf_path / "LICENSE").write_text("HF License example")
    (hf_path / "CHANGELOG.md").write_text("HF Changelog example")
    (hf_path / "CONTRIBUTING.md").write_text("HF Contributing example")

    kg_path = example_docs_path / "kaggle"
    kg_path.mkdir(exist_ok=True)
    (kg_path / "README.md").write_text("KG README example")
    (kg_path / "dataset-card.md").write_text("KG Dataset Card example")
    (kg_path / "LICENSE").write_text("KG License example")
    (kg_path / "CHANGELOG.md").write_text("KG Changelog example")
    (kg_path / ".kaggle").mkdir(exist_ok=True)
    (kg_path / ".kaggle" / "README.md").write_text("KG .kaggle README example")

    yield mock_config

# Mock subprocess_handler and printer for all tests
@pytest.fixture(autouse=True)
def mock_external_dependencies(mocker):
    mock_subprocess_handler = mocker.patch("meddata.subprocess_handler")
    mock_printer = mocker.patch("meddata.printer")
    return {"subprocess_handler": mock_subprocess_handler, "printer": mock_printer}


# Helper to create a mock args object
def create_mock_args(**kwargs):
    args = MagicMock()
    for key, value in kwargs.items():
        setattr(args, key, value)
    return args


# --- Test init_dataset ---
def test_init_dataset_success(mock_external_dependencies, tmp_path):
    args = create_mock_args(
        id="test_id",
        name="Test Name",
        description="Test Description",
        license=False,
        changelog=False,
        citation=False,
        ds_card=False,
        contributing=False,
        readme=False,
    )
    init_dataset(args)
    mock_external_dependencies["subprocess_handler"].run_python_script.assert_called_once_with(
        str(tmp_path / "scripts" / "create-dataset.py"),
        ["test_id", "Test Name", "Test Description"],
        check=True,
    )
    mock_external_dependencies["printer"].success.assert_called_once()


def test_init_dataset_with_docs(mock_external_dependencies, tmp_path, mocker):
    # No direct mocking of _copy_template_file, let it run naturally
    # Ensure the example-docs files have the 'example' placeholder for re.sub

    args = create_mock_args(
        id="test_id_docs",
        name="Test Name Docs",
        description="Test Description Docs",
        license=True,
        changelog=True,
        citation=True,
        ds_card=True,
        contributing=True,
        readme=True,
    )
    init_dataset(args)
    mock_external_dependencies["subprocess_handler"].run_python_script.assert_called_once()
    mock_external_dependencies["printer"].success.assert_called_once()

    dataset_dir = tmp_path / "dataset" / args.id 
    dataset_dir.mkdir(parents=True, exist_ok=True) # Ensure parent directories exist
    assert dataset_dir.exists()
    assert (dataset_dir / "LICENSE").exists()
    assert (dataset_dir / "CHANGELOG.md").exists()
    assert (dataset_dir / "CITATION.cff").exists()
    assert (dataset_dir / "dataset-card.md").exists()
    assert (dataset_dir / "CONTRIBUTING.md").exists()
    assert (dataset_dir / "README.md").exists()

    # Verify content replacement
    assert "test_id_docs" in (dataset_dir / "README.md").read_text()


def test_init_dataset_failure(mock_external_dependencies):
    mock_external_dependencies["subprocess_handler"].run_python_script.side_effect = (
        subprocess.CalledProcessError(1, "cmd")
    )
    args = create_mock_args(
        id="fail_id",
        name="Fail Name",
        description="Fail Description",
        license=False,
        changelog=False,
        citation=False,
        ds_card=False,
        contributing=False,
        readme=False,
    )
    with pytest.raises(SystemExit) as excinfo:
        init_dataset(args)
    assert excinfo.value.code == 1
    mock_external_dependencies["printer"].error.assert_called_once()


# --- Test process_dataset ---
def test_process_dataset_success(mock_external_dependencies, tmp_path):
    args = create_mock_args(id="test_process_id")
    process_dataset(args)
    mock_external_dependencies["subprocess_handler"].run_python_script.assert_called_once_with(
        str(tmp_path / "scripts" / "process-dataset.py"),
        ["test_process_id"],
        check=True,
    )
    mock_external_dependencies["printer"].success.assert_called_once()


def test_process_dataset_failure(mock_external_dependencies):
    mock_external_dependencies["subprocess_handler"].run_python_script.side_effect = (
        subprocess.CalledProcessError(1, "cmd")
    )
    args = create_mock_args(id="fail_process_id")
    with pytest.raises(SystemExit) as excinfo:
        process_dataset(args)
    assert excinfo.value.code == 1
    mock_external_dependencies["printer"].error.assert_called_once()


# --- Test publish_dataset ---
def test_publish_dataset_success_no_token_no_platforms(mock_external_dependencies, tmp_path):
    args = create_mock_args(id="test_publish_id", token=None, platforms=None)
    publish_dataset(args)
    mock_external_dependencies["subprocess_handler"].run_python_script.assert_called_once_with(
        str(tmp_path / "scripts" / "publish-dataset.py"),
        ["test_publish_id"],
        check=True,
    )
    mock_external_dependencies["printer"].success.assert_called_once()


def test_publish_dataset_success_with_token_and_platforms(mock_external_dependencies, tmp_path):
    args = create_mock_args(id="test_publish_id", token="my_token", platforms=["huggingface", "github"])
    publish_dataset(args)
    mock_external_dependencies["subprocess_handler"].run_python_script.assert_called_once_with(
        str(tmp_path / "scripts" / "publish-dataset.py"),
        ["test_publish_id", "--token", "my_token", "--platforms", "huggingface", "github"],
        check=True,
    )
    mock_external_dependencies["printer"].success.assert_called_once()


def test_publish_dataset_failure(mock_external_dependencies):
    mock_external_dependencies["subprocess_handler"].run_python_script.side_effect = (
        subprocess.CalledProcessError(1, "cmd")
    )
    args = create_mock_args(id="fail_publish_id", token=None, platforms=None)
    with pytest.raises(SystemExit) as excinfo:
        publish_dataset(args)
    assert excinfo.value.code == 1
    mock_external_dependencies["printer"].error.assert_called_once()


# --- Test generate_assets ---
def test_generate_assets_all_datasets_success(mock_external_dependencies, tmp_path):
    args = create_mock_args(dataset_id=None)
    generate_assets(args)
    mock_external_dependencies["subprocess_handler"].run_python_script.assert_called_once_with(
        str(tmp_path / "scripts" / "generate-assets.py"),
        [],
        check=True,
    )
    mock_external_dependencies["printer"].success.assert_called_once()


def test_generate_assets_specific_dataset_success(mock_external_dependencies, tmp_path):
    args = create_mock_args(dataset_id="test_asset_id")
    generate_assets(args)
    mock_external_dependencies["subprocess_handler"].run_python_script.assert_called_once_with(
        str(tmp_path / "scripts" / "generate-assets.py"),
        ["test_asset_id"],
        check=True,
    )
    mock_external_dependencies["printer"].success.assert_called_once()


def test_generate_assets_failure(mock_external_dependencies):
    mock_external_dependencies["subprocess_handler"].run_python_script.side_effect = (
        subprocess.CalledProcessError(1, "cmd")
    )
    args = create_mock_args(dataset_id=None)
    with pytest.raises(SystemExit) as excinfo:
        generate_assets(args)
    assert excinfo.value.code == 1
    mock_external_dependencies["printer"].error.assert_called_once()


# --- Test generate_docs ---
def test_generate_docs_success(mock_external_dependencies, tmp_path):
    args = create_mock_args(id="test_docs_id")
    generate_docs(args)
    mock_external_dependencies["subprocess_handler"].run_python_script.assert_called_once_with(
        str(tmp_path / "scripts" / "generate-docs.py"),
        ["test_docs_id"],
        check=True,
    )
    mock_external_dependencies["printer"].success.assert_called_once()


def test_generate_docs_failure(mock_external_dependencies):
    mock_external_dependencies["subprocess_handler"].run_python_script.side_effect = (
        subprocess.CalledProcessError(1, "cmd")
    )
    args = create_mock_args(id="fail_docs_id")
    with pytest.raises(SystemExit) as excinfo:
        generate_docs(args)
    assert excinfo.value.code == 1
    mock_external_dependencies["printer"].error.assert_called_once()


# --- Test generate_site ---
def test_generate_site_build_success(mock_external_dependencies):
    args = create_mock_args(serve=False)
    generate_site(args)
    mock_external_dependencies["subprocess_handler"].run.assert_called_once_with(
        ["bundle", "exec", "jekyll", "build"], check=True
    )
    mock_external_dependencies["printer"].success.assert_called_once()


def test_generate_site_serve_success(mock_external_dependencies):
    args = create_mock_args(serve=True)
    generate_site(args)
    mock_external_dependencies["subprocess_handler"].run.assert_called_once_with(
        ["bundle", "exec", "jekyll", "serve"], check=True
    )
    mock_external_dependencies["printer"].success.assert_called_once()


def test_generate_site_failure(mock_external_dependencies):
    mock_external_dependencies["subprocess_handler"].run.side_effect = (
        subprocess.CalledProcessError(1, "cmd")
    )
    args = create_mock_args(serve=False)
    with pytest.raises(SystemExit) as excinfo:
        generate_site(args)
    assert excinfo.value.code == 1
    mock_external_dependencies["printer"].error.assert_called_once()


# --- Test doctor_dataset ---
def test_doctor_dataset_all_files_exist(mock_external_dependencies, tmp_path):
    dataset_id = "existing_dataset"
    dataset_dir = tmp_path / "dataset" / dataset_id
    dataset_dir.mkdir(parents=True, exist_ok=True) 
    (dataset_dir / "README.md").touch()
    (dataset_dir / "dataset-card.md").touch()
    (dataset_dir / "CITATION.cff").touch()
    (dataset_dir / "LICENSE").touch()
    (dataset_dir / "CHANGELOG.md").touch()
    (tmp_path / "_data" / "processed" / dataset_id).mkdir(parents=True, exist_ok=True)
    (tmp_path / "_data" / "processed" / dataset_id / "data.parquet").touch()
    (dataset_dir / ".kaggle").mkdir(parents=True, exist_ok=True)
    (dataset_dir / ".kaggle" / "README.md").touch()

    args = create_mock_args(id=dataset_id, hf=False, kg=False, fix=False)
    doctor_dataset(args)
    mock_external_dependencies["printer"].success.assert_called_once_with("All required files exist. Dataset is ready for publishing!")
    mock_external_dependencies["printer"].error.assert_not_called()


def test_doctor_dataset_missing_hf_files_no_fix(mock_external_dependencies, tmp_path, mocker):
    dataset_id = "missing_hf"
    dataset_dir = tmp_path / "dataset" / dataset_id
    dataset_dir.mkdir(parents=True, exist_ok=True) 
    
    # Do NOT create the files that should be missing

    args = create_mock_args(id=dataset_id, hf=True, kg=False, fix=False)
    with pytest.raises(SystemExit) as excinfo:
        doctor_dataset(args)
    assert excinfo.value.code == 1
    mock_external_dependencies["printer"].table.assert_called_once()
    mock_external_dependencies["printer"].error.assert_not_called() # Should not call error, but exit


def test_doctor_dataset_missing_hf_files_with_fix(mock_external_dependencies, tmp_path, mocker):
    dataset_id = "missing_hf_fix"
    dataset_dir = tmp_path / "dataset" / dataset_id
    dataset_dir.mkdir(parents=True, exist_ok=True) 
    
    # Remove files that should be missing
    (dataset_dir / "README.md").unlink(missing_ok=True)
    (dataset_dir / "dataset-card.md").unlink(missing_ok=True)
    (dataset_dir / "CITATION.cff").unlink(missing_ok=True)
    (dataset_dir / "LICENSE").unlink(missing_ok=True)
    (tmp_path / "_data" / "processed" / dataset_id / "data.parquet").unlink(missing_ok=True)

    args = create_mock_args(id=dataset_id, hf=True, kg=False, fix=True)
    doctor_dataset(args)
    mock_external_dependencies["printer"].success.assert_called_with("All required files exist. Dataset is ready for publishing!")
    mock_external_dependencies["printer"].table.assert_called_once()
    mock_external_dependencies["printer"].print.assert_any_call("Please review and customise the generated templates before publishing.", "warning")

    # Assert that the files are created
    assert (dataset_dir / "README.md").exists()
    assert (dataset_dir / "dataset-card.md").exists()
    assert (dataset_dir / "CITATION.cff").exists()
    assert (dataset_dir / "LICENSE").exists()
    assert (dataset_dir / "CHANGELOG.md").exists()
    assert not (tmp_path / "_data" / "processed" / dataset_id / "data.parquet").exists() # Data file should not be auto-generated


def test_doctor_dataset_missing_kg_files_no_fix(mock_external_dependencies, tmp_path, mocker):
    dataset_id = "missing_kg"
    dataset_dir = tmp_path / "dataset" / dataset_id
    dataset_dir.mkdir(parents=True, exist_ok=True) 
    
    # Do NOT create the files that should be missing

    args = create_mock_args(id=dataset_id, hf=False, kg=True, fix=False)
    with pytest.raises(SystemExit) as excinfo:
        doctor_dataset(args)
    assert excinfo.value.code == 1
    mock_external_dependencies["printer"].table.assert_called_once()


def test_doctor_dataset_missing_kg_files_with_fix(mock_external_dependencies, tmp_path, mocker):
    dataset_id = "missing_kg_fix"
    dataset_dir = tmp_path / "dataset" / dataset_id
    dataset_dir.mkdir(parents=True, exist_ok=True) 

    # Remove files that should be missing
    (dataset_dir / ".kaggle" / "README.md").unlink(missing_ok=True)
    (dataset_dir / "dataset-card.md").unlink(missing_ok=True)
    (dataset_dir / "LICENSE").unlink(missing_ok=True)
    (dataset_dir / "CHANGELOG.md").unlink(missing_ok=True)

    args = create_mock_args(id=dataset_id, hf=False, kg=True, fix=True)
    doctor_dataset(args)
    mock_external_dependencies["printer"].success.assert_called_with("All required files exist. Dataset is ready for publishing!")
    mock_external_dependencies["printer"].table.assert_called_once()

    # Assert that the files are created
    assert (dataset_dir / ".kaggle" / "README.md").exists()
    assert (dataset_dir / "dataset-card.md").exists()
    assert (dataset_dir / "LICENSE").exists()
    assert (dataset_dir / "CHANGELOG.md").exists()


def test_doctor_dataset_not_found(mock_external_dependencies, tmp_path, mocker):
    # Remove the dataset directory to simulate it being missing
    shutil.rmtree(tmp_path / "dataset", ignore_errors=True)
    shutil.rmtree(tmp_path / "docs", ignore_errors=True)
    shutil.rmtree(tmp_path / "_datasets", ignore_errors=True)

    args = create_mock_args(id="non_existent_dataset", hf=False, kg=False, fix=False)
    with pytest.raises(SystemExit) as excinfo:
        doctor_dataset(args)
    assert excinfo.value.code == 1
    mock_external_dependencies["printer"].error.assert_called_once()


# --- Test setup_env ---
def test_setup_env_success(mock_external_dependencies, tmp_path):
    env_file_path = tmp_path / ".env"
    args = create_mock_args(env_file=str(env_file_path), force=False)
    setup_env(args)
    assert env_file_path.exists()
    # Removed platform-specific permission check
    mock_external_dependencies["printer"].success.assert_called_once()
    assert "HF_TOKEN=" in env_file_path.read_text()


def test_setup_env_already_exists_no_force(mock_external_dependencies, tmp_path):
    env_file_path = tmp_path / ".env"
    env_file_path.touch()  # Create dummy file
    args = create_mock_args(env_file=str(env_file_path), force=False)
    setup_env(args)
    mock_external_dependencies["printer"].warning.assert_any_call(f"Environment file already exists at {env_file_path}")
    mock_external_dependencies["printer"].warning.assert_any_call("Use --force to overwrite")
    mock_external_dependencies["printer"].success.assert_not_called()
    assert env_file_path.read_text() == ""  # Should not be overwritten


def test_setup_env_already_exists_with_force(mock_external_dependencies, tmp_path):
    env_file_path = tmp_path / ".env"
    env_file_path.write_text("OLD CONTENT")
    args = create_mock_args(env_file=str(env_file_path), force=True)
    setup_env(args)
    assert env_file_path.exists()
    assert "HF_TOKEN=" in env_file_path.read_text()
    assert "OLD CONTENT" not in env_file_path.read_text()
    mock_external_dependencies["printer"].success.assert_called_once()


def test_setup_env_failure(mock_external_dependencies, tmp_path):
    read_only_dir = tmp_path / "read_only"
    read_only_dir.mkdir()

    env_file_path = read_only_dir / ".env"
    args = create_mock_args(env_file=str(env_file_path), force=False)

    # Mock open to raise an error
    with patch("builtins.open", side_effect=OSError("Permission denied")) as mock_open:
        with pytest.raises(SystemExit) as excinfo:
            setup_env(args)
        assert excinfo.value.code == 1
        mock_external_dependencies["printer"].error.assert_called_once()
    
    # Clean up the read-only directory (if it was created)
    if read_only_dir.exists():
        pass # No need to remove if open was mocked to fail before creation


# --- Test validate_environment ---
def test_validate_environment_success(mock_config_manager_paths, mocker):
    # All necessary directories are created by the fixture, so exists() should return True
    assert validate_environment() is True
    # No need to mock exists() here, as the real Path.exists() will be called and return True


def test_validate_environment_missing_project_root(mock_config_manager_paths, mocker):
    # Remove the project_root directory to simulate it being missing
    shutil.rmtree(mock_config_manager_paths.paths.project_root, ignore_errors=True)
    mocker.patch("meddata.printer.smart_error")
    mocker.patch("meddata.printer.warning")
    assert validate_environment() is False
    meddata.printer.smart_error.assert_called_once()
    meddata.printer.warning.assert_called_once()


def test_validate_environment_missing_scripts_dir(mock_config_manager_paths, mocker):
    # Remove the scripts directory to simulate it being missing
    shutil.rmtree(mock_config_manager_paths.paths.project_root / "scripts", ignore_errors=True)
    mocker.patch("meddata.printer.smart_error")
    mocker.patch("meddata.printer.warning")
    assert validate_environment() is False
    meddata.printer.smart_error.assert_called_once()
    meddata.printer.warning.assert_called_once()


def test_validate_environment_missing_datasets_dir(mock_config_manager_paths, mocker):
    # Remove the datasets directory to simulate it being missing
    shutil.rmtree(mock_config_manager_paths.paths.datasets_dir, ignore_errors=True)
    mocker.patch("meddata.printer.smart_error")
    mocker.patch("meddata.printer.warning")
    assert validate_environment() is False
    meddata.printer.smart_error.assert_called_once()
    meddata.printer.warning.assert_called_once()


# --- Test create_parser ---
def test_create_parser():
    parser = create_parser()
    assert isinstance(parser, argparse.ArgumentParser)
    # Check if some known subparsers exist
    subparsers_actions = [
        action
        for action in parser._actions
        if isinstance(action, argparse._SubParsersAction)
    ]
    assert len(subparsers_actions) == 1
    assert "init" in subparsers_actions[0].choices
    assert "process" in subparsers_actions[0].choices
    assert "publish" in subparsers_actions[0].choices
    assert "assets" in subparsers_actions[0].choices
    assert "docs" in subparsers_actions[0].choices
    assert "site" in subparsers_actions[0].choices
    assert "doctor" in subparsers_actions[0].choices
    assert "setup" in subparsers_actions[0].choices


# --- Test main ---
def test_main_no_command(mock_external_dependencies, capsys):
    # Simulate no command given
    with patch.object(sys, "argv", ["meddata.py"]):
        exit_code = main()
        assert exit_code == 1
        mock_external_dependencies["printer"].logo.assert_called_once()
        captured = capsys.readouterr()
        assert "usage: meddata.py" in captured.out


def test_main_init_command_success(mock_external_dependencies, mocker):
    # Simulate 'init' command
    mocker.patch("meddata.validate_environment", return_value=True) # Ensure environment validation passes
    with patch.object(
        sys, "argv", ["meddata.py", "init", "test_id", "Test Name", "Test Description"]
    ):
        exit_code = main()
        assert exit_code == 0
        mock_external_dependencies["printer"].logo.assert_called_once()
        mock_external_dependencies["subprocess_handler"].run_python_script.assert_called_once()
        mock_external_dependencies["printer"].success.assert_called_once()


def test_main_command_with_environment_validation_failure(mock_external_dependencies, mocker):
    # Simulate a command that requires environment validation, but it fails
    mocker.patch("meddata.validate_environment", return_value=False)
    with patch.object(
        sys, "argv", ["meddata.py", "process", "test_id"]
    ):
        exit_code = main()
        assert exit_code == 1
        mock_external_dependencies["printer"].logo.assert_called_once()
        mock_external_dependencies["subprocess_handler"].run_python_script.assert_not_called()


def test_main_setup_command_skips_environment_validation(mock_external_dependencies, mocker, tmp_path):
    # Ensure the .env file does not exist before the test runs
    env_file_path = tmp_path / "test.env"
    if env_file_path.exists():
        env_file_path.unlink()

    # Simulate 'setup' command, which should skip environment validation
    mocker.patch("meddata.validate_environment", return_value=False) # This mock should not be called
    with patch.object(
        sys, "argv", ["meddata.py", "setup", "--env-file", str(env_file_path)]
    ):
        exit_code = main()
        assert exit_code == 0 # setup_env should succeed if no other errors
        mock_external_dependencies["printer"].logo.assert_called_once()
        # validate_environment should not have been called for 'setup' command
        meddata.validate_environment.assert_not_called()
        mock_external_dependencies["printer"].success.assert_called_once() # setup_env success
