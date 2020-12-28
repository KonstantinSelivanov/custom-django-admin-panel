from django import template
from django.utils.translation import ugettext_lazy as _

from cms.utils import get_admin_site_name, get_cms_settings


register = template.Library()


@register.simple_tag(name='render_custom_style', takes_context=True)
def render_custom_style(context):
    """
    Визуализировать собственный стиль.
    """
    custom_style_path = get_cms_settings(get_admin_site_name(context)) \
        .get('custom_style', None)
    if custom_style_path:
        return '<link type="text/css" rel="stylesheet" href="%s" />' \
            % custom_style_path
    else:
        return ''


class AreBreadcrumbsEnabledNode(template.Node):
    """
    Включен узел навигационной цепочки.
    """
    def are_breadcrumbs_enabled(admin_site_name='admin'):
        """
        Включены навигационной цепочки.
        """
        return get_cms_settings(admin_site_name).get('dashboard', {}) \
            .get('breadcrumbs', True)

    def render(self, context):
        """
        Отобразить.
        """
        context['are_breadcrumbs_enabled'] = self.are_breadcrumbs_enabled(
            get_admin_site_name(context))
        return ''


@register.tag(name='show_breadcrumbs')
def show_breadcrumbs(parser, token):
    """
    Включить узел навигационной цепочки.
    Отображается стандартная навигационная цепока.
    """
    return AreBreadcrumbsEnabledNode()


@register.simple_tag(takes_context=True)
def render_custom_title(context):
    """
    Отобразить настраеваемый заголовок.
    """
    # Переводчики: это уже переведено на Django.
    return get_cms_settings(get_admin_site_name(context)) \
        .get('title', context.get('site_title', _('Django site admin')))
