from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, Serializer

from sales.models import Promo, Order
from store.models import Cart, Product
from store.serializer import ProductSerializer, ImageSerializer


class PromoSerializer(ModelSerializer):
    class Meta:
        model = Promo
        fields = '__all__'


class ApplyPromoSerializer(Serializer):
    promo_code = serializers.CharField(max_length=200)
    order_id = serializers.IntegerField()


class PromoCreateSerializer(ModelSerializer):
    class Meta:
        model = Promo
        fields = ['promo_code', 'promo_type', 'amount', 'description', 'started_at', 'validity']


class OrderSerializer(ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'


class CartedProductSerializer(ModelSerializer):
    product_images=ImageSerializer(many=True)
    class Meta:
        model = Product
        fields = ['name', 'sku', 'weight', 'price', 'price2', 'product_images']


class CartSerializer(ModelSerializer):
    product = CartedProductSerializer(many=False)

    class Meta:
        model = Cart
        fields = ['id', 'product', 'quantity']
