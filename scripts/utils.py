from pathlib import Path

def write_file(path: Path, content: str) -> None:
    """
    Write text to a file, creating parent directories if needed.
    """

    path.parent.mkdir(parents=True, exist_ok=True)

    path.write_text(
        content,
        encoding="utf-8"
        )