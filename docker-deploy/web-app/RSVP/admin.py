from django.contrib import admin

from .models import *

admin.site.register(Event)
admin.site.register(Role)
admin.site.register(Question)
admin.site.register(Choice)
admin.site.register(Response)