import argparse
from pathlib import Path

from src.logger_config import setup_logger
from src.processor import MailProcessor
from src.report import ReportGenerator


def main():
    parser = argparse.ArgumentParser(
        description="Автоматизированная система обработки писем"
    )
    parser.add_argument(
        "--inbox",
        type=str,
        default="inbox",
        help="Путь к директории с входящими письмами",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="processed",
        help="Путь к директории для сохранения обработанных писем",
    )
    parser.add_argument(
        "--report",
        type=str,
        default="logs/report.txt",
        help="Путь к файлу итогового отчета",
    )
    args = parser.parse_args()

    # Инициализация логирования
    logger = setup_logger()
    logger.info("Запуск системы обработки писем")

    inbox_path = Path(args.inbox)
    output_path = Path(args.output)
    report_path = Path(args.report)

    # Инициализация процессора
    processor = MailProcessor(inbox_dir=inbox_path, output_dir=output_path)

    # Запуск пайплайна
    results = processor.process_all()

    # Генерация отчета
    report_gen = ReportGenerator()
    stats = report_gen.generate_stats(results)
    formatted_report = report_gen.format_report(stats)

    # Вывод отчета
    print(formatted_report)

    # Сохранение отчета
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_gen.save_report(stats, report_path)
    logger.info(f"Отчет сохранен в {report_path}")


if __name__ == "__main__":
    main()
