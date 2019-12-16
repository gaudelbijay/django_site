from django.contrib import admin
from .models import *
from django.apps import  apps
from django.contrib.admin.sites import AlreadyRegistered

# Register your models here.


for geeks_model in apps.get_app_config('geeks_app').get_models():
    try:
        admin.site.register(geeks_model)
    except AlreadyRegistered:
        pass