from src.models import Email, Category


class ClassificationRule:
    def __init__(self, category, body_keywords=None, subject_keywords=None, sender_keywords=None, priority=0):
        self.category = category
        self.body_keywords = body_keywords if body_keywords is not None else []
        self.subject_keywords = subject_keywords if subject_keywords is not None else []
        self.sender_keywords = sender_keywords if sender_keywords is not None else []
        self.priority = priority

    def matches(self, email) -> bool:
        body = email.body.lower()
        subject = email.subject.lower()
        sender = email.sender.lower()
        sender_email = email.sender_email.lower()
        sender_name = email.sender_name.lower()

        for word in self.sender_keywords:
            if word in sender or word in sender_email or word in sender_name:
                return True

        for word in self.subject_keywords:
            if word in subject:
                return True

        for word in self.body_keywords:
            if word in body:
                return True

        return False


RULES = [
    ClassificationRule(Category.SPAM, body_keywords=["розыгрыш", "выигр", "банковская карта", "totally-not-spam", "prize", "подтвердите личность", "верификация", "выиграли", "денежный приз", "нажмите здесь", "бесплатно"], subject_keywords=["поздравляем", "розыгрыш", "prize", "выигрыш"], sender_keywords=["promo", "scam", "spam", "prize"], priority=100),
    ClassificationRule(Category.MONITORING, body_keywords=["автоматическое уведомление", "[critical]", "[warning]", "[info]", "cpu usage", "disk usage", "healthcheck", "uptime", "zabbix", "nagios", "prometheus", "alert"], subject_keywords=["автоматическое уведомление", "critical", "warning", "info", "alert"], sender_keywords=["monitoring", "zabbix", "alert", "noreply"], priority=90),
    ClassificationRule(Category.INCIDENT, body_keywords=["критичный инцидент", "массовый сбой", "ошибка 500", "работа остановлена", "не работает у всего", "503", "401", "авария", "упал сервер", "база данных недоступна", "отказ сервиса"], subject_keywords=["инцидент", "сбой", "ошибка 500", "критично", "incident", "crash"], priority=80),
    ClassificationRule(Category.HARDWARE, body_keywords=["гарнитура", "принтер", "сканер", "мышь", "ноутбук", "клавиатура", "монитор", "кабель", "наушники", "компьютер", "жесткий диск", "usb"], subject_keywords=["принтер", "мышь", "клавиатура", "ноутбук", "гарнитура", "монитор", "оборудование"], priority=60),
    ClassificationRule(Category.ACCESS, body_keywords=["выдать доступ", "права на", "учётная запись", "подключить", "рабочее место", "восстановить доступ", "пароль", "логин", "аккаунт", "создать учетную", "vpn", "роль", "права доступа"], subject_keywords=["доступ", "права", "пароль", "учетная запись", "vpn", "access"], priority=50),
    ClassificationRule(Category.DOCUMENTS, body_keywords=["счёт", "акт выполненных", "закрывающие документы", "договор", "оплата по", "реквизиты", "акт", "счет", "накладная", "бухгалтерия", "инвойс", "invoice"], subject_keywords=["счет", "акт", "договор", "документы", "invoice"], priority=45),
    ClassificationRule(Category.HR, body_keywords=["отпуск", "больничный", "bolnichnyy", "netrudosposobnost", "график работы", "увольнение", "прием на работу", "резюме", "кадры", "оформление", "заявление на"], subject_keywords=["отпуск", "больничный", "bolnichnyy", "график", "кадры"], priority=40),
    ClassificationRule(Category.REQUEST, body_keywords=["не открывает", "зависает", "переустановка", "установка", "после обновления", "ошибка при старте", "настройка", "помогите", "не работает программа", "браузер", "excel", "outlook", "zoom"], subject_keywords=["не работает", "ошибка", "проблема", "помощь", "запрос"], priority=30),
    ClassificationRule(Category.INTERNAL, body_keywords=["согласование", "созвон", "дайджест", "обсудить", "приглашение на демо", "встреча", "коллеги", "планерка", "совещание", "демо", "новости"], subject_keywords=["совещание", "встреча", "дайджест", "демо", "internal", "обсуждение"], priority=20),
]
