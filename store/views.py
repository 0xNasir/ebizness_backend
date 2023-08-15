import coreapi
from django.shortcuts import redirect
from django.views import View
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.filters import BaseFilterBackend
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from accounts.models import Staff, Customer
from ebizness.no_serializer import NoSerializer
from store.models import Brand, Category, Product, ProductImage, Favourite, Cart
from store.serializer import BrandSerializer, CategorySerializer, ProductSerializer, ProductCreateUpdateSerializer, \
    ImageSerializer, ProductCartQuantitySerializer


class Home(View):
    def get(self, request):
        return redirect('/docs')


def error_404_handler(request, exception):
    return redirect('/docs')


# Create your views here.
class BrandAPIView(viewsets.GenericViewSet,
                   mixins.ListModelMixin,
                   mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin):
    serializer_class = BrandSerializer
    queryset = Brand.objects.all()
    parser_classes = (MultiPartParser,)

    @action(detail=True, methods=['get'], url_path='products', serializer_class=ProductSerializer)
    def products(self, request, pk):
        obj = self.get_object()
        product = Product.objects.filter(brand=obj)
        return Response(self.serializer_class(product, many=True).data, status.HTTP_200_OK)


class CategoryAPIView(viewsets.GenericViewSet,
                      mixins.ListModelMixin,
                      mixins.CreateModelMixin,
                      mixins.RetrieveModelMixin,
                      mixins.UpdateModelMixin):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()

    @action(detail=True, methods=['get'], url_path='products', serializer_class=ProductSerializer)
    def products(self, request, pk):
        obj = self.get_object()
        product = Product.objects.filter(category=obj)
        return Response(self.serializer_class(product, many=True).data, status.HTTP_200_OK)


class ProductFilterBackend(BaseFilterBackend):
    def get_schema_fields(self, view):
        return [coreapi.Field(
            name='name',
            location='query',
            required=False,
            type='string'
        ), coreapi.Field(
            name='category',
            location='query',
            required=False,
            type='string'
        )]


class ProductAPIView(viewsets.GenericViewSet,
                     mixins.ListModelMixin,
                     mixins.CreateModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin):
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return []
        else:
            return [IsAuthenticated()]

    def get_serializer_class(self):
        if self.action in ['create', 'update']:
            return ProductCreateUpdateSerializer
        if self.action in ['add_to_cart']:
            return ProductCartQuantitySerializer
        elif self.action in ['images']:
            return ImageSerializer
        elif self.action in ['add_to_favourite']:
            return NoSerializer
        else:
            return ProductSerializer

    queryset = Product.objects.all()
    filter_backends = (ProductFilterBackend,)

    def filter_queryset(self, request):
        if self.request.query_params.get('name'):
            return self.get_queryset().filter(name__icontains=self.request.query_params.get('name'))
        return self.get_queryset()

    def create(self, request, *args, **kwargs):
        serializer = ProductCreateUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        staff = Staff.objects.get(user_id=self.request.user.id)
        if staff is None:
            return Response({'details': 'Invalid authentication'}, status=status.HTTP_401_UNAUTHORIZED)
        serializer.validated_data['added_by'] = staff
        serializer.save()
        return Response(serializer.data, status.HTTP_201_CREATED)

    @action(detail=True, methods=['get'], url_path='images', serializer_class=ImageSerializer)
    def images(self, request, pk):
        obj = self.get_object()
        images = ProductImage.objects.filter(product=obj)
        return Response(self.serializer_class(images, many=True).data, status.HTTP_200_OK)

    @action(detail=True, methods=['post'], url_path='add_to_favourite')
    def add_to_favourite(self, request, pk):
        obj = self.get_object()
        try:
            customer = Customer.objects.get(user_id=self.request.user)
            try:
                g = Favourite.objects.get(customer=customer, product=obj)
                return Response({'details': 'Product exists in favourite list'}, status.HTTP_200_OK)
            except:
                Favourite.objects.create(customer=customer, product=obj)
                return Response({'details': 'Product is added to favourite'}, status.HTTP_201_CREATED)
        except:
            return Response({'details': 'Unauthorized access'}, status.HTTP_401_UNAUTHORIZED)

    @action(detail=True, methods=['post'], url_path='add_to_cart')
    def add_to_cart(self, request, pk):
        obj = self.get_object()
        try:
            customer = Customer.objects.get(user_id=self.request.user)
            try:
                g = Cart.objects.get(customer=customer, product=obj)
                return Response({'details': 'Product exists in cart list'}, status.HTTP_200_OK)
            except:
                serializer = ProductCartQuantitySerializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                Cart.objects.create(customer=customer, product=obj, quantity=serializer.validated_data['quantity'])
                return Response({'details': 'Product is added to cart'}, status.HTTP_201_CREATED)
        except:
            return Response({'details': 'Unauthorized access'}, status.HTTP_401_UNAUTHORIZED)
