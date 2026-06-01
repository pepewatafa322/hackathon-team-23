from src.models import ClassificationResult, Category
from src.rules import RULES


class RuleBasedClassifier:
    def __init__(self):
        self.rules = sorted(RULES, key=lambda r: r.priority, reverse=True)

    def classify(self, email):
        for rule in self.rules:
            if rule.matches(email):
                return ClassificationResult(
                    email=email,
                    category=rule.category,
                    confidence=1.0,
                    reason="rule matching: " + rule.category.value,
                )
        return ClassificationResult(
            email=email,
            category=Category.UNCLASSIFIED,
            confidence=0.0,
            reason="no rules matched",
        )
