from rest_framework import serializers
from .models import String

class StringSerializer(serializers.ModelSerializer):
    class Meta:
        model = String
        fields = ["id", "value", "properties", "length", "is_palindrome", "word_count", "sha256_hash", "character_frequency_map"]
        read_only_fields = ["id", "properties", "length", "is_palindrome", "word_count", "sha256_hash", "character_frequency_map"]

class SingleStringSerializer(serializers.ModelSerializer):
    class Meta:
        model = String
        fields = ["id", "value", "properties"]