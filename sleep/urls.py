from django.urls import path
from . import views

urlpatterns = [
    path('', views.sleep_list, name='sleep_list'),
    path('add/', views.add_record, name='add_record'),
]