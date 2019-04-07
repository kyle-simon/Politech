from django.shortcuts import render
from rest_framework import generics
from .models import District
from .serializers import DistrictSerializer
from django.http import JsonResponse


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













