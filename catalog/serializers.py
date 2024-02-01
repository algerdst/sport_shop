from rest_framework import serializers
from .models import Product, Category


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['name', 'brand', 'type_product', 'category', 'price', 'quantity_in_stock', 'slug']

    def to_representation(self, instance):
        rep = super(ProductSerializer, self).to_representation(instance)
        rep['category'] = instance.category.category_name
        rep['brand'] = instance.brand.brand_name
        rep['type_product'] = instance.type_product.type_name
        return rep

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['category_name']
