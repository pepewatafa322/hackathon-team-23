import pytest
from pathlib import Path
from src.processor import MailProcessor


def test_processor_directory_creation(tmp_inbox, tmp_path):
    """Тестирует создание выходных директорий для категорий."""
    output_dir = tmp_path / "processed"
    processor = MailProcessor(inbox_dir=tmp_inbox, output_dir=output_dir)

    processor._ensure_directories()

    # Должна быть создана папка processed/ и 10 папок категорий внутри нее
    assert output_dir.exists()
    for category_dir in [
        "incident",
        "request",
        "hardware",
        "access",
        "documents",
        "hr",
        "monitoring",
        "internal",
        "spam",
        "unclassified",
    ]:
        assert (output_dir / category_dir).exists()


def test_process_all_pipeline(tmp_inbox, tmp_path):
    """Тестирует полный пайплайн обработки всех писем."""
    output_dir = tmp_path / "processed"
    processor = MailProcessor(inbox_dir=tmp_inbox, output_dir=output_dir)

    # TODO: Раскомментировать после реализации pipeline
    # results = processor.process_all()
    # assert len(results) == 5
    pass
