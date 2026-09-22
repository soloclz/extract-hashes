from pathlib import Path
import subprocess
import sys
import tempfile


def run_cli(content: str, *args: str) -> subprocess.CompletedProcess[str]:
    with tempfile.TemporaryDirectory() as folder:
        source = Path(folder) / "evidence.html"
        source.write_text(content, encoding="utf-8")
        return subprocess.run(
            [sys.executable, "-m", "extract_hashes", str(source), *args],
            capture_output=True,
            text=True,
        )


def test_extracts_normalizes_and_deduplicates():
    digest = "665A50AC9EAA781E4F7F04199DB97A11"
    result = run_cli(f"password={digest}\nagain={digest.lower()}\n")
    assert result.returncode == 0, result.stderr
    assert result.stdout == digest.lower() + "\n"
    assert "32-hex: 1" in result.stderr
    assert "MD5, MD4, NTLM" in result.stderr


def test_rejects_embedded_or_unsupported_lengths():
    result = run_cli(
        "x" + "a" * 32 + "f trailing=" + "b" * 31 + " valid=" + "c" * 40
    )
    assert result.returncode == 0, result.stderr
    assert result.stdout == "c" * 40 + "\n"


def test_output_file_contains_only_hashes():
    with tempfile.TemporaryDirectory() as folder:
        source = Path(folder) / "input.txt"
        output = Path(folder) / "hashes.txt"
        source.write_text("value=" + "d" * 64, encoding="utf-8")
        result = subprocess.run(
            [sys.executable, "-m", "extract_hashes", str(source), "-o", str(output)],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0, result.stderr
        assert result.stdout == ""
        assert output.read_text(encoding="utf-8") == "d" * 64 + "\n"
        assert str(output) in result.stderr


def test_stdin_and_version():
    digest = "e" * 32
    result = subprocess.run(
        [sys.executable, "-m", "extract_hashes", "-"],
        input=digest,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
    assert result.stdout == digest + "\n"

    version = subprocess.run(
        [sys.executable, "-m", "extract_hashes", "--version"],
        capture_output=True,
        text=True,
    )
    assert version.returncode == 0
    assert version.stdout.strip() == "extract-hashes 0.1.0"
