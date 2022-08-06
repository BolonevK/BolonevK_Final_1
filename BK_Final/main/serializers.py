import io

from rest_framework import serializers
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer

from .models import Products


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = '__all__'
        # fields = ("id", "name", "factory", "p_text", "balance", "coast", "cat")


# class ProductSerializer(serializers.Serializer):
#     name = serializers.CharField(max_length=100)
#     factory = serializers.CharField(max_length=250)
#     p_text = serializers.CharField()
#     balance = serializers.IntegerField()
#     coast = serializers.DecimalField(max_digits=10, decimal_places=2)
#     cat_id = serializers.IntegerField()
#
#     def create(self, validated_data):
#         return Products.objects.create(**validated_data)
#
#     def update(self, instance, validated_data):
#         instance.name = validated_data.get("name", instance)
#         instance.p_text = validated_data.get("p_text", instance)
#         instance.balance = validated_data.get("balance", instance)
#         instance.factory = validated_data.get("factory", instance)
#         instance.coast = validated_data.get("coast", instance)
#         instance.cat_id = validated_data.get("cat_id", instance)
#         instance.save()
#         return instance
