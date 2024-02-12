from django.db import models
from django.conf import settings
from datetime import datetime   

# Create your models here.
class TodoItem(models.Model):
    titel = models.CharField(max_length=50)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(default=datetime.now, blank=True)
    checked = models.BooleanField(default=False)
    
    def __str__(self):
        return f'({self.id}) {self.titel}'