from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers, exceptions

from vendor import models as vendor_models


class VendorSerializer(serializers.ModelSerializer):
    """ serializer for listing the vendor details"""

    class Meta:
        model = vendor_models.Vendors
        fields = "__all__"

    def validate_contact_number(self, attrs):
        try:
            if vendor_models.Vendors.objects.get(contact_number=attrs):
                raise exceptions.ValidationError("Contact Number already exists!!!")
        except Exception as e:
            return attrs

    def validate_vendor_name(self, attrs):
        try:
            if vendor_models.Vendors.objects.get(vendor_name=attrs):
                raise exceptions.ValidationError("Vendor already exists with this vendor name!!!")
        except ObjectDoesNotExist:
            return attrs