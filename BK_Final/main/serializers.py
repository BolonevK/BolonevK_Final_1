from rest_framework import serializers
from .models import Products

class ProductSerializer(serializers.ModelSerializer):   # формирование класса сериалайзера
    class Meta:
        model = Products                                # привязка сериалайзера к модели
        fields = '__all__'                              # установка все полей по модели
