from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from store.models import Brand, Category, Product, ProductImage, Favourite, Cart


class BrandSerializer(ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ProductSerializer(ModelSerializer):
    product_images = serializers.StringRelatedField(many=True, read_only=True)
    category = CategorySerializer(many=False)
    brand = BrandSerializer(many=False)

    class Meta:
        model = Product
        fields = '__all__'


class ProductCreateUpdateSerializer(ModelSerializer):
    class Meta:
        model = Product
        exclude = ['added_by']


class ImageSerializer(ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image']


class ProductCartQuantitySerializer(ModelSerializer):
    class Meta:
        model = Cart
        fields = ['quantity']
