import re

from django.conf import settings
from django.urls import reverse
from django.utils.text import capfirst
from django.utils.translation import ugettext_lazy as _

from cms.filters import filter_models
from cms.utils import get_admin_site_name, get_admin_site


class Menu(object):
    """
    Базовое меню.
    """
    children = None

    def __init__(self, **kwargs):
        for key in kwargs:
            if hasattr(self.__class__, key):
                setattr(self, key, kwargs[key])
        self.children = kwargs.get('children', [])

    def init_with_context(self, context):
        pass

    def is_user_allowed(self, user):
        """
        Этот метод можно перезаписать, чтобы проверить, видит ли текущий
        пользователь этот элемент.
        """
        return True


class MenuItem(object):
    """
    Это базовый класс для настраиваемых пунктов меню.
    Пункт меню может иметь следующие свойства:

    ``title``
        Строка, содержащая заголовок пункта меню, убедитесь, что вы используете
        функции django gettext, если ваше приложение многоязычно.
        Значение по умолчанию: 'Untitled menu item'.

    ``url``
        Строка, содержащая URL-адрес пункта меню.
        Значение по умолчанию: None (будет отображаться как 'javascript:;').

    ``add_url``
        Необязательная строка, содержащая URL-адрес второго пункта меню.
        Этот URL-адрес позволяет редактировать и добавлять URL-адреса в одном
        пункте меню. add_url - это маленький знак плюса в меню рядом с обычным
        URL-адресом.
        Значение по умолчанию: None.

    ``icon``
        Необязательная строка, содержащая классы для значков из Font Awesome,
        которые следует использовать для этого пункта меню. Обратите внимание,
        что значки могут отображаться не на всех уровнях меню.
        Они поддерживаются только на верхнем уровне.
        Значение по умолчанию: None.

    ``css_styles``
        Строка, содержащая специальный стиль CSS для этого пункта меню.
        Значение по умолчанию: None.

    ``description``
        Необязательная строка, которая будет использоваться в качестве
        атрибута ``title`` тега ``a ``элемента меню.
        Значение по умолчанию: None.

    ``enabled``
        Логическое значение, определяющее, включен ли пункт меню.
        Отключенные элементы отображаются, но на них нельзя нажимать.
        Значение по умолчанию: None.

    ``children``
        Список пунктов подменю. Все дочерние элементы должны быть экземплярами
        класса MenuItem.
    """

    title = 'Untitled menu item'
    url = None
    add_url = None
    icon = None
    css_styles = None
    description = None
    enabled = True
    children = None

    def __init__(self, title=None, url=None, **kwargs):

        if title is not None:
            self.title = title

        if url is not None:
            self.url = url

        for key in kwargs:
            if hasattr(self.__class__, key):
                setattr(self, key, kwargs[key])
        self.children = self.children or []

    def init_with_context(self, context):
        pass

    def is_selected(self, request):
        """
        Вспомогательный метод, возвращает True, если пункт меню активен.
        Пункт меню считается активным, если его url или add_url или один из его
        потомков url или add_url равен текущему URL.
        """
        current_url = request.path

        return self.url == current_url or \
            self.add_url == current_url or \
            bool(re.match(r'^%s\d+/$' % self.url, current_url)) or \
            len([c for c in self.children if c.is_selected(request)]) > 0

    def is_empty(self):
        """
        Вспомогательный метод, который возвращает True, если пункт меню пуст.
        Этот метод всегда возвращает False для базовых элементов, но может
        возвращать True, если элемент является AppList.
        """
        return False

    def is_user_allowed(self, user):
        """
        Этот метод можно перезаписать, чтобы проверить, видит ли текущий
        пользователь этот элемент.
        """
        return True


class ElementMixin(object):
    """
    Класс Mixin для AppList и ModelList MenuItem.
    """

    def _get_visible_models(self, context):
        """
        Получить список видимых моделей.
        """
        included = self.models[:]
        excluded = self.exclude[:]

        if excluded and not included:
            included = ["*"]
        return filter_models(context, included, excluded)

    def _get_admin_app_list_url(self, model, context):
        """
        Получить URL-адрес списка приложений администратора.
        """
        app_label = model._meta.app_label
        return reverse('%s:app_list' % get_admin_site_name(context),
                       args=(app_label,))

    def _get_admin_change_url(self, model, context):
        """
        Получить администратором изменения URL.
        """
        app_label = model._meta.app_label
        return reverse('%s:%s_%s_changelist' % (get_admin_site_name(context),
                                                app_label,
                                                model.__name__.lower()))

    def _get_admin_add_url(self, model, context):
        """
        Получить адрес, добавленный администратором.
        """
        app_label = model._meta.app_label
        return reverse('%s:%s_%s_add' % (get_admin_site_name(context),
                                         app_label,
                                         model.__name__.lower()))

    def is_empty(self):
        return len(self.children) == 0


