from typing import List
from src.models import Email, ClassificationResult, Category
from src.rules import ClassificationRule, RULES


class RuleBasedClassifier:
    def __init__(self, rules: List[ClassificationRule] = None):
        # Сортируем правила по приоритету от большего к меньшему
        self.rules = sorted(rules or RULES, key=lambda r: r.priority, reverse=True)

    def classify(self, email: Email) -> ClassificationResult:
        """
        Проходит по правилам и классифицирует письмо.
        Если совпадений нет, возвращает категорию UNCLASSIFIED.
        """
        # TODO: Участник 3 должен реализовать логику классификации по правилам
        return ClassificationResult(
            email=email,
            category=Category.UNCLASSIFIED,
            confidence=0.0,
            reason="Ни одно правило не совпало",
        )
