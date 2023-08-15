import datetime

from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response

from ebizness.no_serializer import NoSerializer
from sales.models import Promo, Order
from sales.serializer import PromoSerializer, PromoCreateSerializer, ApplyPromoSerializer, OrderSerializer, \
    CartSerializer
from store.models import Cart


# Create your views here.
class PromoAPIView(viewsets.GenericViewSet,
                   mixins.ListModelMixin,
                   mixins.CreateModelMixin):
    queryset = Promo.objects.all()

    def get_serializer_class(self):
        if self.action in ['create']:
            return PromoCreateSerializer
        elif self.action in ['invoke']:
            return NoSerializer
        else:
            return PromoSerializer

    @action(methods=['post'], detail=True)
    def invoke(self, request, pk):
        obj = self.get_object()
        obj.invoke = True
        obj.save()
        return Response(PromoSerializer(obj, many=False).data, status.HTTP_201_CREATED)


class ApplyPromoAPIView(viewsets.GenericViewSet,
                        mixins.CreateModelMixin):
    queryset = Promo.objects.all()
    serializer_class = ApplyPromoSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            order = Order.objects.get(id=serializer.validated_data['order_id'])
            if order.order_status == 'Declined':
                return Response({'details': 'Order was declined'}, status.HTTP_404_NOT_FOUND)
            if order.order_status == 'Cancelled':
                return Response({'details': 'Order was cancelled'}, status.HTTP_404_NOT_FOUND)
            if order.order_status == 'Packaging':
                return Response({'details': 'Order is under packaging. Promo is not applicable'},
                                status.HTTP_404_NOT_FOUND)
            if order.order_status == 'Shifted to Rider':
                return Response({'details': 'Product is shifted to Rider. Promo is not applicable'},
                                status.HTTP_404_NOT_FOUND)
            if order.order_status == 'Delivered':
                return Response({'details': 'Order is delivered. Promo is not applicable'}, status.HTTP_404_NOT_FOUND)
            try:
                promo = Promo.objects.get(promo_code=serializer.validated_data['promo_code'], invoke=False,
                                          started_at__lte=datetime.datetime.today())
                order.is_promo_applied = True
                order.promo = promo
                if promo.promo_type == 'Percentage':
                    order.promo_discount = order.net_price * (promo.amount / 100)
                else:
                    order.promo_discount = promo.amount
                order.final_price = order.net_price - order.promo_discount
                order.save()
                return Response(OrderSerializer(order, many=False).data, status.HTTP_200_OK)
            except:
                return Response({'details': 'Invalid Promo code'}, status.HTTP_404_NOT_FOUND)
        except:
            return Response({'details': 'No order found to apply promo code'}, status.HTTP_404_NOT_FOUND)


class CartAPIView(viewsets.GenericViewSet,
                  mixins.ListModelMixin,
                  mixins.CreateModelMixin):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

    def list(self, request, *args, **kwargs):
        return Response(CartSerializer(Cart.objects.filter(customer__user_id=self.request.user), many=True).data,
                        status.HTTP_200_OK)
