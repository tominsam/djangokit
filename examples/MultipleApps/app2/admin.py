from django.contrib import admin
from app2.models import *

class TodoAdmin( admin.ModelAdmin ):
    pass

admin.site.register(Todo, TodoAdmin)
