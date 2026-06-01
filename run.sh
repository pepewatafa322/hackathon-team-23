#!/bin/bash
# Скрипт запуска системы обработки корпоративной почты
set -e

echo "=== Система обработки корпоративной почты ==="
echo "Время запуска: $(date '+%Y-%m-%d %H:%M:%S')"
echo ""

# Проверка Python
if ! command -v python3 &> /dev/null; then
    echo "❌ ERROR: Python3 не найден в системе"
    exit 1
fi
echo "✅ Python3: $(python3 --version)"

# Проверка inbox
if [ ! -d "inbox" ]; then
    echo "❌ ERROR: Директория inbox/ не найдена"
    exit 1
fi

MAIL_COUNT=$(find inbox -type f ! -name '.DS_Store' | wc -l)
echo "📨 Найдено писем в inbox: $MAIL_COUNT"
echo ""

# Создание директории логов
mkdir -p logs

# Установка зависимостей
echo "📦 Проверка зависимостей..."
pip3 install -r requirements.txt --quiet 2>/dev/null || true

echo ""
echo "▶ Запуск обработки..."
echo "---"

# Запуск main модуля
python3 -m src.main --inbox inbox --output processed 2>&1 | tee logs/run_output.log
EXIT_CODE=${PIPESTATUS[0]}

echo "---"
echo ""

# Итоги
if [ $EXIT_CODE -eq 0 ]; then
    echo "✅ Обработка завершена успешно"
    echo ""
    echo "📊 Распределение по категориям:"
    if [ -d "processed" ]; then
        for dir in processed/*/; do
            if [ -d "$dir" ]; then
                COUNT=$(find "$dir" -type f | wc -l)
                CATEGORY=$(basename "$dir")
                printf "   📁 %-15s %d писем\n" "$CATEGORY" "$COUNT"
            fi
        done
    fi
else
    echo "❌ Обработка завершена с ошибкой (код: $EXIT_CODE)"
fi

echo ""
echo "📝 Подробный лог: logs/processing.log"
echo "Окончание: $(date '+%Y-%m-%d %H:%M:%S')"
