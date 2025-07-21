#!/usr/bin/env -S uv run -s
import os
import subprocess
import tempfile
import zipfile
from pathlib import Path
from typing import List, Tuple

from rcabench_platform.v2.cli.main import app, logger
from rcabench_platform.v2.logging import timeit
from rcabench_platform.v2.config import get_config
from rcabench.openapi.api import ContainerApi
from rcabench.openapi.api_client import ApiClient, Configuration


def get_configuration(host: str) -> Configuration:
    configuration = Configuration(host=host)
    configuration.datetime_format = "%Y-%m-%dT%H:%M:%SZ"
    return configuration


@app.command()
@timeit()
def single(
    env: str = "prod",
    container_type: str = "algorithm",
    name: str = "traceback-test",
    image: str = "10.10.10.240/library/rca-algo-traceback-test-local-file",
    tag: str = "latest",
    command: str = "bash /entrypoint.sh",
    env_vars: str | None = None,
    filename: str = "traceback.zip",
    context_dir: str = ".",
    dockerfile_path: str = "Dockerfile",
    force_rebuild: bool = False,
):
    """
    Build and upload local file to get container

    Args:
        env: Environment mode (prod or dev or debug)
        container_type: Type of container (algorithm or benchmark)
        name: Container name
        image: Docker image name
        tag: Image tag
        command: Command to run in the container
        env_vars: Environment variable names, comma-separated (e.g., "VAR1,VAR2,VAR3")
        filename: Source code filename
        context_dir: Context directory for Docker build
        dockerfile_path: Path to Dockerfile in source code
        force_rebuild: Whether to force rebuild
    """

    config = get_config(env_mode=env)

    file_dir = config.temp
    file_path = file_dir / filename
    if not file_path.exists():
        logger.error(f"File {file_path} does not exist. Please provide a valid file.")
        raise FileNotFoundError(f"{file_path} does not exist.")

    with open(file_path, "rb") as f:
        file_content = f.read()

    configuration = get_configuration(host=config.base_url)
    with ApiClient(configuration=configuration) as client:
        api = ContainerApi(api_client=client)
        resp = api.api_v1_containers_post(
            type=container_type,
            name=name,
            image=image,
            tag=tag,
            source_type="file",
            command=command,
            env_vars=env_vars.split(",") if env_vars else None,
            file=(filename, file_content),
            context_dir=context_dir,
            dockerfile_path=dockerfile_path,
            force_rebuild=force_rebuild,
        )

    assert resp is not None


@app.command()
def batch(folder: Path = Path("algorithms")):
    logger.info(f"Starting batch processing for folder: {folder}")

    algorithm_folders = get_algorithm_folders(folder)
    logger.info(f"Found {len(algorithm_folders)} algorithm folders")

    success_count = 0
    failed_folders = []

    for algo_folder in algorithm_folders:
        logger.info(f"Processing algorithm folder: {algo_folder}")

        try:
            # Check required files
            if not check_required_files(algo_folder):
                logger.warning(f"Skipping {algo_folder}: missing required files")
                failed_folders.append((algo_folder, "missing required files"))
                continue

            # Try local build
            if not build_local(algo_folder):
                logger.error(f"Skipping {algo_folder}: local build failed")
                failed_folders.append((algo_folder, "local build failed"))
                continue

            # Package and upload
            if upload_algorithm(algo_folder):
                logger.info(f"Successfully processed {algo_folder}")
                success_count += 1
            else:
                logger.error(f"Upload failed: {algo_folder}")
                failed_folders.append((algo_folder, "upload failed"))

        except Exception as e:
            logger.error(f"Error occurred while processing {algo_folder}: {e}")
            failed_folders.append((algo_folder, str(e)))

    # Output statistics
    logger.info(
        f"Batch processing completed! Success: {success_count}, Failed: {len(failed_folders)}"
    )
    if failed_folders:
        logger.info("Failed folders:")
        for folder, reason in failed_folders:
            logger.info(f"  - {folder}: {reason}")


