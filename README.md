# englex-csv

Скрипт выгружает данные из всех словарей в личном кабинете englex и экспортирует в csv файл.

## Установка зависимостей

```shell
# Создание виртуального окружения.
python3 -m venv venv
source venv/bin/activate

# Установка зависимостей.
pip install -r requirements.txt
```

## Запуск

Необходимо определить переменные окружения:

| Имя переменной       | Описание            |
|----------------------|---------------------|
| ENGLEX_USER_EMAIL    | Email пользователя  |
| ENGLEX_USER_PASSWORD | Пароль пользователя |

Затем вызвать `main.py`, после чего слова будут сохранены в файле `englex.csv`.

Так же можно указать альтернативный путь при запуске скрипта, передав его в аргументах.

```shell
# Экспорт переменных окружения.
export ENGLEX_USER_EMAIL=student@example.com
export ENGLEX_USER_PASSWORD=my_secret_password

# Запуск экспорта.
python3 main.py
# Или...
python3 main.py another/path/to/save/output.csv
```
