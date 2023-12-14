from django.shortcuts import get_object_or_404
from rest_framework import viewsets, generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny

from orders import models as order_models
from orders import serializers as order_serializer


# Create your views here.
class ItemsViewSets(viewsets.ModelViewSet):
    """api for creating, listing , updating and deleting the items for orders"""

    model = order_models.Items
    serializer_class = order_serializer.ItemsSerializer
    queryset = model.objects.all()
    # authentication_classes = [TokenAuthentication]
    permission_classes = [AllowAny]

class CreatePurchaseOrders(generics.ListCreateAPIView):
    """api for creating, listing, the purchasing orders"""

    model = order_models.PurchaseOrders
    serializer_class = order_serializer.CreatePurchaseOrderSerializer
    queryset = model.objects.all()
    permission_classes = [AllowAny,]

class PurchaseOrdersViews(generics.RetrieveUpdateDestroyAPIView):
    """api for displaying the purchase details, update the orders and deleting the purchased orders"""

    model = order_models.PurchaseOrders
    serializer_class = order_serializer.PurchaseOrderSerializer
    queryset = model.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self):
        """fetching the query based on given po_number of the order"""
        return self.queryset.filter(po_number=self.kwargs.get('po_number')).first()


class OrderAcknowledgementView(generics.RetrieveUpdateAPIView):
    """api for update the acknowledgement date and status of the order"""

    model = order_models.PurchaseOrders
    serializer_class = order_serializer.AcknowledgementSerializer
    queryset = model.objects.all()
    # authentication_classes = [TokenAuthentication]
    permission_classes = [AllowAny,]

    def get_object(self):
        return get_object_or_404(self.model, po_number=self.kwargs.get("po_number"))
