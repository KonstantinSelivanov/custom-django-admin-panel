from django import template

from cms.utils import get_admin_site_name, get_menu


register = template.Library()


class IsMenuEnabledNode(template.Node):
    """
    Узел с включенным меню.
    """

    def __init__(self, menu_name):
        """
        menu_name - название меню ('top' or 'left')
        """
        self.menu_name = menu_name

    def render(self, context):
        menu = get_menu(self.menu_name, get_admin_site_name(context))
        if menu and menu.is_user_allowed(context.get('request').user):
            enabled = True
        else:
            enabled = False
        context['is_%s_menu_enabled' % self.menu_name] = enabled
        return ''


@register.tag('is_left_menu_enabled')
def is_left_menu_enabled(parser, token):
    """
    Включено меню слева.
    """
    return IsMenuEnabledNode('left')


@register.inclusion_tag('menu/top_menu.html', takes_context=True)
def render_top_menu(context):
    """
    Отобразить веню сверху.
    """
    menu = get_menu('top', get_admin_site_name(context))
    if not menu:
        from cms.services import DefaultTopMenu
        menu = DefaultTopMenu()
    menu.init_with_context(context)
    context.update({
        'menu': menu,
        'is_user_allowed': menu.is_user_allowed(context.get('request').user),
    })
    return context


@register.inclusion_tag('menu/left_menu.html', takes_context=True)
def render_left_menu(context):
    """
    Отобразить меню слева.
    """
    menu = get_menu('left', get_admin_site_name(context))
    if menu:
        menu.init_with_context(context)
        context.update({
            'menu': menu,
            'is_user_allowed': menu.is_user_allowed(
                context.get('request').user),
        })
    return context


@register.inclusion_tag('menu/menu_top_item.html', takes_context=True)
def render_menu_top_item(context, item, is_first, is_last):
    """
    Отобразить верхний пункт меню сверху.
    """
    item.init_with_context(context)
    if item.icon:
        icon = item.icon
    else:
        icon = 'fa-folder-o'
    context.update({
        'item': item,
        'is_first': is_first,
        'is_last': is_last,
        'icon': icon,
        'is_selected': item.is_selected(context.get('request')),
        'is_user_allowed': item.is_user_allowed(context.get('request').user),
    })
    return context


@register.inclusion_tag('menu/menu_item.html', takes_context=True)
def render_menu_item(context, item, is_first, is_last):
    """
    Отобразить пункт меню.
    """
    item.init_with_context(context)
    context.update({
        'item': item,
        'is_first': is_first,
        'is_last': is_last,
        'is_selected': item.is_selected(context.get('request')),
        'is_user_allowed': item.is_user_allowed(context.get('request').user),
    })
    return context


@register.inclusion_tag('menu/user_tools.html', takes_context=True)
def render_user_tools(context, item, is_first, is_last):
    """
    Отобразить инструменты пользователя.
    """
    item.init_with_context(context)
    context.update({
        'item': item,
        'is_first': is_first,
        'is_last': is_last,
        'is_user_allowed': context.get('request').user.is_authenticated and
                           item.is_user_allowed(context.get('request').user),
    })
    return context
