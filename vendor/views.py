from django.db.models import F, Avg
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, generics, status, response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny

from vendor import models as vendor_models
from vendor import serializers as vendor_serializer

from orders import models as order_models

# Create your views here.
class VendorModelViewSets(viewsets.ModelViewSet):
    """creating routes/viewsets for listing, creating, updating, and deleting the vendors details"""

    model = vendor_models.Vendors
    queryset = model.objects.all()
    serializer_class = vendor_serializer.VendorSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


class VendorPeformanceMatrics(generics.ListAPIView):
    """ api for analysis of the performance of the vendors based on their orders"""

    model = vendor_models.Vendors
    serializer_class = vendor_serializer.VendorSerializer
    queryset = model.objects.all()
    permission_classes = [AllowAny,]

    def get_queryset(self):
        return self.queryset.filter(vendor_id=self.kwargs.get("vendor_id"))

    def get_on_time_delivery_rate(self, obj):
        completed_orders = order_models.PurchaseOrders.objects.filter(vendor_id=self.kwargs.get("vendor_id"),
                                                                      status=order_models.PurchaseOrders.completed)
        total_completed_orders = completed_orders.count()
        if total_completed_orders > 0:
            on_time_delivery_orders = completed_orders.filter(
                delivery_date__lte=F('acknowledgment_date')).count()
            on_time_delivery_rate = (on_time_delivery_orders / total_completed_orders) * 100
        else:
            on_time_delivery_rate = 0
        return on_time_delivery_rate

    def get_quality_rating_average(self, obj):
        completed_orders = order_models.PurchaseOrders.objects.filter(vendor_id=self.kwargs.get("vendor_id"),
                                                                      status=order_models.PurchaseOrders.completed,
                                                                      quality_rating__isnull=False)
        total_ratings = completed_orders.aggregate(Avg('quality_rating'))
        return total_ratings['quality_rating__avg'] if total_ratings['quality_rating__avg'] else 0

    def get_average_response_time(self, obj):
        orders = order_models.PurchaseOrders.objects.filter(vendor_id=self.kwargs.get("vendor_id"), acknowledgment_date__isnull=False)
        response_times = orders.annotate(response_time=F('acknowledgment_date') - F('issue_date'))
        avg_time = response_times.aggregate(Avg('response_time'))
        return avg_time['response_time__avg'].days if avg_time['response_time__avg'] else 0

    def get_fulfilment_rate(self, obj):
        total_orders = order_models.PurchaseOrders.objects.filter(vendor_id=self.kwargs.get("vendor_id"))
        fulfilled_orders = total_orders.filter(status=order_models.PurchaseOrders.completed)
        return fulfilled_orders.count() / total_orders.count() if total_orders.count() > 0 else 0

    def get(self, request, *args, **kwargs):
        """get the calculation of the performance of the vendor along with all completed orders"""
        vendor = get_object_or_404(vendor_models.Vendors, id=self.kwargs.get("vendor_id"))
        quality_rating_avg = self.get_quality_rating_average(vendor)
        avg_response_time = self.get_average_response_time(vendor)
        fulfillment_rate = self.get_fulfilment_rate(vendor)
        on_time_delivery_rate = self.get_on_time_delivery_rate(vendor)
        data = {
            "vendor_id": self.kwargs.get("vendor_id"),
            "on_time_delivery_rate": on_time_delivery_rate,
            "quality_rating_avg": quality_rating_avg,
            "avg_response_time": avg_response_time,
            "fulfillment_rate": fulfillment_rate
        }

        return response.Response(data, status=status.HTTP_200_OK)