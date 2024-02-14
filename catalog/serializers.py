from rest_framework import serializers

from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        # fields=['name', 'brand', 'type_product', 'category']
        fields='__all__'