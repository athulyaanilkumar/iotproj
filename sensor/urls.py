from django.urls import path
from .views import predict_exceed_time_view

urlpatterns = [
    path('', predict_exceed_time_view, name='home'),
]