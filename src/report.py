from __future__ import annotations

from collections import Counter
from html import escape
from pathlib import Path
import re
from typing import Iterable, Any, Dict, List

_CATEGORY_LABELS = {
    "incident": "Инциденты",
    "request": "Запросы",
    "hardware": "Оборудование",
    "access": "Доступы",
    "documents": "Документы",
    "hr": "Кадровые",
    "monitoring": "Мониторинг",
    "internal": "Внутренние",
    "spam": "Спам",
    "unclassified": "Не распознано",
}


def _label(category: str) -> str:
    return _CATEGORY_LABELS.get(category, category)


class ReportGenerator:
    def __init__(self):
        self._last_results: List[Any] = []

    def generate_stats(self, results: Iterable[Any]) -> Dict[str, int]:
        self._last_results = list(results)

        categories = []
        for res in self._last_results:
            cat = getattr(res, "category", None)
            if cat is not None:
                val = getattr(cat, "value", str(cat))
                categories.append(val)
            else:
                categories.append("unclassified")

        return dict(Counter(categories))

    def format_report(self, stats: Dict[str, int]) -> str:
        normalized = self._normalize(stats)
        total = sum(normalized.values())
        unclass = normalized.get("unclassified", 0)

        lines = [
            "Отчет о работе системы",
            f"Всего писем: {total}",
            f"Распознано уверенно: {total - unclass}",
            f"В категории 'Не распознано': {unclass}",
            "",
        ]

        for cat, cnt in sorted(normalized.items(), key=lambda x: x[1], reverse=True):
            pct = round(cnt / total * 100, 2) if total else 0
            lines.append(f"Категория {_label(cat)}: {cnt} ({pct}%)")

        return "\n".join(lines)

    def save_report(self, stats: Dict[str, int], filepath: str | Path) -> None:
        out = Path(filepath)
        out.parent.mkdir(parents=True, exist_ok=True)

        text = self.format_report(stats)
        html = self._render_html(stats)

        html_path = out if out.suffix == ".html" else out.with_suffix(".html")
        html_path.write_text(html, encoding="utf-8")

        txt_path = out.with_suffix(".txt") if out.suffix == ".html" else out
        txt_path.write_text(f"{text}\n\nHTML-дашборд: {html_path}\n", encoding="utf-8")

    def _normalize(self, stats: Dict[str, Any]) -> Dict[str, int]:
        normalized = {}
        for k, v in stats.items():
            try:
                normalized[k] = max(int(v), 0)
            except (ValueError, TypeError):
                normalized[k] = 0
        return normalized

    def _render_html(self, stats: Dict[str, int]) -> str:
        n = self._normalize(stats)
        total = sum(n.values())
        unclass = n.get("unclassified", 0)
        sorted_cats = sorted(n.items(), key=lambda x: x[1], reverse=True)
        max_val = sorted_cats[0][1] if sorted_cats else 1
        analytics = self._build_analytics()
        bars = "\n".join(
            f'<div class="bar-row">'
            f'<div class="bar-label">{escape(_label(c))}</div>'
            f'<div class="bar-track"><div class="bar-fill" data-width="{round(v / max_val * 100) if max_val else 0}"></div></div>'
            f'<div class="bar-val">{v} <span>({round(v / total * 100, 1) if total else 0}%)</span></div>'
            f"</div>"
            for c, v in sorted_cats
        )

        active_cats = [c for c, v in n.items() if v > 0]
        top_cat_name = max(active_cats, key=lambda c: n[c], default="n/a")
        top = escape(_label(top_cat_name))

        spam_share = round((n.get("spam", 0) / total) * 100, 1) if total else 0

        return _TEMPLATE.format(
            total=total,
            confident=total - unclass,
            unclassified=unclass,
            recognized_percent=round((total - unclass) / total * 100, 1) if total else 0,
            top_category=top,
            categories_with_mail=len(active_cats),
            spam_share=spam_share,
            incident_count=n.get("incident", 0),
            peak_hour=analytics["peak_hour"],
            bars=bars,
            hour_bars=analytics["hour_bars"],
            top_sender_rows=analytics["top_sender_rows"],
        )

    def _build_analytics(self) -> Dict[str, Any]:
        by_hour = [0] * 24
        sender_counter = Counter()

        for result in self._last_results:
            email = getattr(result, "email", None)
            if email is None:
                continue

            hour = self._extract_hour(getattr(email, "date", ""))
            if hour is not None:
                by_hour[hour] += 1

            sender = (
                    (getattr(email, "sender_email", "") or "").strip()
                    or (getattr(email, "sender", "") or "").strip()
                    or (getattr(email, "sender_name", "") or "").strip()
            )
            if sender:
                sender_counter[sender] += 1

        max_hour_value = max(by_hour) if any(by_hour) else 1
        peak_hour_idx = by_hour.index(max(by_hour)) if any(by_hour) else None
        peak_hour = f"{peak_hour_idx:02d}:00" if peak_hour_idx is not None else "n/a"


        hour_bars = "\n".join(
            '<div class="hour-cell">'
            f'<div class="hour-col" data-height="{round((value / max_hour_value) * 100) if max_hour_value else 0}"></div>'
            f'<div class="hour-num">{value}</div>'
            f'<div class="hour-lbl">{hour:02d}</div>'
            "</div>"
            for hour, value in enumerate(by_hour)
        )

        top_sender_rows = "\n".join(
            "<tr>"
            f"<td class='mono'>{idx}</td>"
            f"<td>{escape(sender)}</td>"
            f"<td class='mono'>{count}</td>"
            "</tr>"
            for idx, (sender, count) in enumerate(sender_counter.most_common(5), start=1)
        )
        if not top_sender_rows:
            top_sender_rows = "<tr><td class='mono'>-</td><td>Нет данных</td><td class='mono'>0</td></tr>"

        return {
            "peak_hour": peak_hour,
            "hour_bars": hour_bars,
            "top_sender_rows": top_sender_rows,
        }

    def _extract_hour(self, date_value: Any) -> int | None:
        if not date_value:
            return None

        match = re.search(r"\b([01]?\d|2[0-3]):[0-5]\d\b", str(date_value))
        if match is None:
            return None

        try:
            return int(match.group(1))
        except ValueError:
            return None


