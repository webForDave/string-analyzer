# urls.py (Corrected)

from django.urls import path
from . import views

urlpatterns = [
    path('strings/filter-by-natural-language/', views.natural_language_filter_view, name='string-nl-filter'),
    path('strings/', views.strings_root, name="strings_root"),
    path('strings/<str:string_value>/', views.get_or_delete_string, name="get_string"),
]