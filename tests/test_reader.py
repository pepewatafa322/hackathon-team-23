import pytest
from pathlib import Path

from src.reader import EmailReader, FileDecodingError, FileTooLargeError

@pytest.fixture
def email_reader():
    return EmailReader()


def test_discover_files_success(tmp_path: Path, email_reader: EmailReader):
    inbox_path = tmp_path / "inbox"
    inbox_path.mkdir()

    (inbox_path / "mail1.txt").touch()
    (inbox_path / "mail2.json").touch()

    (inbox_path / ".DS_Store").touch()

    (inbox_path / "subdir").mkdir()

    files = email_reader.discover_files(inbox_path)

    assert len(files) == 2

    filenames = sorted(file.name for file in files)

    assert filenames == ["mail1.txt", "mail2.json"]


def test_discover_files_empty(tmp_path: Path, email_reader: EmailReader):
    inbox_path = tmp_path / "empty_inbox"
    inbox_path.mkdir()

    files = email_reader.discover_files(inbox_path)

    assert files == []


def test_discover_files_missing_path(email_reader: EmailReader):
    with pytest.raises(FileNotFoundError, match="Путь inbox_path не существует"):
        email_reader.discover_files(Path("missing_path"))


def test_discover_files_not_directory(tmp_path: Path, email_reader: EmailReader):
    filepath = tmp_path / "file.txt"

    filepath.touch()

    with pytest.raises(NotADirectoryError, match="Путь inbox_path не является папкой"):
        email_reader.discover_files(filepath)


def test_read_empty_file(tmp_path: Path,email_reader: EmailReader):
    filepath = tmp_path / "empty.txt"

    filepath.touch()

    content, file_format = email_reader.read_file(filepath)

    assert content == ""
    assert file_format == "empty"


def test_read_binary(tmp_path: Path, email_reader: EmailReader):
    filepath = tmp_path / "image.jpeg"

    filepath.write_bytes(b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR")

    content, file_format = email_reader.read_file(filepath)

    assert content == ""
    assert file_format == "binary"


def test_read_binary_with_null_byte(tmp_path: Path, email_reader: EmailReader):
    filepath = tmp_path / "text.txt"

    filepath.write_bytes(b"hello\x00world")

    content, file_format = email_reader.read_file(filepath)

    assert content == ""
    assert file_format == "binary"


def test_read_text_file(tmp_path: Path, email_reader: EmailReader):
    filepath = tmp_path / "simple.txt"

    filepath.write_text("Hello world")

    content, file_format = email_reader.read_file(filepath)

    assert content == "Hello world"
    assert file_format == "text"


def test_read_valid_json(tmp_path: Path,email_reader: EmailReader):
    filepath = tmp_path / "data.json"

    json_content = """
    {
        "key": "value",
        "number": 123
    }
    """

    filepath.write_text(json_content)

    content, file_format = email_reader.read_file(filepath)

    assert content == json_content
    assert file_format == "json"


def test_read_invalid_json(tmp_path: Path,email_reader: EmailReader):
    filepath = tmp_path / "broken.json"

    filepath.write_text('{"key": "value", "number": }')

    with pytest.raises(FileDecodingError, match="Повреждённый JSON-файл"):
        email_reader.read_file(filepath)


def test_read_file_without_extension(tmp_path: Path, email_reader: EmailReader):
    filepath = tmp_path / "mail"

    filepath.write_text("content without extension")

    content, file_format = email_reader.read_file(filepath)

    assert content == "content without extension"
    assert file_format == "text"


def test_read_cp1251_file(tmp_path: Path, email_reader: EmailReader):
    filepath = tmp_path / "cp1251.txt"

    text = "Привет мир"

    filepath.write_bytes(text.encode("cp1251"))

    content, file_format = email_reader.read_file(filepath)

    assert content == text
    assert file_format == "text"


def test_read_large_file(tmp_path: Path,email_reader: EmailReader):
    filepath = tmp_path / "large.txt"

    filepath.write_bytes(b"a" * (email_reader.MAX_FILE_SIZE + 10))

    with pytest.raises(FileTooLargeError, match="превышает макс. размер"):
        email_reader.read_file(filepath)


def test_read_missing_file(email_reader: EmailReader):
    with pytest.raises(FileNotFoundError, match="Путь filepath не существует"):
        email_reader.read_file(Path("missing.txt"))

def test_read_undecodable_file(tmp_path, email_reader):
    filepath = tmp_path / "broken.txt"

    filepath.write_bytes(b"\xff\xfe\x00\x00")

    content, file_format = email_reader.read_file(filepath)

    assert content == ""
    assert file_format == "binary"