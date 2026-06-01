from pathlib import Path
from typing import List, Dict, Any
from src.models import ClassificationResult, Category


class ReportGenerator:
    def generate_stats(self, results: List[ClassificationResult]) -> Dict[str, Any]:
        """Генерирует статистику по категориям (количество и процент)."""
        # TODO: Участник 3 должен реализовать сбор статистики
        stats = {
            "total": len(results),
            "distribution": {cat: {"count": 0, "percentage": 0.0} for cat in Category},
        }
        return stats

    def format_report(self, stats: Dict[str, Any]) -> str:
        """Форматирует красивый текстовый отчет для вывода на экран."""
        # TODO: Участник 3 должен реализовать красивое форматирование
        return "Текстовый отчет еще не реализован."

    def save_report(self, stats: Dict[str, Any], filepath: Path) -> None:
        """Сохраняет отчет в файл."""
        # TODO: Участник 3 должен реализовать сохранение отчета на диск
        pass
