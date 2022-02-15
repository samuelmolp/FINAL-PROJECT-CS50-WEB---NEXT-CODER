from .models import Talks, User, Tags
from django.contrib import admin

# Register your models here.
admin.site.register(User)
admin.site.register(Talks)
admin.site.register(Tags)