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

| Имя переменной    | Описание               |
|-------------------|------------------------|
| ENGLEX_STUDENT_ID | Идентификатор студента |
| ENGLEX_TOKEN      | Временный bearer токен |

Затем вызвать `main.py` с указанием пути к csv файлу.

```shell
export ENGLEX_STUDENT_ID=349662
export ENGLEX_TOKEN=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdXRoaWQiOjIzMjEzNCwiYXV0aHJvbGVzIjpbInN0dWRlbnQiXSwiZXhw...

python3 main.py englex.csv
```
