from django.urls import path
from . import views


app_name = "covers_generator"


urlpatterns = [
    path("", views.generate_covers, name="generate_covers"),
]