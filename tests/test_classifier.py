import pytest
from src.models import Category


def test_classify_spam_by_body(sample_email, classifier):
    sample_email.body = "Вы выиграли денежный приз бесплатно"

    result = classifier.classify(sample_email)

    assert result.category == Category.SPAM
    assert result.confidence == 1.0
    assert result.reason == "rule matching: spam"


def test_classify_spam_by_subject(sample_email, classifier):
    sample_email.subject = "Поздравляем с выигрышем"

    result = classifier.classify(sample_email)

    assert result.category == Category.SPAM


def test_classify_spam_by_sender(sample_email, classifier):
    sample_email.sender_email = "promo@spam-site.com"

    result = classifier.classify(sample_email)

    assert result.category == Category.SPAM


def test_classify_monitoring(sample_email, classifier):
    sample_email.body = "Automatic alert: cpu usage is too high"

    result = classifier.classify(sample_email)

    assert result.category == Category.MONITORING


def test_classify_incident(sample_email, classifier):
    sample_email.body = "Критичный инцидент. База данных недоступна"

    result = classifier.classify(sample_email)

    assert result.category == Category.INCIDENT


def test_classify_hardware(sample_email, classifier):
    sample_email.body = "Не работает принтер на третьем этаже"

    result = classifier.classify(sample_email)

    assert result.category == Category.HARDWARE


def test_classify_access(sample_email, classifier):
    sample_email.body = "Прошу выдать доступ к VPN"

    result = classifier.classify(sample_email)

    assert result.category == Category.ACCESS


def test_classify_documents(sample_email, classifier):
    sample_email.body = "Во вложении счёт и закрывающие документы"

    result = classifier.classify(sample_email)

    assert result.category == Category.DOCUMENTS


def test_classify_hr(sample_email, classifier):
    sample_email.body = "Прошу согласовать отпуск на следующей неделе"

    result = classifier.classify(sample_email)

    assert result.category == Category.HR


def test_classify_request(sample_email, classifier):
    sample_email.body = "После обновления не работает программа"

    result = classifier.classify(sample_email)

    assert result.category == Category.REQUEST


def test_classify_internal(sample_email, classifier):
    sample_email.body = "Коллеги, приглашаю на встречу по проекту"

    result = classifier.classify(sample_email)

    assert result.category == Category.INTERNAL


def test_classify_unclassified(sample_email, classifier):
    sample_email.subject = "Привет"
    sample_email.body = "Как дела?"
    sample_email.sender = "user@example.com"
    sample_email.sender_email = "user@example.com"

    result = classifier.classify(sample_email)

    assert result.category == Category.UNCLASSIFIED
    assert result.confidence == 0.0
    assert result.reason == "no rules matched"


def test_priority_spam_over_request(sample_email, classifier):
    sample_email.body = (
        "Вы выиграли денежный приз. "
        "Также нужна помощь с настройкой программы."
    )

    result = classifier.classify(sample_email)

    assert result.category == Category.SPAM


def test_priority_monitoring_over_incident(sample_email, classifier):
    sample_email.body = (
        "Alert: cpu usage 100%. "
        "Критичный инцидент."
    )

    result = classifier.classify(sample_email)

    assert result.category == Category.MONITORING


def test_case_insensitive_matching(sample_email, classifier):
    sample_email.body = "ВЫ ИГРАЛИ ДЕНЕЖНЫЙ ПРИЗ"

    result = classifier.classify(sample_email)

    assert result.category == Category.SPAM