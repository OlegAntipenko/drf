from django.urls import path, include
from rest_framework import routers
from first.views import StoreViewSet, StoreUserViewSet, AdminStoreViewSet

router = routers.SimpleRouter()
router.register('', StoreViewSet, basename='stores')
router2 = routers.SimpleRouter()
router2.register('', StoreUserViewSet, basename='my_store')
router3 = routers.SimpleRouter()
router3.register('', AdminStoreViewSet, basename='adminstore')
