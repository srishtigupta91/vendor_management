from django.db import models
from django.dispatch import receiver


class Items(models.Model):
    """adding the items information"""

    serial_no = models.CharField(max_length=200, unique=True, db_index=True)
    item_name = models.CharField(max_length=100, null=True, blank=True)
    item_description = models.CharField(max_length=256, null=True, blank=True)
    size = models.CharField(max_length=200, null=True, blank=True)
    price = models.FloatField(default=0.0)


    def __str__(self):
        return "{0}".format(self.item_name)


class PurchaseOrders(models.Model):
    """
    adding order details information of the purchase history
    """

    pending = 0
    completed = 1
    canceled = 2

    STATUS = (
        (pending, "Pending"),
        (completed, "Completed"),
        (canceled, "Cancelled")
    )

    po_number = models.CharField(max_length=100, unique=True)
    vendor = models.ForeignKey(
        "vendor.Vendors",
        on_delete=models.CASCADE,
        related_name="vendor_orders",
    )
    order_date = models.DateTimeField(auto_now_add=True)
    delivery_date = models.DateTimeField(auto_now=True)
    items = models.ForeignKey(
        "orders.Items",
        on_delete=models.CASCADE,
        related_name="ordered_items"
    )
    quantity = models.IntegerField(default=0)
    status = models.CharField(max_length=200, choices=STATUS)
    quality_rating = models.FloatField(default=0.0)
    issue_date = models.DateTimeField(auto_now_add=True)
    acknowledgment_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        app_label = "orders"

    def __str__(self):
        return "{0}".format(self.po_number)


@receiver(models.signals.post_save, sender=PurchaseOrders)
def update_vendor_metrics(sender, instance, created, **kwargs):
    if instance.status == PurchaseOrders.completed and instance.delivery_date:
        completed_orders = PurchaseOrders.objects.filter(vendor=instance.vendor, status=PurchaseOrders.completed)

        # On-Time Delivery Rate calculation
        total_completed_orders = completed_orders.count()
        on_time_delivery_orders = completed_orders.filter(delivery_date__lte=models.F('acknowledgment_date')).count()
        instance.vendor.on_time_delivery_rate = (on_time_delivery_orders / total_completed_orders) * 100 if total_completed_orders else 0

        # Quality Rating Average calculation
        quality_ratings = completed_orders.exclude(quality_rating__isnull=True).values_list('quality_rating', flat=True)
        instance.vendor.quality_rating_avg = sum(quality_ratings) / len(quality_ratings) if quality_ratings else 0

        # Average Response Time calculation
        response_times = completed_orders.exclude(acknowledgment_date__isnull=True).annotate(
            response_time=models.ExpressionWrapper(
                models.F('acknowledgment_date') - models.F('issue_date'),
                output_field=models.DurationField()
            )
        ).values_list('response_time', flat=True)
        total_response_time_seconds = sum(response.total_seconds() for response in response_times)
        total_completed_orders = len(response_times)
        instance.vendor.average_response_time = total_response_time_seconds / total_completed_orders if total_completed_orders else 0

        # Fulfillment Rate calculation
        total_orders = PurchaseOrders.objects.filter(vendor=instance.vendor).count()
        successful_orders = completed_orders.exclude(issue_date__isnull=True).count()
        instance.vendor.fulfillment_rate = (successful_orders / total_orders) * 100 if total_orders else 0
        # Save the updated metrics
        instance.vendor.save()