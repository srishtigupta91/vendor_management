from django.urls import include, path
from rest_framework.routers import DefaultRouter

from vendor import views as vendor_views


app_name = 'vendor'
router = DefaultRouter()

router.register("", vendor_views.VendorModelViewSets)

urlpatterns = [
    path("<int:vendor_id>/performance/", vendor_views.VendorPeformanceMatrics.as_view(), name="vendor-performance"),
    path("", include(router.urls)),

]