# python-code-check-system

Вам нужен докер для разработки
- windows: https://docs.docker.com/desktop/install/windows-install/
- linux: https://docs.docker.com/engine/install/ubuntu/
- macos: https://docs.docker.com/desktop/install/mac-install/

> [!IMPORTANT]
> Не забудьте выставить концы строк LF, а не CRLF
> 
> Создайте файл `.env` в корне репозитория и поместите туда содержимое файла `env.example`

Великолепно, теперь можно поднимать приложение одной командой!

Тогда будет докер приложение можно развернуть одной командой:
```console
docker compose up --build
```

Чтобы остановить приложение:
```console
docker compose down
```

Приложение будет доступно по следующему адресу: http://localhost:80/ или http://localhost

Также развернуто тестовое окружение тут http://158.160.28.235/
