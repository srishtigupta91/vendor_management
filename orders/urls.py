from django.urls import include, path
from rest_framework.routers import DefaultRouter

from orders import views as order_views


app_name = 'orders'
router = DefaultRouter()

router.register("items", order_views.ItemsViewSets)

urlpatterns = [
    path("", order_views.CreatePurchaseOrders.as_view(), name="purchase-orders"),
    path("<str:po_number>/acknowledgement/", order_views.OrderAcknowledgementView.as_view(), name="order-acknowledgement"),
    path("<str:po_number>", order_views.PurchaseOrdersViews.as_view(), name="purchase-orders-details"),
    path("", include(router.urls)),
]