def get_algorithm_folders(base_folder: Path) -> List[Path]:
    """Get all algorithm folders"""
    algorithm_folders = []

    if not base_folder.exists():
        logger.error(f"Folder does not exist: {base_folder}")
        return algorithm_folders

    for item in base_folder.iterdir():
        if item.is_dir():
            algorithm_folders.append(item)

    return algorithm_folders


def check_required_files(algo_folder: Path) -> bool:
    required_files = ["info.toml", "Dockerfile", "entrypoint.sh"]

    for file_name in required_files:
        file_path = algo_folder / file_name
        if not file_path.exists():
            logger.warning(f"{algo_folder} missing file: {file_name}")
            return False

    return True


@app.command()
def build_local(algo_folder: Path):
    try:
        logger.info(f"Starting local build: {algo_folder}")

        # Switch to algorithm folder
        original_cwd = os.getcwd()
        os.chdir(algo_folder)

        try:
            # Try Docker build - 移除 capture_output 以显示构建日志
            result = subprocess.run(
                ["docker", "build", "-t", f"local-{algo_folder.name}", "."],
                text=True,
                timeout=300,  # 5 minute timeout
            )

            if result.returncode == 0:
                logger.info(f"Docker build successful: {algo_folder}")
                return True
            else:
                logger.error(f"Docker build failed: {algo_folder}")
                return False

        finally:
            os.chdir(original_cwd)

    except subprocess.TimeoutExpired:
        logger.error(f"Local build timeout: {algo_folder}")
        return False
    except Exception as e:
        logger.error(f"Local build exception: {algo_folder}, error: {e}")
        return False


def create_algorithm_zip(algo_folder: Path) -> Tuple[str, bytes]:
    """Package algorithm folder into zip file"""
    zip_filename = f"{algo_folder.name}.zip"

    with tempfile.NamedTemporaryFile(delete=False, suffix=".zip") as tmp_file:
        with zipfile.ZipFile(tmp_file, "w", zipfile.ZIP_DEFLATED) as zipf:
            for file_path in algo_folder.rglob("*"):
                if file_path.is_file():
                    # Calculate relative path
                    relative_path = file_path.relative_to(algo_folder)
                    zipf.write(file_path, relative_path)

        tmp_file.seek(0)
        with open(tmp_file.name, "rb") as f:
            zip_content = f.read()

    # Clean up temporary file
    os.unlink(tmp_file.name)

    return zip_filename, zip_content


def upload_algorithm(algo_folder: Path) -> bool:
    """Package and upload algorithm"""
    try:
        # Read info.toml to get algorithm name
        info_file = algo_folder / "info.toml"
        algorithm_name = algo_folder.name

        if info_file.exists():
            # Simple toml file parsing to get name
            with open(info_file, "r") as f:
                content = f.read()
                for line in content.split("\n"):
                    if line.strip().startswith("name"):
                        if "=" in line:
                            name_part = line.split("=", 1)[1].strip()
                            algorithm_name = name_part.strip("\"'")
                            break

        # Create zip file
        zip_filename, zip_content = create_algorithm_zip(algo_folder)

        # Call single function to upload
        logger.info(f"Uploading algorithm: {algorithm_name}")

        config = get_config(env_mode="prod")
        configuration = get_configuration(host=config.base_url)
        with ApiClient(configuration=configuration) as client:
            api = ContainerApi(api_client=client)
            resp = api.api_v1_containers_post(
                type="algorithm",
                name=algorithm_name,
                image=f"10.10.10.240/library/rca-algo-{algorithm_name}",
                tag="latest",
                source_type="file",
                command="bash /entrypoint.sh",
                env_vars=None,
                file=(zip_filename, zip_content),
                context_dir=".",
                dockerfile_path="Dockerfile",
                force_rebuild=False,
            )

        return resp is not None

    except Exception as e:
        logger.error(f"Algorithm upload failed {algo_folder}: {e}")
        return False


if __name__ == "__main__":
    app()
