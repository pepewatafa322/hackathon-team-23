import pytest
from src.models import Email, Category
from src.classifier import RuleBasedClassifier


def test_classify_spam(classifier):
    """Тестирует классификацию спама."""
    email = Email(
        filename="mail.txt",
        subject="Срочно!",
        sender="scam@prize.com",
        recipient="user@company.ru",
        date="2026-06-01",
        body="Вы выиграли миллион рублей в нашем розыгрыше! Подтвердите личность.",
        raw_content="...",
        file_format="text",
    )
    # TODO: После реализации классификатора раскомментировать
    # res = classifier.classify(email)
    # assert res.category == Category.SPAM
    pass


def test_classify_monitoring(classifier):
    """Тестирует классификацию сообщений мониторинга."""
    email = Email(
        filename="mail.txt",
        subject="[CRITICAL] Server healthcheck failed",
        sender="monitoring@company.ru",
        recipient="admin@company.ru",
        date="2026-06-01",
        body="CPU usage is high",
        raw_content="...",
        file_format="text",
    )
    pass


def test_classify_unclassified(classifier):
    """Тестирует попадание писем в категорию UNCLASSIFIED."""
    email = Email(
        filename="mail.txt",
        subject="Привет",
        sender="friend@company.ru",
        recipient="user@company.ru",
        date="2026-06-01",
        body="Привет! Как дела?",
        raw_content="...",
        file_format="text",
    )
    # TODO: Должно возвращать UNCLASSIFIED, так как ключевые слова не совпадают
    # res = classifier.classify(email)
    # assert res.category == Category.UNCLASSIFIED
    pass
