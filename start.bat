@echo off
:: Проверка, установлен ли Python
python --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo Python не найден. Начинаю установку...
    
    :: Скачивание Python
    set URL=https://www.python.org/ftp/python/3.11.4/python-3.11.4-amd64.exe
    set TEMP_INSTALLER=%TEMP%\python_installer.exe
    powershell -Command "(New-Object Net.WebClient).DownloadFile('%URL%', '%TEMP_INSTALLER%')"

    :: Установка Python
    echo Установка Python...
    start /wait %TEMP_INSTALLER% /quiet InstallAllUsers=1 PrependPath=1
    echo Python установлен.
)

:: Проверка версии Python
python --version

:: Создание виртуального окружения
echo Создаю виртуальное окружение...
python -m venv venv

:: Активация виртуального окружения
call venv\Scripts\activate.bat

:: Установка зависимостей из requirements.txt
echo Установка зависимостей из requirements.txt...
pip install -r requirements.txt

:: Создание .env файла, если его нет
if not exist .env (
    echo .env файл не найден. Создаю новый...

    :: Запрос переменных окружения
    set /p DB_HOST="Введите хост базы данных: "
    set /p DB_USER="Введите имя пользователя базы данных: "
    set /p DB_PA
