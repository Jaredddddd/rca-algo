"""
Typer CLI application for MicroDig algorithm.

This module provides a command-line interface for running MicroDig
analysis using typer.
"""

import json
from pathlib import Path
from typing import Optional

import typer
from rcabench_platform.v2.logging import logger
from rich.console import Console
from rich.table import Table

from .platform_adapter import microdig_analysis

app = typer.Typer(help="MicroDig: Microservice Failure Root Cause Analysis")
console = Console()


@app.command()
def analyze(
    input_folder: Path = typer.Argument(
        ...,
        help="Path to folder containing parquet data files (normal_traces.parquet, abnormal_traces.parquet, etc.)",
        exists=True,
        file_okay=False,
        dir_okay=True,
    ),
    output_file: Optional[Path] = typer.Option(
        None, "--output", "-o", help="Output file for results (JSON format)"
    ),
    alarm_item: Optional[str] = typer.Option(
        None,
        "--alarm-item",
        "-a",
        help="Name of the alarmed service/component (auto-detected from conclusion.parquet if not provided)",
    ),
    root_cause: Optional[str] = typer.Option(
        None, "--root-cause", "-r", help="Ground truth root cause (for evaluation)"
    ),
    test_length_before: int = typer.Option(
        10,
        "--test-before",
        "-tb",
        help="Time window before alarm for testing (minutes)",
    ),
    test_length_after: int = typer.Option(
        10, "--test-after", "-ta", help="Time window after alarm for testing (minutes)"
    ),
    train_length: int = typer.Option(
        60,
        "--train-length",
        "-tl",
        help="Historical data window for training (minutes)",
    ),
    search_method: str = typer.Option(
        "all",
        "--search-method",
        "-sm",
        help="Strategy for finding candidates",
    ),
    rank_method: str = typer.Option(
        "random walk",
        "--rank-method",
        "-rm",
        help="Ranking algorithm",
    ),
    level: str = typer.Option(
        "method",
        "--level",
        "-l",
        help="Analysis level",
    ),
    rev_weight: float = typer.Option(
        0.2, "--rev-weight", "-rw", help="Weight for reverse edges in graph"
    ),
    beta: float = typer.Option(
        0.1, "--beta", "-b", help="Weight factor for mixed node ranking"
    ),
    verbose: bool = typer.Option(
        False, "--verbose", "-v", help="Enable verbose logging"
    ),
):
    """
    Analyze microservice failure data using MicroDig algorithm.

    This command processes trace, metrics, and log data from parquet files
    to identify potential root causes of microservice failures.
    """

    if verbose:
        logger.info("Verbose mode enabled")

    console.print("[bold blue]MicroDig Analysis[/bold blue]")
    console.print(f"Input folder: {input_folder}")
    console.print(f"Analysis level: {level}")
    console.print(f"Search method: {search_method}")
    console.print(f"Rank method: {rank_method}")

    if alarm_item:
        console.print(f"Alarm item: {alarm_item}")
    if root_cause:
        console.print(f"Root cause (ground truth): {root_cause}")

    console.print()

    with console.status("[bold green]Running MicroDig analysis..."):
        try:
            # Run analysis
            result = microdig_analysis(
                input_folder=input_folder,
                alarm_item=alarm_item,
                root_cause=root_cause,
                test_length_before=test_length_before,
                test_length_after=test_length_after,
                train_length=train_length,
                search_method=search_method,
                rank_method=rank_method,
                level=level,
                rev_weight=rev_weight,
                beta=beta,
            )

        except Exception as e:
            console.print(f"[bold red]Error:[/bold red] {str(e)}")
            raise typer.Exit(1)

    # Check for errors
    if "error" in result:
        console.print(f"[bold red]Analysis failed:[/bold red] {result['error']}")
        raise typer.Exit(1)

    # Display results
    console.print("[bold green]Analysis completed successfully![/bold green]")

    if "processing_time" in result:
        console.print(f"Processing time: {result['processing_time']:.2f}s")

    # Create results table
    ranks = result.get("ranks", [])
    if ranks:
        table = Table(title="Root Cause Rankings")
        table.add_column("Rank", style="cyan", no_wrap=True)
        table.add_column("Service/Component", style="green")
        table.add_column("Ground Truth", style="yellow")

        for i, service in enumerate(ranks[:10], 1):  # Show top 10
            is_ground_truth = "✓" if root_cause and service == root_cause else ""
            table.add_row(str(i), service, is_ground_truth)

        console.print(table)
    else:
        console.print("[yellow]No rankings found[/yellow]")

    # Show algorithm details
    if "algorithms_results" in result and verbose:
        console.print("\n[bold]Algorithm Details:[/bold]")
        algorithms_results = result["algorithms_results"]

        # algorithms_results is an AlgorithmOutput object, not a dict
        if (
            hasattr(algorithms_results, "service_ranking")
            and algorithms_results.service_ranking
        ):
            console.print(
                f"\nService Rankings ({len(algorithms_results.service_ranking)} total):"
            )
            for i, service_name in enumerate(
                algorithms_results.service_ranking[:10], 1
            ):
                console.print(f"  {i}. {service_name}")

        if (
            hasattr(algorithms_results, "evaluation_results")
            and algorithms_results.evaluation_results
        ):
            console.print("\nEvaluation Results:")
            for key, value in algorithms_results.evaluation_results.items():
                console.print(f"  {key}: {value}")

    # Save results to file if specified
    if output_file:
        try:
            with open(output_file, "w") as f:
                json.dump(result, f, indent=2, default=str)
            console.print(f"\n[green]Results saved to {output_file}[/green]")
        except Exception as e:
            console.print(f"[red]Failed to save results: {str(e)}[/red]")


