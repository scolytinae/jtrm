# Jinja Template Report Machine (JTRM)

Все хотят отчеты в каком-нибудь `*.docx`/`*.odt`. Возьмем шаблон в каком-нибудь 
`*.md`. Прогоним это через `Jinja2`. После этого засунем получившийся файл в `pandoc`.

После этого попробуем запихнуть это все в сервис. Заодно попробуем в `REST API`.

## План
1. Скрипт генерации всего локально
2. Простейший сервис на `FastApi` для мгновенной печати отчета
3. Добавим возможность сохранения временных данных, для возможности накопить что-либо. Затем 
   сгенерировать отчет по всем накопленным данным.
4. Может быть добавим хранилище шаблонов.

## Что можно будет попробовать
1. `uv` замена для всяких `pipenv`
2. `FastAPI`
3. ``