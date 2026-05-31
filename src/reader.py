import json
from pathlib import Path


class FileDecodingError(Exception):
    pass


class EmailReader:
    def discover_files(self, inbox_path: Path):
        try:
            files = [elem for elem in inbox_path.iterdir() if elem.is_file() and elem.name != ".DS_Store"]
            return files

        except FileNotFoundError:
            raise FileNotFoundError(f"Путь inbox_path не существует: {inbox_path}")

        except NotADirectoryError:
            raise NotADirectoryError(f"Путь inbox_path не является папкой: {inbox_path}")

        except PermissionError as e:
            raise PermissionError(f"Ошибка доступа к inbox-папке: {inbox_path}") from e

    def read_file(self, filepath: Path):
        try:
            if not filepath.is_file():
                raise FileNotFoundError(f"Путь filepath не является файлом: {filepath}")

            if filepath.stat().st_size == 0:
                return "", "empty"

            file_extension = filepath.suffix.lower()

            binary_extensions = {".bin", ".jpeg", ".jpg", ".png", ".gif",}

            if file_extension in binary_extensions:
                return "", "binary"

            encodings = ["utf-8", "cp1251", "latin-1"]

            for encoding in encodings:
                try:
                    content = filepath.read_text(encoding=encoding)

                    if file_extension == ".json":
                        try:
                            json.loads(content)
                            return content, "json"

                        except json.JSONDecodeError as e:
                            raise ValueError(f"Повреждённый JSON-файл: {filepath}") from e

                    return content, "text"

                except UnicodeDecodeError:
                    continue

            raise FileDecodingError(f"Не удалось декодировать файл: {filepath}")

        except FileNotFoundError as e:
            raise FileNotFoundError(f"Путь filepath не существует: {filepath}") from e

        except PermissionError as e:
            raise PermissionError(f"Ошибка доступа к файлу: {filepath}") from e

        except OSError as e:
            raise OSError(f"Ошибка чтения файла: {filepath}") from e