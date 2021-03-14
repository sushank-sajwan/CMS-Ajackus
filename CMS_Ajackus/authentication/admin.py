from django.contrib import admin
from django.contrib.auth.models import Group

# Remove Group As we dont need it.
admin.site.unregister(Group)