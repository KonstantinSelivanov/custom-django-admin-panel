# Custom django admin panel.

# Description
It has a convenient user interface based on Bootstarap 4. It has a django admin panel structure with the possibility of further expansion.

## Screenshots

### Connection

The django custom admin panel is a standalone django application.

Settings in settings.py

INSTALLED_APPS = [
...
'cms.apps.CmsConfig',
]

...

TEMPLATES = [
     {
      'OPTIONS': {
           # 'debug': DEBUG,
           'loaders': [
               'cms.template.Loader', # Loader template
               'django.template.loaders.filesystem.Loader',
               'django.template.loaders.app_directories.Loader',
           ],
          ...
      },
      },
]

# Пользовательская панель администратора django.

## Описание
Имеет удобный пользовательский интерфейс основанный на Bootstarap 4. Имеет структуру django admin panel с возможностью дальнейшего расширения. 

### Скриншоты

#### Подключение

Пользовательская панель администратора django является отеделным django приложением. 

Настройки в settings.py 

INSTALLED_APPS = [
...
'cms.apps.CmsConfig',
] 

...

TEMPLATES = [
    {
'OPTIONS': {
            # 'debug': DEBUG,
            'loaders': [
                'cms.template.Loader', # Загрузчик шаблонов
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
           ],
          ...
      },
      },
]
