from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView


urlpatterns = [
    path("", TemplateView.as_view(template_name="index.html")),
    path('manage-sheet/', include('sheets.urls', namespace="sheets")),
    path('api/v1/manage-sheet/', include('sheets.apis.urls', namespace="apisheets")),
    path('covers/generators/', include('covers_generator.urls', namespace="covers_generator")),
    path('admin/', admin.site.urls),
]