from src.models import Category


class ReportGenerator:
    def generate_stats(self, results):
        stats = {}
        for cat in Category:
            stats[cat.value] = 0
        for res in results:
            stats[res.category.value] = stats[res.category.value] + 1
        return stats

    def format_report(self, stats):
        total = 0
        for val in stats.values():
            total = total + val

        report_text = ""
        report_text = report_text + "Отчет о работе системы\n"
        report_text = report_text + "Всего писем: " + str(total) + "\n"

        for cat in stats:
            count = stats[cat]
            if total > 0:
                percent = (count / total) * 100
            else:
                percent = 0
            report_text = (
                report_text
                + "Категория "
                + str(cat)
                + ": "
                + str(count)
                + " ("
                + str(round(percent, 2))
                + "%)\n"
            )

        return report_text

    def save_report(self, stats, filepath):
        text = self.format_report(stats)
        f = open(filepath, "w", encoding="utf-8")
        f.write(text)
        f.close()
