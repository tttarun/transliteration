import json
from io import StringIO


from django.http import FileResponse
from django.shortcuts import render
from rest_framework import mixins, viewsets, views
from rest_framework.templatetags.rest_framework import data

from .models import (
    Endpoint,
    MLAlgorithm,
    MLRequest,
    EnglishToHindiTranslation,
    myuploadfile,
)
from .serializers import (
    MLAlgorithmSerializer,
    EndpointSerializer,
    MLRequestSerializer,
    PersonDataSerialzer,
)
from .machine_learning_models.translate_model import Translate
from rest_framework.response import Response
from .authentication import APIAuthentication
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView  # for api
from rest_framework import viewsets
from rest_framework import status
from datetime import datetime
from pytz import timezone
from django.views import View
from openpyxl import load_workbook
from openpyxl.writer.excel import save_virtual_workbook
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from .serializers import UploadSerializer
from django.shortcuts import render, HttpResponse, redirect
from django.core.files import File
from .forms import MyuploadfileForm
from django.core.cache import cache
from django.http import JsonResponse


# Create your views here.


class Home(View):
    def get(self, request):
        return render(request, "translation/home.html")


class EndpointView(
    mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet
):
    """View to get all the available endpoints"""

    queryset = Endpoint.objects.all()
    serializer_class = EndpointSerializer
    authentication_classes = (APIAuthentication,)


class MLAlgoirthmView(
    mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet
):
    """View to get all the available algorithms"""

    queryset = MLAlgorithm.objects.all()
    serializer_class = MLAlgorithmSerializer
    authentication_classes = (APIAuthentication,)


class MLRequestView(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
    mixins.UpdateModelMixin,
):
    """View to get all the successful request history"""

    queryset = MLRequest.objects.all()
    serializer_class = MLRequestSerializer
    authentication_classes = (APIAuthentication,)


class TranslateView(views.APIView):
    """View to get the translation from english to hindi"""

    authentication_classes = (APIAuthentication,)

    def post(self, request, endpoint):
        algorithm = MLAlgorithm.objects.filter(
            parent_endpoint__name__iexact=endpoint
        ).first()
        if not algorithm:
            return Response(
                {"status": "Error", "Error": "Given Endpoint Does Not Exists"},
                status=404,
            )
        serializer = PersonDataSerialzer(data=request.data)
        if serializer.is_valid():
            data = dict()
            translate_obj = Translate()
            for key in serializer.validated_data:
                data_to_translated = serializer.validated_data.get(key)
                if data_to_translated:
                    translated_data = translate_obj.convert(data_to_translated)
                    data[key] = translated_data
                    mlrequest = MLRequest(
                        input_data=json.dumps(data_to_translated),
                        full_response=json.dumps(translated_data),
                        response=json.dumps(translated_data),
                        feedback="",
                        parent_mlalgorithm=algorithm,
                    )
                    mlrequest.save()
            return Response(data)
        else:
            return Response({"message": "Invalid data"}, status=400)



class TranslateStringView(views.APIView):

    def get(self, request):
        word = request.query_params.get('query')
        # print(word) # in word we are getting english word
        data = {}
        if cache.get(word):
            data=cache.get(word)

            # print(possible_match)
        else:
            possible_match = EnglishToHindiTranslation.objects.filter(english__iexact=word).first()
            if possible_match is not None and possible_match.hindi != {}:
                data = possible_match.hindi  #{'संदिप': 61, 'संदीप': 9615, 'सन्दीप': 414} getting this as data for every word
                # print(data)
                for i in data:
                    # print(i) # in data[i] we are getting score and in i we are getting word
                    if isinstance(data[i], int):
                        ind_time = datetime.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M')
                        score=data[i]
                        data[i] = {'manual': False, 'score': score, 'time': ind_time}
                if len(data) < 5:
                    translate_obj = Translate()
                    converted_word_array = translate_obj.hin_translate(word)
                    for i in converted_word_array:
                        if len(data) >= 5:
                            break
                        if i in data.keys():
                            continue
                        else:
                            data.__setitem__(i, {'manual': False, 'score': 10, 'time': ind_time})

            else:
                translate_obj = Translate()
                converted_word_array = translate_obj.hin_translate(word)

                for i in range(len(converted_word_array)):
                    if len(data) >= 5:
                        break
                    ind_time = datetime.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M')
                    data.__setitem__(converted_word_array[i], {'manual': False, 'score': 10, 'time': ind_time})

            data = sorted(data, key=lambda x: (data[x]['manual'], data[x]['score'], data[x]['time']),reverse=True)
            cache.add(word,data)
        return Response({'status': 'Success', 'data': data}, status=200)






