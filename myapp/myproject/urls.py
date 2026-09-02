from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path("admin/", admin.site.urls),
    path("index/", home),
    path("about/", about),
    path("services/", services),
    path("emp/", include("emp.urls")),
]