from django.urls import path
from . import views

urlpatterns = [
    path("", views.strings_root, name="strings_root"),
    path("<str:string_value>/", views.get_or_delete_string, name="get_string"),
]
