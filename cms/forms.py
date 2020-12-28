"""
Формы.
"""
from django import forms
from django.contrib.admin.forms import AdminAuthenticationForm


class UserAuthenticationForm(AdminAuthenticationForm):
    """
    Пользовательская форма аутентификации пользователей
    состоящих в группе 'users'.
    """

    def confirm_login_allowed(self, user):
        """
        Проверить разрешен ли вход.
        Переопределение функции класса AdminAuthenticationForm.
        Добавлена проверка вхождения пользователя в группу 'users'.
        """
        param = user.groups.filter(name='users').count()
        if not user.is_active or not param:
            raise forms.ValidationError(
                self.error_messages['invalid_login'],
                code='invalid_login',
                params={'username': self.username_field.verbose_name}
            )
