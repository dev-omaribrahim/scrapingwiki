from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.renderers import TemplateHTMLRenderer, BrowsableAPIRenderer, JSONRenderer, StaticHTMLRenderer
from rest_framework.response import Response
from rest_framework import status
from .serializers import ExcelDataSerializer
from sheets.utils.shortcuts import (
    get_excel_data_or_none, search_value_in_column,
    file_is_exist, get_current_sheet, get_current_file
)
import pandas as pd
import openpyxl
import os
import json


file_path = os.path.join(settings.BASE_DIR, "excel_files/data.xlsx")
file = openpyxl.load_workbook(file_path)
current_sheet = file.active


class ExcelListCreateAPIView(APIView):

    renderer_classes = (BrowsableAPIRenderer, JSONRenderer, TemplateHTMLRenderer)

    def get(self, request, pk=None):

        if file_is_exist(file_path):
            excel_data = get_excel_data_or_none(file_path)

            return Response(
                {"data": excel_data}, status=status.HTTP_200_OK,
            )

        else:
            return Response(
                "File Not Found !",
                status=status.HTTP_404_NOT_FOUND
            )

    def post(self, request):

        if file_is_exist(file_path):
            requested_data = request.data
            serializer = ExcelDataSerializer(data=requested_data)
            if serializer.is_valid():

                # current_sheet = get_current_sheet(file_path)
                last_row = current_sheet.max_row + 1
                current_sheet["A" + str(last_row)].value = requested_data["ranking"]
                current_sheet["B" + str(last_row)].value = requested_data["novel"]
                current_sheet["C" + str(last_row)].value = requested_data["author"]
                current_sheet["D" + str(last_row)].value = requested_data["country"]
                current_sheet["E" + str(last_row)].value = requested_data["novel_link"]
                current_sheet["F" + str(last_row)].value = requested_data["author_link"]
                current_sheet["G" + str(last_row)].value = requested_data["country_link"]

                file.save(file_path)
                file.close()

                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:

                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(
                "File Not Found !",
                status=status.HTTP_404_NOT_FOUND
            )


class ExcelDetailAPIView(APIView):

    def get(self, request, index):

        if file_is_exist(file_path):
            excel_data = get_excel_data_or_none(file_path)

            try:
                data = excel_data[index]

                return Response(
                    {"data": data},
                    status=status.HTTP_200_OK
                )

            except KeyError:
                return Response("Record Not Found !", status=status.HTTP_404_NOT_FOUND)

        else:
            return Response(
                "File Not Found !",
                status=status.HTTP_404_NOT_FOUND
            )

    def put(self, request, index):

        requested_data = request.data

        if file_is_exist(file_path):

            serializer = ExcelDataSerializer(data=requested_data)

            if serializer.is_valid():

                excel_data = get_excel_data_or_none(file_path)
                ranking = str(int(excel_data[index]["الترتيب"]))
                row_number = search_value_in_column(current_sheet, ranking, column="A")

                if row_number:

                    current_sheet["A" + str(row_number)] = requested_data["ranking"]
                    current_sheet["B" + str(row_number)] = requested_data["novel"]
                    current_sheet["C" + str(row_number)] = requested_data["author"]
                    current_sheet["D" + str(row_number)] = requested_data["country"]
                    current_sheet["E" + str(row_number)] = requested_data["novel_link"]
                    current_sheet["F" + str(row_number)] = requested_data["author_link"]
                    current_sheet["G" + str(row_number)] = requested_data["country_link"]

                    file.save(file_path)
                    file.close()

                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                else:
                    return Response("Row Not Found !", status=status.HTTP_404_NOT_FOUND)

            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(
                "File Not Found !",
                status=status.HTTP_404_NOT_FOUND
            )

    def delete(self, request, index):

        if file_is_exist(file_path):

            excel_data = get_excel_data_or_none(file_path)
            ranking = str(int(excel_data[index]["الترتيب"]))

            row_number = search_value_in_column(current_sheet, ranking, column="A")

            if row_number:
                current_sheet.delete_rows(row_number)

                file.save(file_path)
                file.close()

                return Response("Deleted", status=status.HTTP_204_NO_CONTENT)
            else:
                return Response("Row Not Found !", status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(
                "File Not Found !",
                status=status.HTTP_404_NOT_FOUND
            )


def create_excel(request):
    pass


def create_google_sheet(request):
    import requests
    import pandas as pd
    from bs4 import BeautifulSoup as bs
    import pygsheets

    domain = 'https://ar.wikipedia.org'

    url = "https://ar.wikipedia.org/wiki/%D9%82%D8%A7%D8%A6%D9%85%D8%A9_%D8%A3%D9%81%D8%B6%D9%84_%D9%85%D8%A6%D8%A9_%D8%B1%D9%88%D8%A7%D9%8A%D8%A9_%D8%B9%D8%B1%D8%A8%D9%8A%D8%A9"

    response = requests.get(url)

    soup = bs(response.content, features='html.parser')

    table = soup.select('table.wikitable')[0]

    columns = [i.get_text(strip=True) for i in table.find_all("th")]

    columns += ["رابط الكتاب", "رابط المؤلف", "رابط البلد"]

    data = []

    for tr in table.find("tbody").find_all("tr"):
        cells = []
        tds = tr.find_all('td')
        link = []

        for td in tds:
            cells.append(td.get_text(strip=True))
            if td.find('a'):
                link.append(domain + td.find('a')['href'])
        data.append(cells + link)

    df = pd.DataFrame(data, columns=columns)

    gc = pygsheets.authorize(service_file=os.path.join(settings.BASE_DIR, "best-100-novel-a99af0da7cee.json"))
    # print("===> gd:", gc.spreadsheet_titles())
    sh = gc.open('test')
    wks = sh[0]
    wks.set_dataframe(df, start=(1, 1))

    return HttpResponse("ok")
