import pytest
from pathlib import Path
from src.models import Email
from src.classifier import RuleBasedClassifier


@pytest.fixture
def tmp_inbox(tmp_path: Path):
    inbox_path = tmp_path / "inbox"
    inbox_path.mkdir()

    (inbox_path / "mail_test_1.txt").write_text(
        "Subject: Тестирую\n"
        "From: Буквально я sender@example.com\n\n"
        "Ну вроде работает, не?"
    )

    (inbox_path / "mail_test_2.json").write_text(
        """
        {
            "subject": "Тестирую JSON",
            "body": "Это определённо JSON"
        }
        """
    )

    (inbox_path / "mail_spam.txt").write_text(
        "Subject: You won a prize!\n\n"
        "Claim your prize now!"
    )

    return inbox_path


@pytest.fixture
def sample_email():
    return Email(
        filename="sample_email.txt",
        subject="Test Subject",

        sender="test@example.com",
        sender_email="test@example.com",

        recipient="recipient@example.com",
        recipient_email="recipient@example.com",

        date="2001-01-01",

        body="This is the body of a sample email.",

        raw_content="Full raw content",

        file_format="txt"
    )


@pytest.fixture
def classifier():
    return RuleBasedClassifier()