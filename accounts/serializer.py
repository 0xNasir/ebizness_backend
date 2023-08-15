from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from accounts.models import Staff, Customer
from store.models import Favourite, Product


class CustomTokenSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super(CustomTokenSerializer, cls).get_token(user)
        token['email'] = user.email
        token['username'] = user.username
        return token


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'username', 'email', 'date_joined']
        read_only_fields = ['id', 'date_joined', 'username']


class StaffProfileSerializer(ModelSerializer):
    user_id = UserSerializer(many=False)

    class Meta:
        model = Staff
        fields = '__all__'


class CustomerProfileSerializer(ModelSerializer):
    user_id = UserSerializer(many=False)

    class Meta:
        model = Customer
        fields = '__all__'


class FavouriteProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        exclude = ['brand', 'category', 'quantity', 'added_on', 'added_by']


class FavouriteSerializer(ModelSerializer):
    product = FavouriteProductSerializer(many=False)

    class Meta:
        model = Favourite
        exclude = ['customer']


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length=200, validators=[validate_password])
    new_password = serializers.CharField(max_length=200, validators=[validate_password])
