from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import generics
from .models import District
from .serializers import DistrictSerializer
from django.http import JsonResponse
from PoliTech.api.serializers import *

class EconomicListCreateView(generics.ListCreateAPIView):
    queryset = EconomicData.objects.all()
    serializer_class = EconomicDataSerializer

    def create(self, request, *args, **kwargs):
        write_serializer = EconomicDataSerializer(data=request.data)
        write_serializer.is_valid(raise_exception=True)
        instance = self.perform_create(write_serializer)
        read_serializer = EconomicDataSerializer(instance)
        return JsonResponse(read_serializer.data)

class VoteCountCreateView(generics.ListCreateAPIVIEW):
    queryset = VoteCount.objects.all()
    serializer_class = VoteCountSerializer

    def create(self, request):
        write_serializer = VoteCountSerializer(data=request.data)
        write_serializer.is_valid(raise_exception=True)
        instance = self.perform_create(write_serializer)

        read_serializer = VoteCountSerializer(instance)

        return JsonResponse(read_serializer.data)

#
# class districtCreateView(generics.ListCreateAPIVIEW):
#     queryset = District.objects.all()
#     serializer_class = DistrictSerializer
#
#     def create(self, request):
#         write_serializer = DistrictSerializer(data=request.data)
#         write_serializer.is_valid(raise_exception=True)
#         instance = self.perform_create(write_serializer)
#
#         read_serializer = DistrictSerializer(instance)
#
#         return JsonResponse(read_serializer.data)
#
#
#
# class DemographicTypePopulationCreateView(generics.ListCreateAPIVIEW):
#     queryset = DemographicTypePopulation.objects.all()
#     serializer_class = DemographicTypePopulationSerializer
#
#     def create(self, request):
#         write_serializer = DemographicTypePopulationSerializer(data=request.data)
#         write_serializer.is_valid(raise_exception=True)
#         instance = self.perform_create(write_serializer)
#
#         read_serializer = DemographicTypePopulationSerializer(instance)
#
#         return JsonResponse(read_serializer.data)


#
#
# class PoliticalPartyCreateView(generics.ListCreateAPIVIEW):
#     queryset = PoliticalParty.objects.all()
#     serializer_class = PoliticalPartySerializer
#
#     def create(self, request):
#         write_serializer = PoliticalPartySerializer(data=request.data)
#         write_serializer.is_valid(raise_exception=True)
#         instance = self.perform_create(write_serializer)
#
#         read_serializer = PoliticalPartySerializer(instance)
#
#         return JsonResponse(read_serializer.data)
#
#
#
# class ElectionResultCreateView(generics.ListCreateAPIVIEW):
#     queryset = ElectionResult.objects.all()
#     serializer_class = ElectionResultSerializer
#
#     def create(self, request):
#         write_serializer = ElectionResultSerializer(data=request.data)
#         write_serializer.is_valid(raise_exception=True)
#         instance = self.perform_create(write_serializer)
#
#         read_serializer = ElectionResultSerializer(instance)
#
#         return JsonResponse(read_serializer.data)


# class DistrictMembershipCreateView(generics.ListCreateAPIVIEW):
#         queryset = DistrictMembership.objects.all()
#         serializer_class = DistrictMembershipSerializer
#
#         def create(self, request):
#             write_serializer = DistrictMembershipSerializer(data=request.data)
#             write_serializer.is_valid(raise_exception=True)
#             instance = self.perform_create(write_serializer)
#
#             read_serializer = DistrictMembershipSerializer(instance)
#
#             return JsonResponse(read_serializer.data)