# class TranslateStringView(views.APIView):
#
#     def get(self, request):
#         word = request.query_params.get('query')
#         # print(word) # in word we are getting english word
#         possible_match = EnglishToHindiTranslation.objects.select_related(english__iexact=word).first()
#         # print(possible_match)
#         data = {}
#         if possible_match is not None and possible_match.hindi != {}:
#             data = possible_match.hindi  #{'संदिप': 61, 'संदीप': 9615, 'सन्दीप': 414} getting this as data for every word
#             # print(data)
#             for i in data:
#                 # print(i) # in data[i] we are getting score and in i we are getting word
#                 if isinstance(data[i], int):
#                     ind_time = datetime.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M')
#                     score=data[i]
#                     data[i] = {'manual': False, 'score': score, 'time': ind_time}
#             if len(data) < 5:
#                 translate_obj = Translate()
#                 converted_word_array = translate_obj.hin_translate(word)
#                 for i in converted_word_array:
#                     if len(data) >= 5:
#                         break
#                     if i in data.keys():
#                         continue
#                     else:
#                         data.__setitem__(i, {'manual': False, 'score': 10, 'time': ind_time})
#
#         else:
#             translate_obj = Translate()
#             converted_word_array = translate_obj.hin_translate(word)
#
#             for i in range(len(converted_word_array)):
#                 if len(data) >= 5:
#                     break
#                 ind_time = datetime.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M')
#                 data.__setitem__(converted_word_array[i], {'manual': False, 'score': 10, 'time': ind_time})
#
#         data = sorted(data, key=lambda x: (data[x]['manual'], data[x]['score'], data[x]['time']),reverse=True)
#
#         return Response({'status': 'Success', 'data': data}, status=200)

class SearchAndUpdateAPIView(APIView):
    def post(self, request):

        data = request.data

        for key in data:
            record = EnglishToHindiTranslation.objects.filter(
                english__iexact=key
            ).first()
            if record:
                record.hindi = data[key]
                record.save()
            else:
                add_new = EnglishToHindiTranslation.objects.create(
                    english=key, hindi=data[key]
                )

        return Response(
            {"status": "Success", "message": "Saved Successfully"}, status=200
        )


class ExcelFileTranslate(views.APIView):
    # def get(self,request):
    # #     data=request.data
    # #     data=json.dumps(data)
    #     word = request.query_params.get('query')
    #     return Response({'status': 'Success', 'data': word}, status=200)

    def post(self, request):
        # data = request.data
        # data = json.dumps(data)
        translate_obj = Translate()
        translated_data = translate_obj.excel_english_to_hindi()
        return Response({"status": "Success", "data": data}, status=200)


# from django.views.decorators.csrf import csrf_exempt
#
# @csrf_exempt
class send_files(views.APIView):
    def post(self, request):
        name = request.POST.get("f_name")
        myfile = request.FILES["uploaded_file"]

        print(name)
        print(myfile)
        translate_obj = Translate()

        translated_data = translate_obj.excel_english_to_hindi(myfile)
        now = datetime.now()
        translated_data.to_excel("media/{}_{}.xlsx".format(name, now), index=False)
        myuploadfile(
            f_name=name,
            uploaded_file=myfile,
            translated_file="{}_{}.xlsx".format(name, now),
        ).save()

        response = FileResponse(open("media/{}_{}.xlsx".format(name, now), "rb"))
        return response
        # return Response({"status": "Success", "data": 'my name is sandeep kumar kohli'}, status=200)




#
# class send_files(views.APIView):
#     def post(self, request):
#
#         name = request.POST.get("filename")
#         myfile = request.FILES.getlist("uploadfiles")
#
#         for f in myfile:
#             # name=f.filename
#             # print(name)
#             translate_obj = Translate()
#
#             translated_data = translate_obj.excel_english_to_hindi(f)
#             now = datetime.now()
#             translated_data.to_excel("media/{}_{}.xlsx".format(name, now), index=False)
#
#             myuploadfile(
#                 f_name=name,
#                 uploaded_file=f,
#                 translated_file="{}_{}.xlsx".format(name, now),
#             ).save()
#
#         response = FileResponse(open("media/{}_{}.xlsx".format(name, now), "rb"))
#
#         # return response
#         return Response({"status": "Success", "data": 'my name is sandeep kumar kohli'}, status=200)
#
