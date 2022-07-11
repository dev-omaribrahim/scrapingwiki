from django.urls import path
from . import views as apiviews

app_name = "apisheets"

urlpatterns = [

    # api views
    path("", apiviews.ExcelListCreateAPIView.as_view(), name="ExcelListCreateAPIView"),
    path("create/", apiviews.create_google_sheet, name="create_google_sheet"),
    path("<int:index>/", apiviews.ExcelDetailAPIView.as_view(), name="ExcelDetailAPIView"),

]