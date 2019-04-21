from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import generics, viewsets
from rest_framework.decorators import action
from .models import *
from .serializers import *
from datetime import date
from django.db.models import Q, F
from .constants import STATES

# @api_view()
# def getState(state, year):



class EconomicViewSet(viewsets.ModelViewSet):
    queryset = EconomicData.objects.all()
    serializer_class = EconomicDataSerializer


class VoteCountViewSet(viewsets.ModelViewSet):
    queryset = VoteCount.objects.all()
    serializer_class = VoteCountSerializer


class AdjacencyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Adjacency.objects.all()
    serializer_class = AdjacencySerializer

class AdjacencyTypeViewSet(viewsets.ModelViewSet):
    queryset = AdjacencyType.objects.all()
    serializer_class = AdjacencyTypeSerializer

class DistrictViewSet(viewsets.ModelViewSet):
    queryset = District.objects.all()
    serializer_class = DistrictSerializer

    @action(detail=True, methods=['GET'])
    def state(self, request, state, year=date.today(), include_economic_data=False,
             include_election_result_data=False, include_demographic_data=False):
        districts_in_state = District.objects.filter(Q(state=state) 
                                                    & Q(precincts__DistrictMembership__from_year__gte=year) 
                                                    & (Q(precincts__DistrictMembership__to_year__lt=year) | Q(precincts__DistrictMembership__to_year__isnull=True)))

        precincts_in_district = list(districts_in_state.values('precincts'))

        # Only grab precinct where from_precinct < to_precinct, this will make it so we don't grab reverse relationships
        adjacencies_in_district = Adjacency.objects.filter((Q(from_precinct__in=precincts_in_district) | Q(to_precinct__in=precincts_in_district)) 
                                                           & Q(from_precinct__pk__lt=F('to_precinct')))

        economic_data = None
        election_result_data = None
        demographic_data = None

        if include_economic_data:
            # grab economic data from the most recent year

            economic_data = EconomicData.objects.filter(Q(precinct__in=precincts_in_district) & Q(year__lte=year)) \
                                                .order_by('pk', '-year') \
                                                .distinct('pk')
        if include_election_result_data:
            election_result_data = ElectionResult.objects.filter(Q(precinct__in=precincts_in_district) & Q(election_year__lte=year)) \
                                                         .order_by('pk', '-election_year') \
                                                         .distinct('pk')
        if include_demographic_data:
            demographic_data = Demographic.objects.filter(Q(precinct__in=precincts_in_district) & Q(year__lte=year)) \
                                                  .order_by('pk', '-year') \
                                                  .distinct('pk')

        state = State(state, districts_in_state, adjacencies_in_state, economic_data, demographic_data, election_result_data)

        serializer = StateSerializer(state)

        return JsonResponse(serializer.data)



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
#
# class districtCreateView(generics.ListCreateAPIVIEW):
#     queryset = District.objects.all()
#     serializer_class = DistrictSerializer
#
#     def create(self, request):
#         write_serializer = DistrictSerializer(data=request.data)
#         write_serializer.is_valid(raise_exception=True)
#         instance = self.perform_create(write_serializer)
#         read_serializer = DistrictSerializer(instance)
#         return JsonResponse(read_serializer.data)
#
# class DemographicTypePopulationCreateView(generics.ListCreateAPIVIEW):
#     queryset = DemographicTypePopulation.objects.all()
#     serializer_class = DemographicTypePopulationSerializer
#
#     def create(self, request):
#         write_serializer = DemographicTypePopulationSerializer(data=request.data)
#         write_serializer.is_valid(raise_exception=True)
#         instance = self.perform_create(write_serializer)
#         read_serializer = DemographicTypePopulationSerializer(instance)
#         return JsonResponse(read_serializer.data)
#
# class PoliticalPartyCreateView(generics.ListCreateAPIVIEW):
#     queryset = PoliticalParty.objects.all()
#     serializer_class = PoliticalPartySerializer
#
#     def create(self, request):
#         write_serializer = PoliticalPartySerializer(data=request.data)
#         write_serializer.is_valid(raise_exception=True)
#         instance = self.perform_create(write_serializer)
#         read_serializer = PoliticalPartySerializer(instance)
#         return JsonResponse(read_serializer.data)
#
# class ElectionResultCreateView(generics.ListCreateAPIVIEW):
#     queryset = ElectionResult.objects.all()
#     serializer_class = ElectionResultSerializer
#
#     def create(self, request):
#         write_serializer = ElectionResultSerializer(data=request.data)
#         write_serializer.is_valid(raise_exception=True)
#         instance = self.perform_create(write_serializer)
#         read_serializer = ElectionResultSerializer(instance)
#         return JsonResponse(read_serializer.data)
#
# class DistrictMembershipCreateView(generics.ListCreateAPIVIEW):
#         queryset = DistrictMembership.objects.all()
#         serializer_class = DistrictMembershipSerializer
#
#         def create(self, request):
#             write_serializer = DistrictMembershipSerializer(data=request.data)
#             write_serializer.is_valid(raise_exception=True)
#             instance = self.perform_create(write_serializer)
#             read_serializer = DistrictMembershipSerializer(instance)
#             return JsonResponse(read_serializer.data)
