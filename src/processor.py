import shutil
from pathlib import Path
from src.logger_config import logger

class EmailCopier:
    def __init__(self, out_root: Path):
        self.out_root = out_root.resolve()
        self.proc_dir = self.out_root / "processed"
        self.proc_dir.mkdir(parents=True, exist_ok=True)
        try:
            from src.models import Category
            for c in Category:
                (self.proc_dir / c.value).mkdir(parents=True, exist_ok=True)
        except Exception:
            pass
        (self.proc_dir / "unclassified").mkdir(parents=True, exist_ok=True)

    def copy(self, src: Path, cat: str):
        src = src.resolve()
        target = self.proc_dir / cat
        if not target.is_dir():
            logger.warning("Неизвестная категория '%s' – сохраняем в 'unclassified'", cat)
            target = self.proc_dir / "unclassified"

        try:
            shutil.copy2(src, target / src.name)
            logger.info("Скопировано %s → %s", src.name, target.name)
        except Exception as e:
            logger.error("Ошибка копирования %s в %s: %s", src, target, e)
            raise