from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('api/v1/manage-sheet/', include('sheets.apis.urls', namespace="apisheets")),
    path('admin/', admin.site.urls),
]