from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework import viewsets, mixins, status, serializers
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from accounts.models import Staff, Customer
from accounts.serializer import CustomTokenSerializer, StaffProfileSerializer, CustomerProfileSerializer, \
    UserSerializer, FavouriteSerializer, ChangePasswordSerializer
from ebizness.no_serializer import NoSerializer
from store.models import Favourite


# Create your views here.
class CustomObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = CustomTokenSerializer


class StaffProfileAPIView(viewsets.GenericViewSet,
                          mixins.ListModelMixin,
                          mixins.CreateModelMixin):
    serializer_class = StaffProfileSerializer
    queryset = Staff.objects.all()

    def list(self, request, *args, **kwargs):
        user = self.request.user
        staff = Staff.objects.filter(user_id=user.id)
        if staff.exists():
            return Response(self.serializer_class(staff.first(), many=False).data, status=status.HTTP_200_OK)
        else:
            return Response({'details': 'Please login first'}, status=status.HTTP_401_UNAUTHORIZED)

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = UserSerializer(data=serializer.validated_data['user_id'], instance=self.request.user)
        user.is_valid(raise_exception=True)
        user.save()
        instance = Staff.objects.filter(user_id=self.request.user)
        if instance.exists():
            staff = instance.first()
            staff.salary = serializer.validated_data['salary']
            staff.birth_date = serializer.validated_data['birth_date']
            staff.designation = serializer.validated_data['designation']
            staff.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class CustomerProfileAPIView(viewsets.GenericViewSet,
                             mixins.ListModelMixin,
                             mixins.CreateModelMixin):
    queryset = Customer.objects.all()

    def get_serializer_class(self):
        if self.action in ['remove']:
            return NoSerializer
        elif self.action in ['favourite']:
            return FavouriteSerializer
        return CustomerProfileSerializer

    def list(self, request, *args, **kwargs):
        user = self.request.user
        customer = Customer.objects.filter(user_id=user.id)
        if customer.exists():
            return Response(self.serializer_class(customer.first(), many=False).data, status=status.HTTP_200_OK)
        else:
            return Response({'details': 'Please login first'}, status=status.HTTP_401_UNAUTHORIZED)

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = UserSerializer(data=serializer.validated_data['user_id'], instance=self.request.user)
        user.is_valid(raise_exception=True)
        user.save()
        instance = Customer.objects.filter(user_id=self.request.user)
        if instance.exists():
            customer = instance.first()
            customer.user_badge = serializer.validated_data['user_badge']
            customer.contact_number = serializer.validated_data['contact_number']
            customer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_path='favourites', serializer_class=FavouriteSerializer)
    def favourite(self, request):
        customer = Customer.objects.filter(user_id=self.request.user).first()
        images = Favourite.objects.filter(customer=customer)
        return Response(self.serializer_class(images, many=True).data, status.HTTP_200_OK)


class RemoveFavouriteAPIView(viewsets.GenericViewSet,
                             mixins.DestroyModelMixin):
    queryset = Favourite.objects.all()
    serializer_class = []


class ChangePasswordAPIView(viewsets.GenericViewSet,
                            mixins.CreateModelMixin):
    serializer_class = ChangePasswordSerializer
    queryset = User.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.get(id=self.request.user.id)
        if user.check_password(serializer.validated_data['old_password']):
            raise serializers.ValidationError('Incorrect current password')
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        return Response({'details': 'Password is changed successfully!'}, status.HTTP_200_OK)
