from rest_framework import serializers
from .models import Product

#Serializer convierte el modelo Product a formato JSON y viceversa
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'product_name', 'product_desc', 'product_price', 'stock_product']
        # 'id' se incluye para identificar cada producto de forma única