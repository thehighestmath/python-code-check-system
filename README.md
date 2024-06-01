# python-code-check-system

Вам нужен докер для разработки
- windows: https://docs.docker.com/desktop/install/windows-install/
- linux: https://docs.docker.com/engine/install/ubuntu/

> [!WARNING]
> В связи с событиями 30.05.2024 образы с hub.docker.com с российских IP адресов скачать нельзя
> 
> Образы, необходимые для проекта, тут https://disk.yandex.ru/d/goJyB9dny51Lsg

Нужно скачать следующие:
- redis-7.0.15-alpine3.20.tar
- postgres-16.3-alpine3.20.tar
- python-3.12.3-slim.tar

Далее выполнить следующие команды в терминале в папке, куда вы скачали образы:
```console
docker load -i redis-7.0.15-alpine3.20.tar
docker load -i postgres-16.3-alpine3.20.tar
docker load -i python-3.12.3-slim.tar
```

> [!NOTE]
> Вы должны увидеть примерно следующий вывод
```console
➜  docker-images docker load -i redis-7.0.15-alpine3.20.tar
Loaded image: redis:7.0.15-alpine3.20
➜  docker-images docker load -i postgres-16.3-alpine3.20.tar
Loaded image: postgres:16.3-alpine3.20
➜  docker-images docker load -i python-3.12.3-slim.tar
Loaded image: python:3.12.3-slim
```

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
