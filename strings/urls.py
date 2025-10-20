from django.urls import path
from . import views

urlpatterns = [
    path("", views.get_string, name="get_string"),
]
