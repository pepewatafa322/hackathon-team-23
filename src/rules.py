from dataclasses import dataclass, field
from typing import List
from src.models import Category, Email


@dataclass
class ClassificationRule:
    category: Category
    body_keywords: List[str] = field(default_factory=list)
    subject_patterns: List[str] = field(default_factory=list)
    sender_patterns: List[str] = field(default_factory=list)
    priority: int = 0

    def matches(self, email: Email) -> bool:
        """
        Проверяет, подходит ли письмо под данное правило.
        Должно проверять ключевые слова в теле, теме и отправителе (без учета регистра).
        """
        # TODO: Участник 3 должен реализовать логику сопоставления
        return False


# Набор стандартных правил классификации согласно task_distribution
RULES = [
    ClassificationRule(
        category=Category.SPAM,
        body_keywords=[
            "розыгрыш",
            "выигр",
            "банковская карта",
            "totally-not-spam",
            "prize",
            "подтвердите личность",
            "верификация аккаунта",
        ],
        priority=100,
    ),
    ClassificationRule(
        category=Category.MONITORING,
        body_keywords=[
            "автоматическое уведомление",
            "[critical]",
            "[warning]",
            "[info]",
            "cpu usage",
            "disk usage",
            "healthcheck",
            "uptime",
        ],
        priority=90,
    ),
    ClassificationRule(
        category=Category.INCIDENT,
        body_keywords=[
            "критичный инцидент",
            "массовый сбой",
            "ошибка 500",
            "работа остановлена",
            "не работает у всего",
            "503",
            "401",
        ],
        priority=80,
    ),
    ClassificationRule(
        category=Category.HARDWARE,
        body_keywords=[
            "гарнитура",
            "принтер",
            "сканер",
            "мышь",
            "ноутбук",
            "клавиатура",
            "монитор",
        ],
        priority=60,
    ),
    ClassificationRule(
        category=Category.ACCESS,
        body_keywords=[
            "выдать доступ",
            "права на",
            "учётная запись",
            "подключить",
            "рабочее место",
            "восстановить доступ",
        ],
        priority=50,
    ),
    ClassificationRule(
        category=Category.DOCUMENTS,
        body_keywords=[
            "счёт",
            "акт выполненных",
            "закрывающие документы",
            "договор",
            "оплата по",
            "реквизиты",
        ],
        priority=45,
    ),
    ClassificationRule(
        category=Category.HR,
        body_keywords=[
            "отпуск",
            "больничный",
            "bolnichnyy",
            "netrudosposobnost",
            "график работы",
            "увольнение",
        ],
        priority=40,
    ),
    ClassificationRule(
        category=Category.REQUEST,
        body_keywords=[
            "не открывает",
            "зависает",
            "переустановка",
            "установка",
            "после обновления",
            "ошибка при старте",
        ],
        priority=30,
    ),
    ClassificationRule(
        category=Category.INTERNAL,
        body_keywords=[
            "согласование",
            "созвон",
            "дайджест",
            "обсудить",
            "приглашение на демо",
        ],
        priority=20,
    ),
]
