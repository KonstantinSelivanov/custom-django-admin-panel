from importlib import import_module

from django.conf import settings
from django.contrib import admin
from django.utils.translation import get_language_from_path


def get_cms_settings(admin_site_name='admin'):
    """
    Получить настройки CMS для указанного сайта администратора.
    """
    return getattr(settings, 'CMS', {}).get(admin_site_name, {})


def get_menu_cls(menu, admin_site_name='admin'):
    """
    menu - название меню ('top' or 'left')
    """
    return get_cms_settings(admin_site_name) \
        .get('menu', {}) \
        .get(menu, None)


def get_menu(menu, admin_site_name='admin'):
    """
    menu - название меню ('top' or 'left')
    """
    menu_cls = get_menu_cls(menu, admin_site_name)
    if menu_cls:
        mod, inst = menu_cls.rsplit('.', 1)
        mod = import_module(mod)
        return getattr(mod, inst)()
    return None


def get_admin_site_name(context):
    """
    Получить имя админки сайта из запроса из контекста.
     Имя админки взято из пути запроса:
     * это первая часть пути - между первой и второй косой чертой, если нет
     префикс языка
     * или вторая часть пути - между второй и третьей косой чертой
    """
    path = context.get('request').path
    lang = get_language_from_path(path)
    path = path.split('/')
    if lang and path[1] == lang:
        return path[2]
    return path[1]


def get_admin_site(context):
    """
    Получить экземпляр админки.
    """
    admin_site = get_cms_settings(get_admin_site_name(context)) \
        .get('admin_site')
    if admin_site:
        mod, inst = admin_site.rsplit('.', 1)
        mod = import_module(mod)
        return getattr(mod, inst)
    else:
        return admin.site
