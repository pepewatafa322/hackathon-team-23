import json
import re
from pathlib import Path
from src.models import Email


class EmailParsingError(Exception):
    pass

class UnknownEmailFormatError(Exception):
    pass


class EmailParser:  
    def _prepare_content(self, content: str):
        content = re.sub(r'\r\n|\r', '\n', content)
        return re.sub(r'\n[ \t]+', ' ', content)
    
    def _parse_contact(self, value: str):
        value = re.sub(r"\s+", " ", value.strip())

        match = re.match(r'^(.*?)\s*<([^<>]+)>$', value)

        if match:
            name = match.group(1).strip('" ')
            email = match.group(2).strip()
            return name, email

        if "@" in value:
            return "", value

        return value, ""

    def _identify_header_format(self, raw_content: str):
        lower_content = raw_content.lower()

        if "от кого:" in lower_content and "тема:" in lower_content:
            return "ru"

        if "ot kogo:" in lower_content and "tema:" in lower_content:
            return "translit"

        if ("from:" in lower_content and "to:" in lower_content and "date:" in lower_content):
            return "en"

        if "subject:" in lower_content and "from:" in lower_content:
            return "simple"

        raise UnknownEmailFormatError("Неизвестный формат email-заголовков")

    def _extract_value(self, content: str, keyword: str):
        pattern = rf"^\s*{re.escape(keyword)}\s*(.*?)\s*$"

        match = re.search(pattern, content, re.IGNORECASE | re.MULTILINE)

        if not match:
            return ""

        return match.group(1).strip()

    def _extract_body(self, content: str):
        lines = content.splitlines()

        for i, line in enumerate(lines):
            if not line.strip():
                return "\n".join(lines[i + 1:]).strip()

        return ""

    def _parse_text_email(self,
        raw_content: str,
        header_format: str,
        filename: Path
    ):
        email = Email(
            filename=filename.name,
            raw_content=raw_content,
            file_format="text"
        )

        try:
            if header_format == "ru":
                email.subject = self._extract_value(raw_content, "Тема:")
                sender = self._extract_value(raw_content, "От кого:")
                recipient = self._extract_value(raw_content, "Кому:")
                email.date = self._extract_value(raw_content, "Дата:")

                sender_name, sender_email = self._parse_contact(sender)
                email.sender, email.sender_name, email.sender_email = sender, sender_name, sender_email

                recipient_name, recipient_email = self._parse_contact(recipient)
                email.recipient, email.recipient_name, email.recipient_email = recipient, recipient_name, recipient_email

            elif header_format == "translit":
                email.subject = self._extract_value(raw_content, "Tema:")
                sender = self._extract_value(raw_content, "Ot kogo:")
                recipient = self._extract_value(raw_content, "Komu:")
                email.date = self._extract_value(raw_content, "Data:")

                sender_name, sender_email = self._parse_contact(sender)
                email.sender, email.sender_name, email.sender_email = sender, sender_name, sender_email

                recipient_name, recipient_email = self._parse_contact(recipient)
                email.recipient, email.recipient_name, email.recipient_email = recipient, recipient_name, recipient_email

            elif header_format == "en":
                email.subject = self._extract_value(raw_content, "Subject:")
                sender = self._extract_value(raw_content, "From:")
                recipient = self._extract_value(raw_content, "To:")
                email.date = self._extract_value(raw_content, "Date:")

                sender_name, sender_email = self._parse_contact(sender)
                email.sender, email.sender_name, email.sender_email = sender, sender_name, sender_email

                recipient_name, recipient_email = self._parse_contact(recipient)
                email.recipient, email.recipient_name, email.recipient_email = recipient, recipient_name, recipient_email

            elif header_format == "simple":
                email.subject = self._extract_value(raw_content, "Subject:")
                sender = self._extract_value(raw_content, "From:")
                sender_name, sender_email = self._parse_contact(sender)
                email.sender, email.sender_name, email.sender_email = sender, sender_name, sender_email

            email.body = self._extract_body(raw_content)

            return email

        except Exception as e:
            raise EmailParsingError(
                f"Ошибка парсинга текстового email: {filename}"
            ) from e

    def _parse_json_email(
        self,
        raw_content: str,
        filename: Path
    ):
        try:
            data = json.loads(raw_content)

            email = Email(
                filename=filename.name,
                raw_content=raw_content,
                file_format="json"
            )

            email.subject=data.get("subject", "")
            sender = data.get("from", "")
            recipient = data.get("to", "")
            email.date = data.get("date", "")

            sender_name, sender_email = self._parse_contact(sender)
            email.sender, email.sender_name, email.sender_email = sender, sender_name, sender_email

            recipient_name, recipient_email = self._parse_contact(recipient)
            email.recipient, email.recipient_name, email.recipient_email = recipient, recipient_name, recipient_email

            email.body = data.get("body", "")

            return email
        
        except json.JSONDecodeError as e:
            raise EmailParsingError(f"Повреждённый JSON email: {filename}") from e

        except Exception as e:
            raise EmailParsingError(f"Ошибка парсинга JSON email: {filename}") from e

    def parse(self,
        raw_content: str,
        filename: Path,
        file_format: str
    ):
        try:
            if file_format == "json":
                return self._parse_json_email(raw_content, filename)

            if file_format == "text":
                prepared_content = self._prepare_content(raw_content)

                header_format = self._identify_header_format(prepared_content)

                return self._parse_text_email(
                    prepared_content,
                    header_format, 
                    filename
                )

            return Email(
                filename=filename.name,
                raw_content=raw_content,
                file_format=file_format
            )

        except UnknownEmailFormatError:
            return Email(
                filename=filename.name,
                raw_content=raw_content,
                file_format=file_format
            )