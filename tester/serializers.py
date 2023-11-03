from .models import Test
from rest_framework import serializers

class Testserializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = ["quiz","points"]