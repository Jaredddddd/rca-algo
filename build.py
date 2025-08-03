import subprocess
from pathlib import Path
from typing import List, Optional, Dict, Any
import toml
import typer
from rich.console import Console
from rich.table import Table

console = Console()
app = typer.Typer(
    name="build-push",
    help="RCA algorithm Docker image build and push tool",
    add_completion=False,
)


class DockerBuildError(Exception):
    pass


def load_config(config_file: Optional[Path] = None) -> Dict[str, Any]:
    """Load configuration file"""
    default_config = {
        "docker": {
            "registry": "10.10.10.240",
            "namespace": "library",
            "default_tag": "latest",
        },
        "build": {"algorithms_dir": "algorithms", "no_cache": False, "platform": ""},
        "push": {"auto_push": False},
        "algorithms": {},
    }

    if config_file and config_file.exists():
        try:
            file_config = toml.load(config_file)
            # Merge configuration
            for section, values in file_config.items():
                if section in default_config:
                    if isinstance(default_config[section], dict):
                        default_config[section].update(values)
                    else:
                        default_config[section] = values
                else:
                    default_config[section] = values
        except Exception as e:
            console.print(
                f"[yellow]Warning: Unable to load config file {config_file}: {e}[/yellow]"
            )

    return default_config


class AlgorithmConfig:
    """Algorithm configuration class"""

    def __init__(self, path: Path, global_config: Optional[Dict[str, Any]] = None):
        self.path = path
        self.name = path.name
        self.info_file = path / "info.toml"
        self.dockerfile = path / "Dockerfile"
        self.global_config = global_config or {}

    @property
    def has_dockerfile(self) -> bool:
        """Check if Dockerfile exists"""
        return self.dockerfile.exists()

    @property
    def config(self) -> Dict[str, Any]:
        """Read info.toml configuration"""
        if self.info_file.exists():
            return toml.load(self.info_file)
        return {}

    @property
    def display_name(self) -> str:
        """Get display name"""
        return self.config.get("name", self.name)

    def get_algorithm_config(self, key: str, default: Any = None) -> Any:
        """Get algorithm-specific configuration"""
        algo_config = self.global_config.get("algorithms", {}).get(self.name, {})
        return algo_config.get(key, default)


def run_command(
    cmd: List[str], cwd: Optional[Path] = None, capture_output: bool = False
) -> subprocess.CompletedProcess:
    """Run command"""
    try:
        result = subprocess.run(
            cmd, cwd=cwd, check=True, capture_output=capture_output, text=True
        )
        return result
    except subprocess.CalledProcessError as e:
        if capture_output:
            console.print(f"[red]Command execution failed: {' '.join(cmd)}[/red]")
            console.print(f"[red]Error output: {e.stderr}[/red]")
        raise DockerBuildError(f"Command execution failed: {e}")


def discover_algorithms(
    algorithms_dir: Path, global_config: Optional[Dict[str, Any]] = None
) -> List[AlgorithmConfig]:
    """Discover all algorithms"""
    algorithms = []

    if not algorithms_dir.exists():
        console.print(
            f"[red]Algorithms directory does not exist: {algorithms_dir}[/red]"
        )
        return algorithms

    for item in algorithms_dir.iterdir():
        if item.is_dir() and not item.name.startswith("."):
            algo = AlgorithmConfig(item, global_config)
            if algo.has_dockerfile:
                algorithms.append(algo)
            else:
                console.print(
                    f"[yellow]Skipping {item.name}: Dockerfile not found[/yellow]"
                )

    return sorted(algorithms, key=lambda x: x.name)


