import argparse
from pathlib import Path

from src.reader import EmailReader
from src.parser import EmailParser
from src.classifier import RuleBasedClassifier
from src.report import ReportGenerator
from src.processor import EmailCopier
from src.logger_config import setup_logger
logger = setup_logger()

parser = argparse.ArgumentParser()
parser.add_argument("--inbox", type=Path, required=True)
parser.add_argument("--output", type=Path, required=True)
args = parser.parse_args()

inbox_path = args.inbox.resolve()
output_path = args.output.resolve()

logger.info("Старт обработки писем: inbox=%s, output=%s", inbox_path, output_path)

copier = EmailCopier(output_path)
reader = EmailReader()
email_parser = EmailParser()
classifier = RuleBasedClassifier()
report_gen = ReportGenerator()

results = []
for file_path in reader.discover_files(inbox_path):
    try:
        raw_content, file_type = reader.read_file(file_path)
        email = email_parser.parse(raw_content, file_path, file_type)
        classification = classifier.classify(email)
        results.append(classification)

        copier.copy(file_path, classification.category.value)
        logger.info("Обработано: %s → %s", file_path.name, classification.category.value)
    except Exception as e:
        logger.error("Ошибка при обработке файла %s: %s", file_path.name, e)
        copier.copy(file_path, "unclassified")

report_path = output_path / "report.txt"
stats = report_gen.generate_stats(results)
report_gen.save_report(stats, str(report_path))
logger.info("Отчет сохранен: %s", report_path)
