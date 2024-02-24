
from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.main, name='main'),
    path('peshang/', include('peshang_petrol.urls')),
    path('bodybuilding/', include('body_building.urls')),
    path('awat/', include('awat_petrol.urls')),
]
