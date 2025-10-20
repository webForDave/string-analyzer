from django.urls import path
from . import views

urlpatterns = [
    path("", views.analyze_string, name="analyze_string"),
    path("<str:string_value>", views.get_string, name="get_string"),
]
