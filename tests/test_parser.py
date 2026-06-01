import pytest
from pathlib import Path

from src.parser import (
    EmailParser,
    EmailParsingError
)


@pytest.fixture
def email_parser():
    return EmailParser()


def test_parse_simple_email(email_parser: EmailParser):
    content = (
        "Subject: Test subject\n"
        "From: sender@example.com\n\n"
        "Hello world"
    )

    email = email_parser.parse(content, Path("mail.txt"),"text")

    assert email.subject == "Test subject"
    assert email.sender_email == "sender@example.com"
    assert email.body == "Hello world"


def test_parse_english_email(email_parser: EmailParser):
    content = (
        "From: John Snow <john@example.com>\n"
        "To: Mary Jane <jane@example.com>\n"
        "Date: 2041-01-01\n"
        "Subject: Meeting\n\n"
        "See you tomorrow"
    )

    email = email_parser.parse(content,Path("mail.txt"), "text"
    )

    assert email.subject == "Meeting"
    assert email.sender_name == "John Snow"
    assert email.sender_email == "john@example.com"

    assert email.recipient_name == "Mary Jane"
    assert email.recipient_email == "jane@example.com"

    assert email.date == "2041-01-01"

    assert email.body == "See you tomorrow"


def test_parse_russian_email(email_parser: EmailParser):
    content = (
        "От кого: Иван Иванов <ivan@example.com>\n"
        "Кому: Петр Петров <petr@example.com>\n"
        "Дата: 2026-01-01\n"
        "Тема: Отчёт\n\n"
        "Текст письма"
    )

    email = email_parser.parse(
        content,
        Path("mail.txt"),
        "text"
    )

    assert email.subject == "Отчёт"

    assert email.sender_name == "Иван Иванов"
    assert email.sender_email == "ivan@example.com"

    assert email.recipient_name == "Петр Петров"
    assert email.recipient_email == "petr@example.com"

    assert email.body == "Текст письма"


def test_parse_translit_email(email_parser: EmailParser):
    content = (
        "Ot kogo: Ivan Ivanov <ivan@example.com>\n"
        "Komu: Petr Petrov <petr@example.com>\n"
        "Data: 2026-01-01\n"
        "Tema: Otchet\n\n"
        "Tekst pisma"
    )

    email = email_parser.parse(
        content,
        Path("mail.txt"),
        "text"
    )

    assert email.subject == "Otchet"

    assert email.sender_name == "Ivan Ivanov"
    assert email.sender_email == "ivan@example.com"

    assert email.recipient_name == "Petr Petrov"
    assert email.recipient_email == "petr@example.com"

    assert email.body == "Tekst pisma"


def test_parse_valid_json_email(email_parser: EmailParser):
    content = """
    {
        "subject": "JSON Subject",
        "from": "Mikle Jacson <jac@example.com>",
        "to": "Mikle Jacson <mike@example.com>",
        "date": "2006-01-01",
        "body": "JSON Body"
    }
    """

    email = email_parser.parse(
        content,
        Path("mail.json"),
        "json"
    )

    assert email.subject == "JSON Subject"

    assert email.sender_name == "Mikle Jacson"
    assert email.sender_email == "jac@example.com"

    assert email.recipient_name == "Mikle Jacson"
    assert email.recipient_email == "mike@example.com"

    assert email.date == "2006-01-01"

    assert email.body == "JSON Body"


def test_parse_invalid_json_email(email_parser: EmailParser):
    content = """
    {
        "subject": "Broken",
        "body":
    }
    """

    with pytest.raises(EmailParsingError, match="Повреждённый JSON email"):
        email_parser.parse(
            content,
            Path("mail.json"),
            "json"
        )


def test_parse_unknown_text_format(email_parser: EmailParser):
    content = (
        "Random text\n"
        "Without email headers\n\n"
        "Hello"
    )

    email = email_parser.parse(
        content,
        Path("mail.txt"),
        "text"
    )

    assert email.filename == "mail.txt"
    assert email.raw_content == content
    assert email.file_format == "text"


def test_parse_binary_file(email_parser: EmailParser):
    email = email_parser.parse(
        "",
        Path("image.jpg"),
        "binary"
    )

    assert email.filename == "image.jpg"
    assert email.file_format == "binary"


def test_parse_empty_file(email_parser: EmailParser):
    email = email_parser.parse(
        "",
        Path("empty.txt"),
        "empty"
    )

    assert email.filename == "empty.txt"
    assert email.file_format == "empty"


def test_parse_email_without_recipient(email_parser: EmailParser):
    content = (
        "Subject: Test\n"
        "From: sender@example.com\n\n"
        "Body"
    )

    email = email_parser.parse(
        content,
        Path("mail.txt"),
        "text"
    )

    assert email.subject == "Test"
    assert email.sender_email == "sender@example.com"
    assert email.recipient_email == ""
    assert email.body == "Body"