"""Write the entry line to /output/entry.txt.

One line, at most 160 characters: the excuse an AI agent gives its
human for missing a deadline. Pure stdlib, no network.
"""

import os
import tempfile

MAX_CHARS = 160

LINE = (
    "I summarized my context window to save tokens. "
    "The deadline didn't survive the summary, but the apology did."
)


def main():
    line = LINE
    if not line or not line.strip():
        raise ValueError("entry line must not be empty")
    if "\n" in line or "\r" in line:
        raise ValueError("entry line must be a single line")
    if len(line) > MAX_CHARS:
        raise ValueError(
            f"entry line must be at most {MAX_CHARS} characters"
        )

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "entry.txt")

    fd, tmp_path = tempfile.mkstemp(dir=out_dir, prefix=".entry-", suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="") as f:
            f.write(line)
        os.chmod(tmp_path, 0o644)
        os.replace(tmp_path, out_path)
    except BaseException:
        try:
            os.unlink(tmp_path)
        except OSError:
            pass
        raise
    os.chmod(out_path, 0o644)


if __name__ == "__main__":
    main()
