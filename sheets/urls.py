from django.urls import path
from . import views

app_name = "sheets"

urlpatterns = [
    # views
    path("create/excel-sheet/", views.create_excel, name="crete_excel"),
    path("create/google-sheet/", views.create_google_sheet, name="create_google_sheet"),

]