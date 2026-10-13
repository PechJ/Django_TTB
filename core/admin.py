from django.contrib import admin
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin, GroupAdmin


try:
    admin.site.register(User, UserAdmin)
except admin.sites.AlreadyRegistered:
    pass

try:
    admin.site.register(Group, GroupAdmin)
except admin.sites.AlreadyRegistered:
    pass
