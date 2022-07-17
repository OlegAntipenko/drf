"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path

from first import views
from first.urls import router as first_router
from first.urls import router2 as mystore_router
from first.urls import router3 as admin_router


urlpatterns = [
    path('admin/', admin.site.urls),
    path('hello/', views.hello_world),
    path('my_name/', views.my_name),
    path('today/', views.today),
    path('calculator/', views.calculator),
    path('store/', views.StoreApiView.as_view()),
    path('auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
    path('viewsetstore/', include(first_router.urls)),
    path('my_store/', include(mystore_router.urls)),
    path('admin_store/', include(admin_router.urls)),

]

