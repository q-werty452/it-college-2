from pathlib import Path
import os
from dotenv import load_dotenv
from django.utils.translation import gettext_lazy as _



load_dotenv()
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/6.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY')
DEBUG = True
ALLOWED_HOSTS = ['127.0.0.1', 'localhost']



# Application definition

INSTALLED_APPS = [
    'modeltranslation',
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'django_ckeditor_5',

    'main.apps.MainConfig',
    'contacts.apps.ContactsConfig',
    'news.apps.NewsConfig',
    'events.apps.EventsConfig',
    'abiturient.apps.AbiturientConfig',
    'education.apps.EducationConfig',
    'people.apps.PeopleConfig',
    'about.apps.AboutConfig'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.i18n',
                'contacts.context_processors.global_contacts',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'


# Database
# https://docs.djangoproject.com/en/6.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/6.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/6.0/topics/i18n/

LANGUAGE_CODE = 'ru'

TIME_ZONE = 'Asia/Bishkek'

USE_I18N = True

USE_TZ = True



LANGUAGES = (
    ('ru', _('Russian')),
    ('en', _('English')),
    ('ky', _('Kyrgyz')),
)

LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale'),
]


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/6.0/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'assets'),
]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Документы абитуриентов: не раздаются публично, только через админку
PRIVATE_MEDIA_URL = '/private-files/'
PRIVATE_MEDIA_ROOT = BASE_DIR / 'private_media'


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

JAZZMIN_SETTINGS = {
    # === Основная информация ===
    "site_title": "IT-College Admin",
    "site_header": "IT-College",
    "site_brand": "IT-College",
    "site_logo": "img/favicon.png",
    "login_logo": "img/favicon.png",
    "login_logo_dark": "img/favicon.png",
    "site_logo_classes": "img-circle",
    "site_icon": "img/favicon.png",
    "welcome_sign": "Добро пожаловать в панель управления IT-College",
    "copyright": "IT-College © 2025",

    # === Поиск в шапке ===
    "search_model": ["auth.user"],

    # === Аватар пользователя ===
    "user_avatar": None,

    # === Верхнее меню ===
    "topmenu_links": [
        {"name": "Главная", "url": "admin:index", "permissions": ["auth.view_user"]},
        {"name": "Сайт", "url": "/", "new_window": True},
    ],

    # === Меню пользователя (справа сверху) ===
    "usermenu_links": [
        {"model": "auth.user"},
    ],

    # === Боковое меню ===
    "show_sidebar": True,
    "navigation_expanded": False,   # компактнее — разворачивать по клику
    "hide_apps": [],
    "hide_models": [],

    # === Порядок приложений в меню ===
    "order_with_respect_to": [
        "auth",
        "main",
        "news",
        "events",
        "education",
        "abiturient",
        "people",
        "contacts",
    ],

    # === Пользовательские иконки (Font Awesome 5) ===
    "icons": {
        # auth
        "auth": "fas fa-shield-alt",
        "auth.user": "fas fa-user",
        "auth.Group": "fas fa-users",

        # main
        "main": "fas fa-home",

        # news
        "news": "fas fa-newspaper",

        # events
        "events": "fas fa-calendar-alt",

        # education
        "education": "fas fa-graduation-cap",

        # abiturient
        "abiturient": "fas fa-user-graduate",

        # people
        "people": "fas fa-id-badge",

        # contacts
        "contacts": "fas fa-address-book",
    },

    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-circle",

    # === Related Modal ===
    "related_modal_active": True,   # удобнее, чем всплывающие окна

    # === UI ===
    "custom_css": "css/admin_custom.css",
    "custom_js": None,
    "use_google_fonts_cdn": True,
    "show_ui_builder": False,       # включите на время настройки темы

    # === Форма редактирования ===
    "changeform_format": "horizontal_tabs",
    "changeform_format_overrides": {
        "auth.user": "collapsible",
        "auth.group": "vertical_tabs",
    },

    # === Выбор языка в админке ===
    "language_chooser": True,
}

JAZZMIN_UI_TWEAKS = {
    "navbar": "navbar-light",        # светлая тема по умолчанию
    "dark_mode_theme": "darkly",     # тёмная тема Bootstrap
    "navbar_fixed": True,
    "sidebar": "sidebar-dark-primary",
    "sidebar_fixed": True,
    "accent": "accent-primary",
    "no_navbar_border": True,
    "actions_sticky_top": True,
}


# === CKEditor 5 (визуальный редактор в админке) ===
# поле редактора нужно явно разрешить для django-modeltranslation
MODELTRANSLATION_CUSTOM_FIELDS = ('CKEditor5Field',)
CKEDITOR_5_FILE_UPLOAD_PERMISSION = 'staff'
CKEDITOR_5_CONFIGS = {
    'default': {
        'toolbar': {
            'items': [
                'heading', '|', 'bold', 'italic', 'underline', 'link', '|',
                'bulletedList', 'numberedList', 'blockQuote', '|',
                'insertImage', 'insertTable', 'mediaEmbed', '|', 'undo', 'redo',
            ],
        },
        'image': {
            'toolbar': ['imageTextAlternative', '|', 'imageStyle:alignLeft',
                        'imageStyle:alignRight', 'imageStyle:alignCenter'],
        },
        'table': {
            'contentToolbar': ['tableColumn', 'tableRow', 'mergeTableCells'],
        },
        'language': 'ru',
    },
}
