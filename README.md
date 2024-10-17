# 🚗 Telegram Car Bot

Этот бот создан для управления автомобилями, ведения учёта расходов, напоминаний о сервисах и многого другого. Он легко запускается с помощью Docker и готов к использованию без специальных знаний.

## 🔧 Функции бота

- Добавление и управление автомобилями
- Создание заметок о расходах
- Напоминания о событиях
- Учёт покупок и их управление
- Удобное меню для взаимодействия
- Учёт проведённых ТО, кастомные шаблоны ТО

## 📋 Как запустить бота шаг за шагом

### Шаг 1: Клонируйте репозиторий
Сначала скачайте код на ваш компьютер. Для этого откройте терминал (или командную строку) и выполните команду:

```bash
git clone https://github.com/Sayrrexe/SF-Car-Bot.git
```

### Шаг 2: Установите Docker
Если у вас ещё нет Docker, скачайте и установите его:

- [Инструкция по установке Docker](https://docs.docker.com/get-docker/)

### Шаг 3: Настройка переменных окружения

Боту нужен токен Telegram и база данных для работы. Создайте файл `.env` в корне проекта с таким содержимым:

```env
TOKEN=ВАШ_ТОКЕН_ОТ_TELEGRAM
```

Как получить токен:
1. Откройте Telegram и найдите [BotFather](https://t.me/BotFather).
2. Введите `/newbot` и следуйте инструкциям.
3. После создания бота вы получите токен.

### Шаг 4: Запуск бота через Docker

После установки Docker и создания файла `.env` можно запускать бота. Всё, что вам нужно сделать:

1. Откройте терминал в папке с проектом.
2. Выполните команду:

```bash
docker-compose up --build
```

Это создаст и запустит контейнер с ботом.

### Шаг 5: Запуск бота вручную (если не хотите использовать Docker)

1. Убедитесь, что у вас установлен Python 3.10 или выше.
2. Создайте файл .env и добавьте туда ваш ТОКЕН как это было показано выше
3. Установите зависимости, выполнив команду:

```bash
pip install -r requirements.txt
```

4. Запустите скрипт бота:

```bash
bash run_bot.sh
```

Теперь ваш бот готов к работе! 🎉

## 🛠 Команды для взаимодействия с ботом

- `/start` — начать взаимодействие с ботом
- `/menu` — открыть главное меню
- `/help` — список всех доступных команд

## 💡 Советы
- Убедитесь, что вы правильно настроили файл `.env`.
