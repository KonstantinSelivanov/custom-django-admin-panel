from django.contrib.admin.sites import AdminSite
from django.contrib.auth.admin import GroupAdmin, UserAdmin
from django.contrib.auth.models import Group, User


from blog.admin import CommentAdmin, PostAdmin
from blog.models import Comment, Post

admin = AdminSite(name='adminpanel')
staff = AdminSite(name='staffpanel')


admin.register(User, UserAdmin)
admin.register(Group, GroupAdmin)
# admin.register(Post, PostAdmin)
# admin.register(Site, AdminSite)
# admin.register(Post, PostAdmin)
# admin.register(Comment, CommentAdmin)
