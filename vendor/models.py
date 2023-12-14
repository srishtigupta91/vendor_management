from phonenumber_field.modelfields import PhoneNumberField
from django.db import models

# Create your models here.
class Vendors(models.Model):
    """model for adding the information of the vendors"""

    vendor_code = models.CharField(max_length=200, unique=True)
    vendor_name = models.CharField(max_length=255, null=True, blank=True)
    contact_number = PhoneNumberField()
    address = models.CharField(max_length=256, null=True, blank=True)
    on_time_delivery_rate = models.FloatField(default=0.0)
    quality_rating_avg = models.FloatField(default=0.0)
    average_response_time = models.FloatField(default=0.0)
    fulfillment_rate = models.FloatField(default=0.0)

    class Meta:
        app_label = 'vendor'

    def __str__(self):
        return "{0}-----------{1}".format(self.vendor_code, self.vendor_name)

