# funbox

### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/petrimma/funbox.git
```

```
cd funbox
```

Cоздать и активировать виртуальное окружение (для Windows):

```
python -m venv venv
```

```
source venv/Scripts/activate
```

Установить зависимости из файла requirements.txt:

```
pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Скачать и установить Redis (для Windows):

```
https://github.com/MicrosoftArchive/redis/releases/download/win-3.2.100/Redis-x64-3.2.100.msi
```

Запустить проект:

```
python manage.py runserver
```

### Доступны два ресурса:

1. Ресурс загрузки посещений

Запрос:

>POST /visited_links/

```
{
"links": [
"https://ya.ru",
"https://ya.ru?q=123",
"funbox.ru",
"https://stackoverflow.com/questions/11828270/how-to-exit-the-vim-editor"
]
}
```

Ответ:

```
{
"status": "ok"
}
```

2. Ресурс получения статистики

Запрос:

>GET /visited_domains/?from=1545221231&to=1545217638

Ответ:

```
{
"domains": [
"ya.ru",
"funbox.ru",
"stackoverflow.com"
],
"status": "ok"
}
```

Запуск тестов:

```
python manage.py test
```

Для хранения данных используется db №1, для тестирования – db №2.  
С тестовым запросом нужно передавать заголовок Test="True"  

Примечание:   
В конце адресов использовала **/** в соответствии с соглашением о наименовании адресов Django.

### Технологии:

- Python 3.9.6
- Django 3.2.7
- Django REST framework 3.12.4
- Redis 3.2.100
- Unittest

