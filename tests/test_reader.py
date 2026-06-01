import pytest
from pathlib import Path
from src.reader import EmailReader


def test_discover_files(tmp_inbox):
    """Тестирует обнаружение файлов во входящей директории."""
    reader = EmailReader()
    files = reader.discover_files(tmp_inbox)
    filenames = [f.name for f in files]

    # Должен найти все 5 файлов
    assert len(files) == 5
    assert "mail_0001.txt" in filenames
    assert "mail_0103.txt" in filenames
    assert "mail_0104.bin" in filenames
    assert "mail_0105.json" in filenames
    assert "mail_0109.jpeg" in filenames


def test_read_text_file(tmp_inbox):
    """Тестирует чтение обычного текстового файла."""
    reader = EmailReader()
    filepath = tmp_inbox / "mail_0001.txt"
    content, file_format = reader.read_file(filepath)

    assert file_format == "text"
    assert "Привет, это обычное письмо." in content


def test_read_empty_file(tmp_inbox):
    """Тестирует чтение пустого файла."""
    reader = EmailReader()
    filepath = tmp_inbox / "mail_0103.txt"
    content, file_format = reader.read_file(filepath)

    assert content == ""
    assert file_format == "empty"


def test_read_binary_file(tmp_inbox):
    """Тестирует чтение бинарного файла."""
    reader = EmailReader()
    filepath = tmp_inbox / "mail_0104.bin"
    content, file_format = reader.read_file(filepath)

    assert content == ""
    assert file_format == "binary"
