from enum import Enum
from dataclasses import dataclass


class Category(Enum):
    INCIDENT = "incident"
    REQUEST = "request"
    HARDWARE = "hardware"
    ACCESS = "access"
    DOCUMENTS = "documents"
    HR = "hr"
    MONITORING = "monitoring"
    INTERNAL = "internal"
    SPAM = "spam"
    UNCLASSIFIED = "unclassified"


@dataclass
class Email:
    filename: str
    subject: str
    sender: str
    recipient: str
    date: str
    body: str
    raw_content: str
    file_format: str  # "text", "json", "binary", "empty", "error"


@dataclass
class ClassificationResult:
    email: Email
    category: Category
    confidence: float
    reason: str
