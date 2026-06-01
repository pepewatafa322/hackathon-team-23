import pytest
from pathlib import Path
from src.models import Email, Category
from src.classifier import RuleBasedClassifier


@pytest.fixture
def sample_email() -> Email:
    """Возвращает стандартный объект Email для тестирования."""
    return Email(
        filename="mail_test.txt",
        subject="Заявка на доступ к репозиторию",
        sender="ivanov@company.ru",
        recipient="it-support@company.ru",
        date="2026-06-01 10:00",
        body="Прошу выдать доступ к репозиторию проекта TP для нового сотрудника.",
        raw_content="...",
        file_format="text",
    )


@pytest.fixture
def classifier() -> RuleBasedClassifier:
    """Возвращает настроенный объект RuleBasedClassifier для тестирования."""
    return RuleBasedClassifier()


@pytest.fixture
def tmp_inbox(tmp_path: Path) -> Path:
    """Создает временную директорию inbox с тестовыми файлами."""
    inbox = tmp_path / "inbox"
    inbox.mkdir()

    # 1. Обычное текстовое письмо
    (inbox / "mail_0001.txt").write_text(
        "Subject: Test\nFrom: user@test.ru\n\nПривет, это обычное письмо.",
        encoding="utf-8",
    )

    # 2. Пустой файл
    (inbox / "mail_0103.txt").touch()

    # 3. Бинарный файл
    (inbox / "mail_0104.bin").write_bytes(b"\x00\x01\x02\x03\xff")

    # 4. JSON-файл
    (inbox / "mail_0105.json").write_text(
        '{"from": "admin@corp", "subject": "Incident", "body": "Critical crash"}',
        encoding="utf-8",
    )

    # 5. Изображение
    (inbox / "mail_0109.jpeg").write_bytes(b"\xff\xd8\xff\xe0")

    return inbox
