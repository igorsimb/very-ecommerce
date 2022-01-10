from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from ecommerce.drf import views as drf_views

router = routers.DefaultRouter()
router.register(
    r'api', viewset=drf_views.AllProductsViewset, basename='allproducts'
)

router.register(
    r'product/(?P<slug>[^/.]+)', viewset=drf_views.ProductInventoryViewset, basename='products'
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('demo/', include('ecommerce.demo.urls', namespace='demo')),
    path('', include(router.urls))
]
