from django.contrib import admin
from django.contrib.auth.models import Group
from .models import Ugonjwa, Illness, Sign, Merchandise, Image, Department, Doctor, Appointment, ContactMessage

# Register your models here.
admin.site.register(Ugonjwa)
admin.site.register(Illness)
admin.site.register(Sign)
admin.site.register(Merchandise)
admin.site.register(Image)
admin.site.register(Department)
admin.site.register(Doctor)
admin.site.register(Appointment)
admin.site.register(ContactMessage)