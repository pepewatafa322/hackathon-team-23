import pytest
from pathlib import Path

from src.report import ReportGenerator
from src.models import Category, ClassificationResult


@pytest.fixture
def report_generator():
    return ReportGenerator()

def test_generate_stats_empty(report_generator):
    stats = report_generator.generate_stats([])

    for cat in Category:
        assert stats.get(cat.value, 0) == 0


def test_generate_stats_single_category(
    report_generator,
    sample_email
):
    results = [
        ClassificationResult(
            email=sample_email,
            category=Category.SPAM,
            confidence=1.0,
            reason="test"
        )
    ]

    stats = report_generator.generate_stats(results)

    assert stats["spam"] == 1


def test_generate_stats_multiple_categories(report_generator, sample_email):
    results = [
        ClassificationResult(
            email=sample_email,
            category=Category.SPAM,
            confidence=1.0,
            reason="test"
        ),
        ClassificationResult(
            email=sample_email,
            category=Category.SPAM,
            confidence=1.0,
            reason="test"
        ),
        ClassificationResult(
            email=sample_email,
            category=Category.HR,
            confidence=1.0,
            reason="test"
        ),
    ]

    stats = report_generator.generate_stats(results)

    assert stats["spam"] == 2
    assert stats["hr"] == 1


def test_format_report_empty(report_generator):
    stats = {
        cat.value: 0
        for cat in Category
    }

    report = report_generator.format_report(stats)

    assert "Всего писем: 0" in report


def test_format_report_with_data(report_generator):
    stats = {
        cat.value: 0
        for cat in Category
    }

    stats["spam"] = 2
    stats["hr"] = 1

    report = report_generator.format_report(stats)

    assert "Всего писем: 3" in report
    assert "Категория Спам: 2" in report
    assert "Категория Кадровые: 1" in report


def test_save_report(tmp_path: Path, report_generator):
    filepath = tmp_path / "report.txt"

    stats = {
        cat.value: 0
        for cat in Category
    }

    stats["spam"] = 5

    report_generator.save_report(
        stats,
        filepath
    )

    assert filepath.exists()

    content = filepath.read_text(
        encoding="utf-8"
    )

    assert "Категория Спам: 5" in content