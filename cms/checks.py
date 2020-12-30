from django.core.checks import register
from django.template.loader import get_template


@register('cms')
def check_cms_configuration(app_config=None, **kwargs):
    result = []
    get_template('cms:cms/base.html')
    return result
