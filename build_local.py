#!/usr/bin/env -S uv run -s
import os
import subprocess
import tempfile
import zipfile
from pathlib import Path
from typing import List, Tuple, Dict, Any

import tomli
from loguru import logger
from typer import Typer, Option

from rcabench_platform.v2.cli.main import app, logger
from rcabench_platform.v2.logging import timeit
from rcabench_platform.v2.config import get_config
from rcabench_platform.v2.clients.rcabench_ import RCABenchClient
from rcabench.openapi.api import ContainersApi

app = Typer()


@app.command()
@timeit()
def single(
    env: str = "prod",
    container_type: str = "algorithm",
    name: str = "traceback-test",
    image: str = "10.10.10.240/library/rca-algo-traceback-test-local-file",
    tag: str = "latest",
    command: str = "bash /entrypoint.sh",
    env_vars: list[str] | None = None,
    filename: str = "traceback.zip",
    context_dir: str = ".",
    dockerfile_path: str = "Dockerfile",
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

    with RCABenchClient() as api_client:
        api = ContainersApi(api_client=api_client)
        resp = api.api_v2_containers_post(
            type=container_type,
            name=name,
            image=image,
            tag=tag,
            command=command,
            file=(filename, file_content),
            context_dir=context_dir,
            dockerfile_path=dockerfile_path,
            env_vars=env_vars
        )

    assert resp is not None


@app.command()
def batch(
    folder: Path = Path("algorithms"), 
    build_source_type: str = Option(
        "file",
        "--build-source-type",
        "-t",
        help="Build source type: 'file' (upload source code for backend build) or 'harbor' (use pre-built image from harbor)"
    )
):
    """
    Batch process all algorithms in the folder
    
    Two upload modes are supported:
    
    📁 FILE MODE (default): Upload source code files to backend for building
    - Creates ZIP package from algorithm folder
    - Uploads source code to backend
    - Backend builds Docker image from source
    - Requires: Dockerfile, entrypoint.sh, info.toml
    
    🐳 HARBOR MODE: Use pre-built images from Harbor registry
    - No file upload required
    - Assumes image is already built and pushed to Harbor
    - Backend uses existing Harbor image
    - Requires: Image must exist in Harbor registry
    
    Args:
        folder: Folder containing algorithm directories
        build_source_type: Build source type - "file" for file upload, "harbor" for harbor image
    """
    # Validate build_source_type
    if build_source_type not in ["file", "harbor"]:
        logger.error(f"Invalid build_source_type: {build_source_type}. Must be 'file' or 'harbor'")
        logger.info("📁 FILE MODE: Upload source code for backend build")
        logger.info("🐳 HARBOR MODE: Use pre-built image from Harbor")
        return
    
    logger.info(f"Starting batch processing for folder: {folder}")
    if build_source_type == "file":
        logger.info("📁 Using FILE MODE - uploading source code for backend build")
    else:
        logger.info("🐳 Using HARBOR MODE - using pre-built image from Harbor")

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

            # Try local build (only for file mode)
            if build_source_type == "file":
                if not build_local(algo_folder):
                    logger.error(f"Skipping {algo_folder}: local build failed")
                    failed_folders.append((algo_folder, "local build failed"))
                    continue

            # Package and upload
            if upload_algorithm(algo_folder, build_source_type):
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


def parse_toml_config(info_file: Path) -> Tuple[str, Dict[str, str]]:
    """Parse info.toml file to extract name and env_vars"""
    algorithm_name = info_file.parent.name
    env_vars = {}
    
    if info_file.exists():
        try:
            with open(info_file, "rb") as f:
                config = tomli.load(f)
                
            if "name" in config:
                algorithm_name = config["name"]
            if "env_vars" in config:
                env_vars = config["env_vars"]
                
        except Exception as e:
            logger.warning(f"Failed to parse TOML file {info_file}: {e}")
    
    return algorithm_name, env_vars


def upload_algorithm(algo_folder: Path, build_source_type: str = "file") -> bool:
    """Package and upload algorithm
    
    Args:
        algo_folder: Algorithm folder path
        build_source_type: Build source type - "file" for file upload, "harbor" for harbor image
    """
    # Validate build_source_type
    if build_source_type not in ["file", "harbor"]:
        logger.error(f"Invalid build_source_type: {build_source_type}")
        return False
    
    try:
        # Read info.toml to get algorithm name and env_vars
        info_file = algo_folder / "info.toml"
        algorithm_name, env_vars = parse_toml_config(info_file)

        # Convert env_vars dict to list of keys only
        env_vars_list = None
        if env_vars:
            env_vars_list = list(env_vars.keys())

        logger.info(f"Uploading algorithm: {algorithm_name} with build_source_type: {build_source_type}")
        if env_vars:
            logger.info(f"Environment variables: {env_vars}")

        with RCABenchClient(base_url="http://10.10.10.126:8082") as api_client:
            api = ContainersApi(api_client=api_client)
            
            if build_source_type == "harbor":
                # Harbor mode - only pass image and tag
                resp = api.api_v2_containers_post(
                    type="algorithm",
                    name=algorithm_name,
                    image=f"10.10.10.240/library/rca-algo-{algorithm_name}",
                    tag="latest",
                    command="bash /entrypoint.sh",
                    env_vars=env_vars_list,
                    build_source_type="harbor",
                    harbor_image=f"10.10.10.240/library/rca-algo-{algorithm_name}",
                    harbor_tag="latest",
                )
            elif build_source_type == "file":
                # File mode - create zip and upload file
                zip_filename, zip_content = create_algorithm_zip(algo_folder)
                resp = api.api_v2_containers_post(
                    type="algorithm",
                    name=algorithm_name,
                    image=f"10.10.10.240/library/rca-algo-{algorithm_name}",
                    tag="latest",
                    command="bash /entrypoint.sh",
                    env_vars=env_vars_list,
                    file=(zip_filename, zip_content),
                    context_dir=".",
                    dockerfile_path="Dockerfile",
                )
            else:
                raise ValueError(f"Invalid build_source_type: {build_source_type}")

        logger.info(f"resp is {resp}")
        return resp.code == 200

    except Exception as e:
        logger.error(f"Algorithm upload failed {algo_folder}: {e}")
        return False


if __name__ == "__main__":
    app()
