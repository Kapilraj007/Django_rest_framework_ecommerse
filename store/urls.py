from django.urls import path
from django.urls.conf import include
from rest_framework_nested import routers
from . import views

router = routers.DefaultRouter()

router.register('customers',views.CustomerViewSet)
router.register('products',views.ProductViewSet)
router.register('collections',views.CollectionViewSet)
router.register('orders',views.OrderViewSet,basename='orders')


urlpatterns = router.urls