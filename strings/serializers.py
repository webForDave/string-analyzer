from rest_framework import serializers
from .models import String

class StringSerializer(serializers.ModelSerializer):
    class Meta:
        model = String
        fields = ["id", "value"]
        read_only_fields = ["id"]