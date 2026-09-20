from rich.console import Console, Group
from rich.panel import Panel
from rich.align import Align
from rich.text import Text
from rich.table import Table
from rich.prompt import Confirm
from rich.progress import (
    Progress,
    SpinnerColumn,
    TextColumn,
    BarColumn,
    TaskProgressColumn,
)


console = Console()


def show_banner():
    """
    Display the MediaSorter startup banner.
    """

    banner = r"""
███╗   ███╗███████╗██████╗ ██╗ █████╗
████╗ ████║██╔════╝██╔══██╗██║██╔══██╗
██╔████╔██║█████╗  ██║  ██║██║███████║
██║╚██╔╝██║██╔══╝  ██║  ██║██╔══██║
██║ ╚═╝ ██║███████╗██████╔╝██║██║  ██║
╚═╝     ╚═╝╚══════╝╚═════╝ ╚═╝╚═╝  ╚═╝

                 MEDIA SORTER
    """

    text = Text(banner)
    text.justify = "center"

    console.print(
        Panel(
            Align.center(text),
            border_style="cyan",
            padding=(1, 2),
        )
    )

    console.print()


def create_progress():
    """
    Create the Rich progress bar.
    """

    return Progress(
        SpinnerColumn(),
        TextColumn(
            "[bold cyan]{task.description}"
        ),
        BarColumn(),
        TaskProgressColumn(),
    )


def create_dashboard(
    progress,
    scanned,
    sorted_count,
    skipped,
    failed,
    directories_created,
    current_file,
):
    """
    Create the live sorting dashboard.
    """

    stats = Table(
        border_style="cyan",
        show_header=False,
    )

    stats.add_column("Category")
    stats.add_column(
        "Count",
        justify="right",
    )

    stats.add_row(
        "Files scanned",
        str(scanned),
    )

    stats.add_row(
        "Files sorted",
        str(sorted_count),
    )

    stats.add_row(
        "Files skipped",
        str(skipped),
    )

    stats.add_row(
        "Files failed",
        str(failed),
    )

    stats.add_row(
        "Directories created",
        str(directories_created),
    )

    current_file_panel = Panel(
        f"[bold]{current_file}[/bold]",
        title="Current file",
        border_style="cyan",
    )

    return Group(
        progress,
        current_file_panel,
        stats,
    )


def show_success():
    """
    Display successful completion message.
    """

    console.print()

    console.print(
        Panel(
            "[bold green]Sorting completed successfully![/bold green]",
            border_style="green",
        )
    )


def show_summary(result):
    """
    Display the final sorting statistics.
    """

    console.print()

    table = Table(
        title="Sorting Summary",
        border_style="cyan",
    )

    table.add_column("Category")
    table.add_column(
        "Count",
        justify="right",
    )

    table.add_row(
        "Files scanned",
        str(result.files_scanned),
    )

    table.add_row(
        "Files sorted",
        str(result.files_sorted),
    )

    table.add_row(
        "Files skipped",
        str(result.files_skipped),
    )

    table.add_row(
        "Files failed",
        str(result.files_failed),
    )

    table.add_row(
        "Directories created",
        str(result.directories_created),
    )

    console.print(table)
    console.print()

def ask_delete_permission(file_count):

    console.print()

    console.print(
        Panel(
            f"[green]✓ {file_count} files were successfully sorted.[/green]\n\n"
            "The original files are still present in the "
            "source folder.\n\n"
            f"[yellow]If you continue, these {file_count} "
            "original files will be deleted.[/yellow]",
            title="Cleanup",
            border_style="yellow",
        )
    )

    return Confirm.ask(
        "Delete original files?",
        default=False,
    )
