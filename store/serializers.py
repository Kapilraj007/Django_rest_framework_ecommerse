from rest_framework import serializers
from decimal import Decimal
from .models import *
from django.contrib.auth.models import User



class CustomerSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Customer
        fields = ['id', 'user_id', 'phone', 'birth_date', 'membership']

class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['id', 'title', 'products_count']

    products_count = serializers.IntegerField(read_only=True)
    
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id','collection','title','stock','description','price','price_with_tax','vendor']
        
    price_with_tax = serializers.SerializerMethodField(
        method_name='calculate_tax')
    
    def calculate_tax(self, product: Product):
        return product.price * Decimal(1.1)
    
class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id','title','price']

        
class OrderSerializer(serializers.ModelSerializer):
    product= SimpleProductSerializer()
   
    total_price =serializers.SerializerMethodField()
    class Meta:
        model = Order
        fields = ['id','user','product','quantity','status','total_price']
    def get_total_price(self, order):
        product_price = order.product.price
        return order.quantity * product_price
    
class CreateOrderSerializer(serializers.ModelSerializer):      
    class Meta:
        model = Order
        fields = ['id','product','quantity','status']
        
    def create(self, validated_data):
        user_id = self.context['user_id']
        validated_data['user_id'] = user_id
        return Order.objects.create(**validated_data)

class UpdateSerializer(serializers.ModelSerializer):
        class Meta:
                model = Order
                fields = ['id','quantity','status']
   