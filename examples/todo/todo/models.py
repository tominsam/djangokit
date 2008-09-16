from django.db import models

class Todo(models.Model):
    date = models.DateTimeField('date created', auto_now_add = True)
    value = models.CharField(max_length = 200)
    completed = models.BooleanField()
    
    class Admin:

        list_display = [ 'date', 'value', 'completed' ]
        
        fields = [
            [ None, { 'fields':[ 'date', 'value', 'completed' ] } ],
        ]
        
        list_filter = [ 'completed' ]
        search_fields = [ 'value' ]
