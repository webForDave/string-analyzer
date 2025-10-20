from django.db import models

class String(models.Model):
    id = models.CharField(max_length=70, primary_key=True, unique=True)
    value = models.TextField(unique=True)

    def __str__(self):
        return self.value