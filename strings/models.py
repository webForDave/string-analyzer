from django.db import models

class String(models.Model):
    id = models.CharField(max_length=70, primary_key=True, unique=True)
    value = models.TextField(unique=True)
    properties = models.JSONField()
    length = models.IntegerField()
    is_palindrome = models.BooleanField()
    word_count = models.IntegerField()
    sha256_hash = models.CharField(max_length=70)
    character_frequency_map = models.JSONField()

    def __str__(self):
        return self.value