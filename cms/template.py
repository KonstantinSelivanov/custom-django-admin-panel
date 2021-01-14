"""Загрузчик шаблонов Django"""
from os.path import join
from django.apps import apps

from django.template.loaders.filesystem import Loader as FilesystemLoader

_cache = {}


def get_app_template_dir(app_name):
    """
    Получить каталог шаблонов для приложения.
    Использует интерфейс приложений,доступный в django 1.7+.
    Возвращает полный путь или None, если приложение не было найдено.
    """
    if app_name in _cache:
        return _cache[app_name]
    template_dir = None
    for app in apps.get_app_configs():
        if app.label == app_name:
            template_dir = join(app.path, 'templates')
            break
    _cache[app_name] = template_dir
    return template_dir


class Loader(FilesystemLoader):
    is_usable = True

    def get_template_sources(self, template_name, template_dirs=None):
        """
        Возвращает абсолютные пути к «template_name» в указанном приложении.
        Если имя не содержит имени приложения (без двоеточия),
        возвращается пустой список.
        Родительский FilesystemLoader.load_template_source() позаботится
        о фактической загрузке за нас.
        """
        if ':' not in template_name:
            return []
        app_name, template_name = template_name.split(":", 1)
        template_dir = get_app_template_dir(app_name)
        if template_dir:
            try:
                from django.template import Origin
                origin = Origin(
                    name=join(template_dir, template_name),
                    template_name=template_name,
                    loader=self,
                )
            except (ImportError, TypeError):
                origin = join(template_dir, template_name)
            return [origin]
        return []
