from django.db import models


# Create your models here.
class Performance(models.Model):
    """vendor performance model for getting the analytics of the historical vendors data"""

    vendor = models.ForeignKey("vendor.Vendors", related_name="vendor_performance", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    on_time_delivery_rate = models.FloatField(default=0.0)
    quality_rating_avg = models.FloatField(default=0.0)
    average_response_time = models.FloatField(default=0.0)
    fulfillment_rate = models.FloatField(default=0.0)

    class Meta:
        app_label = "performance"

    def __str__(self):
        return "{0} ---- {1}".format(self.vendor.name, self.created_at)
