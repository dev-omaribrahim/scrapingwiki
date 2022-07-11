# from django.urls import path
# from .apis import views as apiviews
# from . import views
#
# app_name = "sheets"
#
# urlpatterns = [
#
#     # api views
#     path("", apiviews.ExcelListCreateAPIView.as_view(), name="ExcelListCreateAPIView"),
#     path("create/", apiviews.create_google_sheet, name="create_google_sheet"),
#     path("<int:index>/", apiviews.ExcelDetailAPIView.as_view(), name="ExcelDetailAPIView"),
#
# ]