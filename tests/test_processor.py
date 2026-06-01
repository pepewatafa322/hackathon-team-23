import pytest
from pathlib import Path

from src.processor import EmailCopier


@pytest.fixture
def email_copier(tmp_path: Path):
    return EmailCopier(tmp_path)


def test_create_processed_directory(tmp_path: Path):
    EmailCopier(tmp_path)

    assert (tmp_path / "processed").exists()
    assert (tmp_path / "processed").is_dir()


def test_copy_file_to_existing_category(
    tmp_path: Path,
    email_copier: EmailCopier
):
    src_file = tmp_path / "mail.txt"

    src_file.write_text("test content")

    email_copier.copy(src_file, "spam")

    copied_file = (tmp_path / "processed" / "spam" / "mail.txt")

    assert copied_file.exists()
    assert copied_file.read_text() == "test content"


def test_copy_file_to_unclassified_when_unknown_category(
    tmp_path: Path,
    email_copier: EmailCopier
):
    src_file = tmp_path / "mail.txt"

    src_file.write_text("test content")

    email_copier.copy(src_file, "some_unknown_category")

    copied_file = (tmp_path / "processed" / "unclassified" / "mail.txt")

    assert copied_file.exists()
    assert copied_file.read_text() == "test content"


def test_copy_preserves_original_file(
    tmp_path: Path,
    email_copier: EmailCopier
):
    src_file = tmp_path / "mail.txt"

    src_file.write_text("original content")

    email_copier.copy(src_file, "spam")

    assert src_file.exists()
    assert src_file.read_text() == "original content"


def test_copy_missing_file_raises_error(
    email_copier: EmailCopier
):
    with pytest.raises(FileNotFoundError):
        email_copier.copy(Path("missing_file.txt"), "spam")


def test_copy_multiple_files(
    tmp_path: Path,
    email_copier: EmailCopier
):
    first = tmp_path / "first.txt"
    second = tmp_path / "second.txt"

    first.write_text("first")
    second.write_text("second")

    email_copier.copy(first, "spam")
    email_copier.copy(second, "spam")

    assert (tmp_path / "processed" / "spam" / "first.txt").exists()

    assert (tmp_path / "processed" / "spam" / "second.txt").exists()


def test_copy_to_access_category(tmp_path: Path, email_copier: EmailCopier):
    src_file = tmp_path / "access_request.txt"

    src_file.write_text("vpn access")

    email_copier.copy(src_file, "access")

    copied_file = (tmp_path / "processed" / "access" / "access_request.txt")

    assert copied_file.exists()


def test_copy_to_incident_category(tmp_path: Path, email_copier: EmailCopier):
    src_file = tmp_path / "incident.txt"

    src_file.write_text("critical incident")

    email_copier.copy(src_file, "incident")

    copied_file = (tmp_path / "processed" / "incident" / "incident.txt")

    assert copied_file.exists()

def test_create_all_category_directories(tmp_path: Path):
    EmailCopier(tmp_path)

    processed = tmp_path / "processed"

    assert processed.exists()

    assert (processed / "spam").exists()
    assert (processed / "incident").exists()
    assert (processed / "request").exists()
    assert (processed / "hardware").exists()
    assert (processed / "access").exists()
    assert (processed / "documents").exists()
    assert (processed / "hr").exists()
    assert (processed / "monitoring").exists()
    assert (processed / "internal").exists()
    assert (processed / "unclassified").exists()