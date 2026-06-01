import shutil
import logging
from pathlib import Path
from typing import List

from src.models import ClassificationResult, Category
from src.reader import EmailReader
from src.parser import EmailParser
from src.classifier import RuleBasedClassifier

logger = logging.getLogger("mail_processor")


class MailProcessor:
    def __init__(
        self,
        inbox_dir: Path,
        output_dir: Path,
        reader: EmailReader = None,
        parser: EmailParser = None,
        classifier: RuleBasedClassifier = None,
    ):
        self.inbox_dir = Path(inbox_dir)
        self.output_dir = Path(output_dir)
        self.reader = reader or EmailReader()
        self.parser = parser or EmailParser()
        self.classifier = classifier or RuleBasedClassifier()

    def _ensure_directories(self) -> None:
        """Создает выходные папки для каждой категории."""
        self.output_dir.mkdir(parents=True, exist_ok=True)
        for category in Category:
            (self.output_dir / category.value).mkdir(parents=True, exist_ok=True)

    def process_one(self, filepath: Path) -> ClassificationResult:
        """Обрабатывает один файл и копирует его в соответствующую папку."""
        # TODO: Участник 1 должен завершить логику обработки одного письма:
        # 1. Прочитать файл через reader
        # 2. Распарсить через parser
        # 3. Классифицировать через classifier
        # 4. Скопировать оригинал файла в processed/{category}/
        # 5. Записать результат в лог и вернуть ClassificationResult
        raise NotImplementedError("Метод process_one еще не реализован")

    def process_all(self) -> List[ClassificationResult]:
        """Обнаруживает все файлы в inbox и обрабатывает их."""
        logger.info(f"Начало обработки писем из {self.inbox_dir}")
        self._ensure_directories()

        # TODO: Получить список файлов через discover_files,
        # вызвать process_one для каждого и собрать список результатов.
        files = self.reader.discover_files(self.inbox_dir)
        results = []
        for file in files:
            try:
                res = self.process_one(file)
                results.append(res)
            except Exception as e:
                logger.error(f"Не удалось обработать файл {file}: {e}")

        logger.info(f"Обработка завершена. Успешно обработано: {len(results)}/{len(files)}")
        return results
