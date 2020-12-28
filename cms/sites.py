from django.contrib.admin.sites import AdminSite

from cms.forms import UserAuthenticationForm


class UserSite(AdminSite):

    login_form = UserAuthenticationForm

    def has_permission(self, request):
        """
        Разрешить всем пользователям, которые находятся в группе `users`.
        """
        return request.user.is_active \
            and request.user.groups.filter(name='users').count()
