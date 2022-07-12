from rest_framework import serializers
from .models import Store


class StoreSerializer(serializers.Serializer):
    title = serializers.CharField()
    description = serializers.CharField()
    rating = serializers.IntegerField()

    def create(self, validated_data):
        result = Store.objects.create(**validated_data)
        return result