@app.command()
def validate(
    input_folder: Path = typer.Argument(
        ...,
        help="Path to folder containing data files",
        exists=True,
        file_okay=False,
        dir_okay=True,
    ),
):
    """
    Validate input data format and structure.

    This command checks if the input folder contains the required
    parquet files and validates their structure.
    """

    console.print(f"[bold blue]Validating data in: {input_folder}[/bold blue]")

    required_files = ["normal_traces.parquet", "abnormal_traces.parquet", "env.json"]

    optional_files = [
        "normal_metrics.parquet",
        "abnormal_metrics.parquet",
        "normal_logs.parquet",
        "abnormal_logs.parquet",
        "normal_metrics_histogram.parquet",
        "abnormal_metrics_histogram.parquet",
    ]

    # Check required files
    missing_required = []
    for file_name in required_files:
        file_path = input_folder / file_name
        if file_path.exists():
            console.print(f"[green]✓[/green] {file_name}")
        else:
            console.print(f"[red]✗[/red] {file_name} (required)")
            missing_required.append(file_name)

    # Check optional files
    for file_name in optional_files:
        file_path = input_folder / file_name
        if file_path.exists():
            console.print(f"[green]✓[/green] {file_name}")
        else:
            console.print(f"[yellow]○[/yellow] {file_name} (optional)")

    if missing_required:
        console.print("\n[bold red]Validation failed![/bold red]")
        console.print(f"Missing required files: {', '.join(missing_required)}")
        raise typer.Exit(1)

    console.print("\n[bold green]Validation passed![/bold green]")

    # Try to load and validate data structure
    try:
        from .data_loader import DataLoader

        loader = DataLoader(input_folder)
        inject_time = loader.get_inject_time()
        console.print(f"Injection time: {inject_time}")

        data = loader.load_all_data()
        for data_type, lazy_frame in data.items():
            if lazy_frame is not None:
                try:
                    sample = lazy_frame.limit(5).collect()
                    console.print(f"{data_type}: {len(sample)} sample rows loaded")
                except Exception as e:
                    console.print(
                        f"[yellow]Warning: Could not sample {data_type}: {str(e)}[/yellow]"
                    )
            else:
                console.print(f"[yellow]{data_type}: Not available[/yellow]")

    except Exception as e:
        console.print(
            f"[yellow]Warning: Could not validate data structure: {str(e)}[/yellow]"
        )


@app.command()
def version():
    """Show MicroDig version information."""
    from . import __author__, __version__

    console.print(f"[bold blue]MicroDig[/bold blue] version {__version__}")
    console.print(f"Author: {__author__}")


if __name__ == "__main__":
    app()
