# IT College — сайт колледжа

Сайт на Django 6 с админкой Jazzmin и тремя языками: ru, en, ky.

## Что нужно заранее

- **Python 3.12 или новее** (на версиях ниже Django 6 не встанет)
- **Git**
- **gettext** — нужен для английской и киргизской версий сайта (`compilemessages`)
  - Linux: `sudo apt install gettext` (Arch: `sudo pacman -S gettext`)
  - macOS: `brew install gettext`
  - Windows: установщик с https://mlocati.github.io/articles/gettext-iconv-windows.html

## Запуск

### Linux / macOS

```bash
git clone <ссылка-на-репозиторий> it-college-2
cd it-college-2

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

cp .env.example .env              # затем впишите свой SECRET_KEY
python manage.py migrate
python manage.py compilemessages -i venv
python manage.py createsuperuser  # логин и пароль для админки
python manage.py runserver
```

### Windows (PowerShell)

```powershell
git clone <ссылка-на-репозиторий> it-college-2
cd it-college-2

python -m venv venv
venv\Scripts\Activate.ps1
pip install -r requirements.txt

copy .env.example .env
python manage.py migrate
python manage.py compilemessages -i venv
python manage.py createsuperuser
python manage.py runserver
```

Если PowerShell не даёт активировать venv, один раз выполните:
`Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`.

Ссылки после запуска:

- Сайт: http://127.0.0.1:8000/
- Админка: http://127.0.0.1:8000/admin/

Сгенерировать `SECRET_KEY`:

```bash
python -c "from django.core.management.utils import get_random_secret_key as k; print(k())"
```

## Важно знать

- **Новый сайт будет пустым.** База `db.sqlite3` и загруженные файлы `media/` не хранятся в git, поэтому весь контент заполняется через админку.
  Чтобы перенести контент с другого компьютера, скопируйте оттуда `db.sqlite3` и папку `media/`.
- **Переводы.** Файлы `*.mo` тоже не хранятся в git. Если английская или киргизская версия показывает русский текст, выполните `python manage.py compilemessages -i venv` и перезапустите сервер.
- **Свои стили и скрипты** лежат в `assets/`. Папка `staticfiles/` создаётся командой `collectstatic` и в git не хранится.
- **`.env`** не попадает в git. Без него сайт не запустится: `SECRET_KEY` будет пустым, а `DEBUG` выключен.
- В режиме `DEBUG=False` Django не отдаёт файлы из `media/` и `static/`. Для боевого сервера нужен nginx (или аналог) и `python manage.py collectstatic`.

## Структура

| Папка | Что внутри |
|---|---|
| `core/` | настройки, корневые URL |
| `main/` | главная, баннеры, преимущества, НПА, паспорт колледжа, этапы приёма |
| `news/` | новости и их галереи |
| `events/` | день открытых дверей |
| `abiturient/` | FAQ, документы для поступления, онлайн-заявки |
| `education/` | специальности, стоимость, бюджет, перевод, лицензии |
| `people/` | директор, выпускники, партнёры, статистика |
| `contacts/` | контакты, отделы, соцсети, обратная связь |
| `templates/` | HTML-шаблоны |
| `assets/` | CSS, JS, картинки |
| `locale/` | переводы en / ky |
