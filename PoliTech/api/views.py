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

# class DistrictCreateView(generics.ListCreateAPIView):
#     queryset = District.objects.all()
#     serializer_class = DistrictSerializer
#
#     def create(self, request, *args, **kwargs):
#         write_serializer = DistrictSerializer(data=request.data)
#         write_serializer.is_valid(raise_exception=True)
#         instance = self.perform_create(write_serializer)
#         read_serializer = DistrictSerializer(instance)
#         return JsonResponse(read_serializer.data)
#
# class AdjacencyTypeCreateView(generics.ListCreateAPIView):
#     queryset = AdjacencyType.objects.all()
#     serializer_class = AdjacencyType
#
#     def create(self, request, *args, **kwargs):
#         write_serializer = AdjacencyTypeSerializer(data=request.data)
#         write_serializer.is_valid(raise_exception=True)
#         instance = self.perform_create(write_serializer)
#         read_serializer = AdjacencyTypeSerializer(instance)
#         return JsonResponse(read_serializer.data)
#
# class DemographicTypeCreateView(generics.ListCreateAPIView):
#     queryset = DemographicType.objects.all()
#     serializer_class = DemographicType
#
#     def create(self, request, *args, **kwargs):
#         write_serializer = DemographicTypeSerializer(data=request.data)
#         write_serializer.is_valid(raise_exception=True)
#         instance = self.perform_create(write_serializer)
#         read_serializer = DemographicTypeSerializer(instance)
#         return JsonResponse(read_serializer.data)
#
# class DemographicCreateView(generics.ListCreateAPIView):
#     queryset = Demographic.objects.all()
#     serializer_class = Demographic
#
#     def create(self, request, *args, **kwargs):
#         write_serializer = DemographicSerializer(data=request.data)
#         write_serializer.is_valid(raise_exception=True)
#         instance = self.perform_create(write_serializer)
#         read_serializer = DemographicSerializer(instance)
#         return JsonResponse(read_serializer.data)
#
# class AdjacencyCreateView(generics.ListCreateAPIView):
#     queryset = Adjacency.objects.all()
#     serializer_class = Adjacency
#
#     def create(self, request, *args, **kwargs):
#         write_serializer = AdjacencySerializer(data=request.data)
#         write_serializer.is_valid(raise_exception=True)
#         instance = self.perform_create(write_serializer)
#         read_serializer = AdjacencySerializer(instance)
#         return JsonResponse(read_serializer.data)
#
# class PrecinctCreateView(generics.ListCreateAPIView):
#     queryset = Precinct.objects.all()
#     serializer_class = Precinct
#
#     def create(self, request, *args, **kwargs):
#         write_serializer = PrecinctSerializer(data=request.data)
#         write_serializer.is_valid(raise_exception=True)
#         instance = self.perform_create(write_serializer)
#         read_serializer = PrecinctSerializer(instance)
#         return JsonResponse(read_serializer.data)