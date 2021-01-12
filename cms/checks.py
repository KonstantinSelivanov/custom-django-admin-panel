from django.core.checks import register
from django.template.loader import get_template, TemplateDoesNotExist


@register('cms')
def check_cms_configuration(app_config=None, **kwargs):
    result = []
    try:
        get_template('admin:admin/base.html')
    except TemplateDoesNotExist:
        print('error!!!!!')
    return result
