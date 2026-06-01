import pytest
from src.reader import EmailReader
from src.parser import EmailParser


def test_empty_file_edge_case(tmp_inbox):
    """Тестирует чтение и обработку пустого файла (0 байт)."""
    reader = EmailReader()
    filepath = tmp_inbox / "mail_0103.txt"
    content, file_format = reader.read_file(filepath)

    assert content == ""
    assert file_format == "empty"


def test_binary_file_edge_case(tmp_inbox):
    """Тестирует чтение бинарного файла."""
    reader = EmailReader()
    filepath = tmp_inbox / "mail_0104.bin"
    content, file_format = reader.read_file(filepath)

    assert content == ""
    assert file_format == "binary"


def test_corrupted_json_edge_case(tmp_path):
    """Тестирует обработку битого JSON-файла (JSONDecodeError)."""
    bad_json = tmp_path / "mail_bad.json"
    bad_json.write_text('{"from": "admin", "subject": "bad"', encoding="utf-8")

    reader = EmailReader()
    with pytest.raises(ValueError) as excinfo:
        reader.read_file(bad_json)

    assert "Повреждённый JSON-файл" in str(excinfo.value)


def test_image_file_edge_case(tmp_inbox):
    """Тестирует чтение изображения (.jpeg)."""
    reader = EmailReader()
    filepath = tmp_inbox / "mail_0109.jpeg"
    content, file_format = reader.read_file(filepath)

    assert content == ""
    assert file_format == "binary"
