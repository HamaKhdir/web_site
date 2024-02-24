from django.urls import path
from . import views

app_name = 'body_building' 
urlpatterns = [
    path('',views.loginPage,name='login'),
]