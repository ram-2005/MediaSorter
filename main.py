from rich.live import Live

from controller import (
    main as sort_media,
    UNSORTED_DIR,
    delete_sorted_files,
)

from ui import (
    show_banner,
    show_summary,
    show_success,
    create_progress,
    create_dashboard,
    ask_delete_permission,
)


def main():

    # --------------------------------
    # Startup
    # --------------------------------

    show_banner()

    # --------------------------------
    # Count files
    # --------------------------------

    files = [
        file
        for file in UNSORTED_DIR.iterdir()
        if file.is_file()
    ]

    total_files = len(files)

    # --------------------------------
    # Create progress bar
    # --------------------------------

    progress = create_progress()

    task = progress.add_task(
        "Starting...",
        total=total_files,
    )

    # --------------------------------
    # Initial dashboard
    # --------------------------------

    dashboard = create_dashboard(
        progress=progress,
        scanned=0,
        sorted_count=0,
        skipped=0,
        failed=0,
        directories_created=0,
        current_file="Preparing...",
    )

    # --------------------------------
    # Live dashboard
    # --------------------------------

    with Live(
        dashboard,
        refresh_per_second=10,
    ) as live:

        def update_progress(
            scanned,
            sorted_count,
            skipped,
            failed,
            directories_created,
            file,
        ):
            """
            Called by the controller after each file.
            """

            progress.update(
                task,
                completed=scanned,
                description="Sorting media...",
            )

            live.update(
                create_dashboard(
                    progress=progress,
                    scanned=scanned,
                    sorted_count=sorted_count,
                    skipped=skipped,
                    failed=failed,
                    directories_created=directories_created,
                    current_file=file.name,
                )
            )

        # --------------------------------
        # Run sorter
        # --------------------------------

        result = sort_media(
            progress_callback=update_progress,
        )

    # --------------------------------
    # Final result
    # --------------------------------

    show_success()

    if result.sorted_files:

        if ask_delete_permission(
                len(result.sorted_files)
                ):

            deleted, failed = delete_sorted_files(
                    result.sorted_files
                    )

            print()
            print(
                f"Deleted: {deleted}"
            )

            if failed:
                print(
                    f"Failed to delete: {failed}"
                )

        else:
            print()
            print("Original files were kept")


if __name__ == "__main__":
    main()
