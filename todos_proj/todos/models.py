from django.db import models

# Create your models here.

class Todo(models.Model):
    item = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)
    
    def __str__(self):
        return self.item