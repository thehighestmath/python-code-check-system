#!/bin/bash

# Скрипт для настройки Nginx на продакшене
# Запустите с правами root: sudo bash setup-nginx.sh

set -e

echo "🚀 Настройка Nginx для Python Code Check System..."

# Проверяем, что скрипт запущен с правами root
if [ "$EUID" -ne 0 ]; then
    echo "❌ Запустите скрипт с правами root: sudo bash setup-nginx.sh"
    exit 1
fi

# Устанавливаем Nginx если не установлен
if ! command -v nginx &> /dev/null; then
    echo "📦 Устанавливаем Nginx..."
    apt update
    apt install -y nginx
fi

# Создаем директорию для логов
mkdir -p /var/log/nginx

# Копируем конфигурацию
echo "📝 Копируем конфигурацию Nginx..."
cp nginx.conf /etc/nginx/sites-available/python-code-check-system

# Создаем симлинк для активации сайта
echo "🔗 Активируем сайт..."
ln -sf /etc/nginx/sites-available/python-code-check-system /etc/nginx/sites-enabled/

# Удаляем дефолтный сайт если он существует
if [ -f /etc/nginx/sites-enabled/default ]; then
    echo "🗑️ Удаляем дефолтный сайт..."
    rm -f /etc/nginx/sites-enabled/default
fi

# Проверяем конфигурацию Nginx
echo "🔍 Проверяем конфигурацию Nginx..."
nginx -t

if [ $? -eq 0 ]; then
    echo "✅ Конфигурация Nginx корректна!"
    
    # Перезапускаем Nginx
    echo "🔄 Перезапускаем Nginx..."
    systemctl restart nginx
    systemctl enable nginx
    
    echo "🎉 Nginx успешно настроен!"
    echo "📋 Проверьте статус: systemctl status nginx"
    echo "🌐 Сайт должен быть доступен по адресу: http://158.160.28.235:8000"
else
    echo "❌ Ошибка в конфигурации Nginx!"
    exit 1
fi

# Показываем статус
echo ""
echo "📊 Статус сервисов:"
echo "Nginx: $(systemctl is-active nginx)"
echo "Docker: $(systemctl is-active docker)"

echo ""
echo "🔧 Полезные команды:"
echo "  Просмотр логов Nginx: tail -f /var/log/nginx/python-code-check-system.error.log"
echo "  Перезапуск Nginx: systemctl restart nginx"
echo "  Проверка конфигурации: nginx -t"
echo "  Статус Nginx: systemctl status nginx"
