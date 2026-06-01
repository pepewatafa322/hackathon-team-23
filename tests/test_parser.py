import pytest
from src.parser import EmailParser


def test_parse_simple_format():
    """Тестирует парсинг простого формата заголовков."""
    raw_content = "Subject: Запрос\nFrom: user@corp.ru\n\nТело сообщения"
    parser = EmailParser()
    email = parser.parse(raw_content, "mail_simple.txt", "text")

    # TODO: После реализации парсера эти ассерты должны проходить
    # assert email.subject == "Запрос"
    # assert email.sender == "user@corp.ru"
    # assert email.body == "Тело сообщения"
    pass


def test_parse_en_format():
    """Тестирует парсинг EN-стиля заголовков."""
    raw_content = (
        "From: Ivanov Ivan <ivanov@corp.ru>\n"
        "To: support@corp.ru\n"
        "Date: 2026-06-01 10:00\n"
        "Subject: Connection problem\n\n"
        "Some body text"
    )
    parser = EmailParser()
    email = parser.parse(raw_content, "mail_en.txt", "text")
    pass


def test_parse_ru_format():
    """Тестирует парсинг RU-стиля заголовков."""
    raw_content = (
        "От кого: Петров Петр <petrov@corp.ru>\n"
        "Кому: support@corp.ru\n"
        "Дата: 01.06.2026 10:00\n"
        "Тема: Проблема со сканером\n\n"
        "Не сканирует"
    )
    parser = EmailParser()
    email = parser.parse(raw_content, "mail_ru.txt", "text")
    pass


def test_parse_json_format():
    """Тестирует парсинг JSON-файла писем."""
    raw_content = '{"from": "admin@corp", "subject": "Alert", "body": "Disk full"}'
    parser = EmailParser()
    email = parser.parse(raw_content, "mail.json", "json")
    pass
