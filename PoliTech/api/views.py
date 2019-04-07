from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import generics
from .models import District
from .serializers import DistrictSerializer
from django.http import JsonResponse
from PoliTech.api.serializers import *
# Create your views here.
# def index(request):
#     data =

class EconomicListCreateView(generics.ListCreateAPIView):
    queryset = EconomicData.objects.all()
    serializer_class = EconomicDataSerializer

    def create(self, request, *args, **kwargs):
        write_serializer = EconomicDataSerializer(data=request.data)
        write_serializer.is_valid(raise_exception=True)
        instance = self.perform_create(write_serializer)
        read_serializer = EconomicDataSerializer(instance)
        return JsonResponse(read_serializer.data)

# Create your views here.
# def index(request):

class districtCreateView(generics.ListCreateAPIVIEW):
    queryset = District.objects.all()
    serializer_class = DistrictSerializer

    def create(self, request):
        write_serializer = DistrictSerializer(data=request.data)
        write_serializer.is_valid(raise_exception=True)
        instance = self.perform_create(write_serializer)

        read_serializer = DistrictSerializer(instance)

        return JsonResponse(read_serializer.data)
