from rest_framework import serializers

from orders import models as order_models
from vendor import models as vendor_models

class CreatePurchaseOrderSerializer(serializers.ModelSerializer):
    """serializer for creating the purchase order of vendor"""

    class Meta:
        model = order_models.PurchaseOrders
        exclude = ("quality_rating", "acknowledgment_date")

class PurchaseOrderSerializer(serializers.ModelSerializer):
    """serializer for updating, deleting and listing the details of the orders of vendor"""

    vendor = serializers.SerializerMethodField(
        read_only=True, method_name="get_vendor_details")

    class Meta:
        model = order_models.PurchaseOrders
        fields = ("po_number", "status", "vendor")

    def get_vendor_details(self, obj):
        data = {"name": obj.vendor.vendor_name, "vendor_code": obj.vendor.vendor_code,
                "on_time_delivery_rate": obj.vendor.on_time_delivery_rate}
        return data


class ItemsSerializer(serializers.ModelSerializer):
    """serializer for creating, updating, retrieving and deleting the items of any order"""

    class Meta:
        model = order_models.Items
        fields = "__all__"


class AcknowledgementSerializer(serializers.ModelSerializer):
    """serializer for updating the acknowledgement information of the vendor"""

    class Meta:
        model = order_models.PurchaseOrders
        fields = ("po_number", "acknowledgment_date",)
