from django.contrib import admin

from .models import Category,Vehicles
# Register your models here.
admin.site.register([Category,Vehicles])
