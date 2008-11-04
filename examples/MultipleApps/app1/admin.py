from django.contrib import admin
from app1.models import *

class TodoAdmin( admin.ModelAdmin ):
    pass

admin.site.register(Todo, TodoAdmin)
