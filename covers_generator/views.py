from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse
from .generate_covers_tool import generate_books_cover
import os


file_path = os.path.join(settings.BASE_DIR, "excel_files/data.xlsx")


def generate_covers(request):
    """
    Generate Cover For Each Book
    """
    generate_books_cover(excel_path=file_path)
    return HttpResponse("Generated !")