class AppList(ElementMixin, MenuItem):
    """
    Список приложений.
    """

    def __init__(self, title=None, models=None, exclude=None, **kwargs):
        self.models = list(models or [])
        self.exclude = list(exclude or [])
        super(AppList, self).__init__(title, **kwargs)

    def init_with_context(self, context):

        items = self._get_visible_models(context)
        apps = {}
        for model, perms in items:
            if not perms['change'] and not perms['add']:
                continue
            app_label = model._meta.app_label
            if app_label not in apps:
                apps[app_label] = {
                    'title': capfirst(_(app_label.title())),
                    'url': self._get_admin_app_list_url(model, context),
                    'models': []
                }
            apps[app_label]['models'].append({
                'title': capfirst(model._meta.verbose_name_plural),
                'url': perms['change'] and self._get_admin_change_url(
                    model, context),
                'add_url': perms['add'] and self._get_admin_add_url(
                    model, context),
                'description':
                # Переводчики: это уже переведено на Django.
                perms['change'] and _("Change") or _("No permission"),
            })

        apps_sorted = list(apps.keys())
        apps_sorted.sort()
        for app in sorted(apps.keys()):
            app_dict = apps[app]
            item = MenuItem(
                title=app_dict['title'], url=app_dict['url'],
                description=app_dict['title'])
            # сортировать список моделей по алфавиту
            apps[app]['models'].sort(key=lambda x: x['title'])
            for model_dict in apps[app]['models']:
                item.children.append(MenuItem(**model_dict))
            self.children.append(item)


class ModelList(ElementMixin, MenuItem):
    """
    Список моделей.
    """

    def __init__(self, title=None, models=None, exclude=None, **kwargs):
        self.models = list(models or [])
        self.exclude = list(exclude or [])

        super(ModelList, self).__init__(title, **kwargs)

    def init_with_context(self, context):

        items = self._get_visible_models(context)
        for model, perms in items:
            if not perms['change']:
                continue
            title = capfirst(model._meta.verbose_name_plural)
            url = self._get_admin_change_url(model, context)
            add_url = self._get_admin_add_url(model, context)
            item = MenuItem(
                title=title, url=url, description=title, add_url=add_url)
            self.children.append(item)


class UserTools(MenuItem):
    """
    Инструменты пользователя.
    """
    is_user_tools = True


class DefaultTopMenu(Menu):
    """
    Верхнее меню по умолчанию, которое имитирует заголовок администратора
    Django по умолчанию. Он используется, если в настройках администратора
    Django WP не указано главное меню.
    """

    def init_with_context(self, context):

        self.children += [
            MenuItem(
                title=get_admin_site(context).site_header,
                url=None,
                icon='fa-gears',
                css_styles='font-size: 1.5em;',
            ),
            UserTools(
                css_styles='float: right;',
                is_user_allowed=lambda user: user.is_active and user.is_staff,
            ),
        ]


class BasicTopMenu(Menu):
    """
    Базовое верхнее меню по умолчанию.
    """

    def init_with_context(self, context):

        admin_site_name = get_admin_site_name(context)

        if 'django.contrib.sites' in settings.INSTALLED_APPS:
            from django.contrib.sites.models import Site
            site_name = Site.objects.get_current().name
            site_url = 'http://' + Site.objects.get_current().domain
        else:
            site_name = _('Site')
            site_url = '/'

        self.children += [
            MenuItem(
                title=site_name,
                url=site_url,
                icon='fa-bullseye',
                css_styles='font-size: 1.5em;',
            ),
            MenuItem(
                title=_('Dashboard'),
                icon='fa-tachometer',
                url=reverse('%s:index' % admin_site_name),
                description=_('Dashboard'),
            ),
            UserTools(
                css_styles='float: right;',
                is_user_allowed=lambda user: user.is_staff,
            ),
        ]


class BasicLeftMenu(Menu):
    """
    Основное левое меню по умолчанию.
    """

    def is_user_allowed(self, user):
        """
        Только пользователи, которые сотрудники могут видеть это меню.
        """
        return user.is_staff

    def init_with_context(self, context):

        if self.is_user_allowed(context.get('request').user):

            admin_site_name = get_admin_site_name(context)

            self.children += [
                MenuItem(
                    title=_('Dashboard'),
                    icon='fa-tachometer',
                    url=reverse('%s:index' % admin_site_name),
                    description=_('Dashboard'),
                ),
                AppList(
                    title=_('Applications'),
                    description=_('Applications'),
                    exclude=('django.contrib.*',),
                    icon='fa-tasks',
                ),
                AppList(
                    title=_('Administration'),
                    description=_('Administration'),
                    models=('django.contrib.*',),
                    icon='fa-cog',
                ),
            ]


class UserTopMenu(BasicTopMenu):

    def my_user_check(self, user):
        """
        Пользовательский вспомогательный метод для скрытия некоторых
        пунктов меню от не допущенных пользователей.
        """
        return user.groups.filter(name='users').exists()

    def init_with_context(self, context):

        admin_site_name = get_admin_site_name(context)

        if 'django.contrib.sites' in settings.INSTALLED_APPS:
            from django.contrib.sites.models import Site
            site_name = Site.objects.get_current().name
            site_url = 'http://' + Site.objects.get_current().domain
        else:
            site_name = _('Site')
            site_url = '/'

        self.children += [
            MenuItem(
                title=site_name,
                url=site_url,
                icon='fa-bullseye',
                css_styles='font-size: 1.5em;',
            ),
            MenuItem(
                title=_('Dashboard'),
                icon='fa-tachometer',
                url=reverse('%s:index' % admin_site_name),
                description=_('Dashboard'),
            ),
        ]
        if self.my_user_check(context.get('request').user):
            self.children += [
                AppList(
                    title=_('Applications'),
                    icon='fa-tasks',
                    exclude=('django.contrib.*',),
                ),
                AppList(
                    title=_('Administration'),
                    icon='fa-cog',
                    models=('django.contrib.*',),
                ),
                UserTools(
                    css_styles='float: right;',
                ),
            ]


class UserLeftMenu(BasicLeftMenu):

    def is_user_allowed(self, user):
        """
        Только пользователи, которые находятся в группе «users»,
        могут видеть это меню.
        """
        return user.groups.filter(name='users').count()
