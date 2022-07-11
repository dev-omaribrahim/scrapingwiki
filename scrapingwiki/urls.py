from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('manage-sheet/', include('sheets.urls', namespace="sheets")),
    path('api/v1/manage-sheet/', include('sheets.apis.urls', namespace="apisheets")),
    path('admin/', admin.site.urls),
]