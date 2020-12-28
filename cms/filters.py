"""
Фильтры.
"""
from fnmatch import fnmatch

from cms.utils import get_admin_site


def filter_models(context, models, exclude):
    """
    Фильтр моделей.
    Возвратить (model, perm,) для всех моделей, которые соответствуют
    моделям / исключают шаблоны и видны текущему пользователю.
    """

    list_models = []

    admin_site = get_admin_site(context)
    for model, model_admin in list(admin_site._registry.items()):
        perms = model_admin.get_model_perms(context.get('request'))
        if True not in list(perms.values()):
            continue
        list_models.append((model, perms,))

    included = []

    def full_name(m):
        return '%s.%s' % (m.__module__, m.__name__)

    if len(models) == 0:
        included = list_models
    else:
        for pattern in models:
            for item in list_models:
                model, perms = item
                if fnmatch(full_name(model), pattern) and item not in included:
                    included.append(item)
 
    result = included[:]
    for pattern in exclude:
        for item in included:
            model, perms = item
            if fnmatch(full_name(model), pattern):
                try:
                    result.remove(item)
                except ValueError:  # если элемент уже был удален, пропустить
                    pass
    return result
