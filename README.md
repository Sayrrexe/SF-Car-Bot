### Шаг 1 (Добавить)

И перейдите в директорию с проектом 

```bash
cd SF-Car-Bot
```

### Шаг 2 (был 3, добавить)
```env
TOKEN=ВАШ_ТОКЕН_ОТ_TELEGRAM
DB_URL=sqlite://db.sqlite3
DB_HOST=db
DB_PORT=5432
DB_USER=postgres
DB_PASS=postgres
DB_NAME=postgres
```

### Шаг 3: Запуск бота с использованием Docker
Мы предполагаем, что Вы используете дистрибутивы Linux Ubuntu или Red Hat, в других случаях, если у вас ещё нет Docker, скачайте и установите его:

- [Инструкция по установке Docker](https://docs.docker.com/get-docker/) 

Выполните следующие команды в терминале для запуска бота:

```bash
chmod +x start.sh
./start.sh
```

Убедитесь, что докер-сервисы запущены:

```bash
docker service ls
```

### Шаг 4 (был 5, добавить условие, что постгрес установлен и запущен либо же раскомментить конфиг с sqlite)