def build_image(
    algorithm: AlgorithmConfig,
    registry: str,
    namespace: str,
    tag: str,
    no_cache: bool = False,
    platform: Optional[str] = None,
) -> str:
    """Build Docker image"""
    image_name = f"{registry}/{namespace}/rca-algo-{algorithm.name}"
    full_image = f"{image_name}:{tag}"

    cmd = ["docker", "build"]

    if no_cache:
        cmd.append("--no-cache")

    if platform:
        cmd.extend(["--platform", platform])

    cmd.extend(["-t", full_image, "."])

    console.print(f"[blue]Building image: {full_image}[/blue]")

    try:
        run_command(cmd, cwd=algorithm.path)
        console.print(f"[green]✓ Build successful: {full_image}[/green]")
        return full_image
    except DockerBuildError:
        console.print(f"[red]✗ Build failed: {full_image}[/red]")
        raise


def push_image(image: str) -> None:
    """Push Docker image"""
    console.print(f"[blue]Pushing image: {image}[/blue]")

    try:
        run_command(["docker", "push", image])
        console.print(f"[green]✓ Push successful: {image}[/green]")
    except DockerBuildError:
        console.print(f"[red]✗ Push failed: {image}[/red]")
        raise


def check_docker() -> bool:
    """Check if Docker is available"""
    try:
        run_command(["docker", "--version"], capture_output=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


@app.command()
def list_algorithms(
    algorithms_dir: Optional[Path] = typer.Option(
        None, "--algorithms-dir", "-d", help="Algorithms directory path"
    ),
    config_file: Optional[Path] = typer.Option(
        Path("build_config.toml"), "--config", "-c", help="Configuration file path"
    ),
):
    """List all buildable algorithms"""
    # Load configuration
    config = load_config(config_file)

    # Use default values from config file
    if algorithms_dir is None:
        algorithms_dir = Path(config["build"]["algorithms_dir"])

    algorithms = discover_algorithms(algorithms_dir, config)

    if not algorithms:
        console.print("[yellow]No buildable algorithms found[/yellow]")
        return

    table = Table(title="Buildable Algorithms")
    table.add_column("Name", style="cyan")
    table.add_column("Display Name", style="green")
    table.add_column("Path", style="blue")

    for algo in algorithms:
        table.add_row(algo.name, algo.display_name, str(algo.path))

    console.print(table)


@app.command()
def build(
    algorithms_dir: Optional[Path] = typer.Option(
        None, "--algorithms-dir", "-d", help="Algorithms directory path"
    ),
    registry: Optional[str] = typer.Option(
        None, "--registry", "-r", help="Docker registry address"
    ),
    namespace: Optional[str] = typer.Option(
        None, "--namespace", "-n", help="Namespace"
    ),
    tag: Optional[str] = typer.Option(None, "--tag", "-t", help="Image tag"),
    algorithms: Optional[List[str]] = typer.Option(
        None,
        "--algorithm",
        "-a",
        help="Specify algorithms to build (can be used multiple times)",
    ),
    exclude: Optional[List[str]] = typer.Option(
        None, "--exclude", "-e", help="Exclude algorithms (can be used multiple times)"
    ),
    no_cache: Optional[bool] = typer.Option(
        None, "--no-cache", help="Build without cache"
    ),
    platform: Optional[str] = typer.Option(
        None, "--platform", help="Target platform (e.g.: linux/amd64,linux/arm64)"
    ),
    push: Optional[bool] = typer.Option(
        None, "--push", "-p", help="Push images after build"
    ),
    dry_run: bool = typer.Option(
        False, "--dry-run", help="Dry run (don't actually execute build)"
    ),
    config_file: Optional[Path] = typer.Option(
        Path("build_config.toml"), "--config", "-c", help="Configuration file path"
    ),
):
    """Build algorithm images"""

    # Load configuration
    config = load_config(config_file)

    # Use default values from config file (if command line arguments not provided)
    if algorithms_dir is None:
        algorithms_dir = Path(config["build"]["algorithms_dir"])
    if registry is None:
        registry = config["docker"]["registry"]
    if namespace is None:
        namespace = config["docker"]["namespace"]
    if tag is None:
        tag = config["docker"]["default_tag"]
    if no_cache is None:
        no_cache = config["build"]["no_cache"]
    if platform is None:
        platform = config["build"]["platform"] or None
    if push is None:
        push = config["push"]["auto_push"]

    # Ensure all required parameters are not None
    assert registry is not None
    assert namespace is not None
    assert tag is not None
    assert no_cache is not None
    assert push is not None

    # Check Docker
    if not dry_run and not check_docker():
        console.print(
            "[red]Error: Docker is not available, please ensure Docker is installed and running[/red]"
        )
        raise typer.Exit(1)

    # Discover algorithms
    all_algorithms = discover_algorithms(algorithms_dir, config)

    if not all_algorithms:
        console.print("[red]No buildable algorithms found[/red]")
        raise typer.Exit(1)

    # Filter algorithms
    if algorithms:
        # Specific algorithms specified
        selected_algorithms = [
            algo for algo in all_algorithms if algo.name in algorithms
        ]
        missing = set(algorithms) - {algo.name for algo in selected_algorithms}
        if missing:
            console.print(
                f"[yellow]Warning: The following algorithms were not found: {', '.join(missing)}[/yellow]"
            )
    else:
        # Use all algorithms
        selected_algorithms = all_algorithms

    # Exclude algorithms
    if exclude:
        selected_algorithms = [
            algo for algo in selected_algorithms if algo.name not in exclude
        ]

    if not selected_algorithms:
        console.print("[yellow]No algorithms to build[/yellow]")
        return

    # Display build plan
    console.print("\n[bold]Build Plan:[/bold]")
    for algo in selected_algorithms:
        image_name = f"{registry}/{namespace}/rca-algo-{algo.name}:{tag}"
        console.print(f"  • {algo.name} -> {image_name}")

    if dry_run:
        console.print("\n[yellow]Dry run completed[/yellow]")
        return

    # Confirm build
    if not typer.confirm("\nContinue with build?"):
        console.print("Cancelled")
        return

    # Start building
    console.print(
        f"\n[bold]Starting to build {len(selected_algorithms)} algorithms...[/bold]"
    )

    success_count = 0
    failed_algorithms = []

    for i, algo in enumerate(selected_algorithms, 1):
        console.print(
            f"\n[bold cyan]({i}/{len(selected_algorithms)}) Processing algorithm: {algo.name}[/bold cyan]"
        )

        try:
            # Build image
            image = build_image(algo, registry, namespace, tag, no_cache, platform)

            # Push image
            if push:
                push_image(image)

            success_count += 1

        except DockerBuildError:
            failed_algorithms.append(algo.name)
            console.print(f"[red]Algorithm {algo.name} processing failed[/red]")

    # Display results
    console.print("\n[bold]Build completed![/bold]")
    console.print(f"[green]Successful: {success_count}[/green]")

    if failed_algorithms:
        console.print(f"[red]Failed: {len(failed_algorithms)}[/red]")
        console.print(f"[red]Failed algorithms: {', '.join(failed_algorithms)}[/red]")
        raise typer.Exit(1)


@app.command()
def push_only(
    registry: str = typer.Option(
        "10.10.10.240", "--registry", "-r", help="Docker registry address"
    ),
    namespace: str = typer.Option("library", "--namespace", "-n", help="Namespace"),
    tag: str = typer.Option("latest", "--tag", "-t", help="Image tag"),
    algorithms: List[str] = typer.Argument(..., help="Algorithm names to push"),
):
    """Push pre-built images only"""

    if not check_docker():
        console.print("[red]Error: Docker is not available[/red]")
        raise typer.Exit(1)

    console.print(f"[bold]Pushing {len(algorithms)} images...[/bold]")

    failed_images = []

    for algo in algorithms:
        image = f"{registry}/{namespace}/rca-algo-{algo}:{tag}"
        try:
            push_image(image)
        except DockerBuildError:
            failed_images.append(image)

    if failed_images:
        console.print(f"[red]Failed to push images: {', '.join(failed_images)}[/red]")
        raise typer.Exit(1)

    console.print("[green]All images pushed successfully![/green]")


if __name__ == "__main__":
    app()
