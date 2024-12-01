from django.contrib import admin
from django.contrib.auth.models import Group
from .models import Ugonjwa, Illness, Sign, User, Merchandise, Image

# Register your models here.
admin.site.register(Ugonjwa)
admin.site.register(Illness)
admin.site.register(Sign)
admin.site.register(Merchandise)
admin.site.register(Image)