# HTML
_TEMPLATE = """<!doctype html>
<html lang="ru">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>Дашборд обработки писем</title>
  <style>
    :root {{
      --ink: #1a1a17;
      --paper: #f4f1ea;
      --card: #fffdf8;
      --line: #d9d3c5;
      --accent: #b5432c;
      --accent2: #2c5b4f;
      --warn: #c8861a;
      --dim: #8a857a;
    }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      background: var(--paper);
      color: var(--ink);
      font-family: "Segoe UI", Tahoma, sans-serif;
      line-height: 1.5;
      background-image: radial-gradient(circle at 1px 1px, rgba(0,0,0,.04) 1px, transparent 0);
      background-size: 22px 22px;
      padding: 36px 18px;
    }}
    .wrap {{ max-width: 1100px; margin: 0 auto; }}
    header {{
      border-bottom: 3px solid var(--ink);
      padding-bottom: 14px;
      margin-bottom: 26px;
      display: flex;
      justify-content: space-between;
      align-items: end;
      gap: 10px;
      flex-wrap: wrap;
    }}
    h1 {{ font-size: clamp(28px, 4vw, 46px); line-height: 1; }}
    h2 {{ font-size: 21px; margin: 30px 0 14px; }}
    h3 {{ font-size: 18px; margin: 0 0 10px; }}
    .kpis {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 12px; }}
    .kpi {{ background: var(--card); border: 1px solid var(--line); border-radius: 10px; padding: 14px 16px; }}
    .kpi .num {{ font-size: 36px; font-weight: 800; line-height: 1.1; }}
    .kpi .lbl {{ color: #6b6658; font-size: 13px; margin-top: 4px; }}
    .grid2 {{ display: grid; grid-template-columns: 1fr 1fr; gap: 24px; align-items: start; }}
    .grid-main {{ display: grid; grid-template-columns: 2fr 1fr; gap: 24px; align-items: start; margin-top: 20px; }}
    @media (max-width: 860px) {{ .grid2 {{ grid-template-columns: 1fr; }} }}
    @media (max-width: 980px) {{ .grid-main {{ grid-template-columns: 1fr; }} }}
    .card {{ background: var(--card); border: 1px solid var(--line); border-radius: 10px; padding: 14px; }}
    
    /* Стили для горизонтальных баров */
    .bar-row {{ display: grid; grid-template-columns: 170px 1fr 90px; gap: 12px; align-items: center; margin-bottom: 8px; }}
    .bar-label {{ text-align: right; color: #3a372f; font-size: 14px; }}
    .bar-track {{ background: #e6e0d2; border-radius: 6px; height: 20px; overflow: hidden; }}
    .bar-fill {{ 
      height: 100%; 
      width: 0; /* Начинаем с 0 для JS-анимации */
      background: linear-gradient(90deg, var(--accent), #d4663f); 
      transition: width 1s cubic-bezier(0.22, 1, 0.36, 1);
    }}
    .bar-val {{ font-size: 13px; }}
    .bar-val span {{ color: var(--dim); }}
    
    table {{ width: 100%; border-collapse: collapse; background: var(--card); border: 1px solid var(--line); border-radius: 10px; overflow: hidden; }}
    th {{ background: var(--ink); color: var(--paper); text-align: left; padding: 9px 10px; font-size: 12px; text-transform: uppercase; letter-spacing: .04em; }}
    td {{ padding: 8px 10px; border-top: 1px solid var(--line); font-size: 13px; }}
    .mono {{ font-family: ui-monospace, SFMono-Regular, Menlo, monospace; }}
    
    /* Стили для гистограммы по часам */
    .hours-wrap {{
      display: grid;
      grid-template-columns: repeat(24, minmax(18px, 1fr));
      gap: 8px;
      align-items: end;
      height: 210px;
      border: 1px solid var(--line);
      border-radius: 10px;
      padding: 8px 10px;
      background: #f8f5ed;
    }}
    .hour-cell {{ display: flex; flex-direction: column; align-items: center; justify-content: end; min-width: 0; height: 100%; }}
    .hour-col {{ 
      width: 100%; 
      max-width: 18px; 
      height: 0; /* Начинаем с 0 для JS-анимации */
      min-height: 0; 
      border-radius: 4px 4px 2px 2px; 
      background: linear-gradient(180deg, #3f89ef, #2e6fce); 
      transition: height 1s cubic-bezier(0.22, 1, 0.36, 1);
    }}
    .hour-num {{ font-size: 10px; color: #5e6675; margin-top: 4px; line-height: 1; }}
    .hour-lbl {{ font-size: 10px; color: #8a857a; margin-top: 3px; line-height: 1; }}
  </style>
</head>
<body>
  <div class="wrap">
    <header>
      <h1>Дашборд обработки почты</h1>
    </header>

    <section class="kpis">
      <div class="kpi"><div class="num">{total}</div><div class="lbl">Всего обработано</div></div>
      <div class="kpi"><div class="num">{spam_share}%</div><div class="lbl">Доля спама</div></div>
      <div class="kpi"><div class="num">{incident_count}</div><div class="lbl">Инциденты</div></div>
      <div class="kpi"><div class="num">{peak_hour}</div><div class="lbl">Пик активности</div></div>
    </section>

    <section class="grid-main">
      <div class="card">
        <h3>Временная диаграмма наплыва писем (по часам)</h3>
        <div class="hours-wrap">{hour_bars}</div>
      </div>
      <div class="card">
        <h3>Топ-5 активных отправителей</h3>
        <table>
          <thead>
            <tr>
              <th>#</th>
              <th>Отправитель</th>
              <th>Писем</th>
            </tr>
          </thead>
          <tbody>{top_sender_rows}</tbody>
        </table>
      </div>
    </section>

    <section class="grid2">
      <div>
        <h2>Распределение по категориям</h2>
        <div class="card">{bars}</div>
      </div>
      <div>
        <h2>Краткая аналитика</h2>
        <div class="card">
          <p><strong>Лидирующая категория:</strong> {top_category}</p>
          <p><strong>Категорий с письмами:</strong> {categories_with_mail}</p>
          <p><strong>Качество распознавания:</strong> {recognized_percent}%</p>
        </div>
      </div>
    </section>

  </div>

  <script>
    document.addEventListener('DOMContentLoaded', () => {{
      const animate = () => {{
        // Анимация горизонтальных полос (категории)
        document.querySelectorAll('.bar-fill').forEach((bar, index) => {{
          const w = bar.getAttribute('data-width') || 0;
          setTimeout(() => {{
            bar.style.width = w + '%';
          }}, 50 * index);
        }});

        document.querySelectorAll('.hour-col').forEach((col, index) => {{
          const h = col.getAttribute('data-height') || 0;
          setTimeout(() => {{
            col.style.height = h + '%';
          }}, 30 * index);
        }});
      }};
      requestAnimationFrame(() => {{
        setTimeout(animate, 100);
      }});
    }});
  </script>
</body>
</html>
"""
