from django.contrib.admin.sites import AdminSite
from django.contrib.auth.admin import GroupAdmin, UserAdmin
from django.contrib.auth.models import Group, User
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from cms.sites import UserSite
from cms.services import MenuItem, UserLeftMenu
from cms.utils import get_admin_site_name


admin = AdminSite(name='adminpanel')
staff = AdminSite(name='staffpanel')
user = UserSite(name='userpanel')

admin.register(User, UserAdmin)
admin.register(Group, GroupAdmin)


class UserLeftMenu(UserLeftMenu):

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
                MenuItem(
                    title=_('Посты'),
                    icon='fa-book',
                    # url=reverse('%s:blog_post_changelist' % admin_site_name),
                ),
                MenuItem(
                    title=_('Коментарии'),
                    icon='fa-music',
                    # url=reverse('%s:blog_comment_changelist' % admin_site_name),
                ),
                MenuItem(
                    title=_('DVDs'),
                    icon='fa-film',
                    # url=reverse('%s:dvds_dvd_changelist' % admin_site_name),
                ),
            ]