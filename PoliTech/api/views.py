import json

from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import generics, viewsets
from rest_framework.decorators import action
from .models import *
from .serializers import *
from datetime import date
from django.db.models import Q, F, Max, OuterRef, Subquery
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)
from rest_framework.response import Response

from .constants import STATES

# @api_view()
# def getState(state, year):

# For the token generation:
@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def login(request):
    username = request.data.get("username")
    password = request.data.get("password")
    if username is None or password is None:
        return Response({'error': 'Please provide both username and password'},
                        status=HTTP_400_BAD_REQUEST)
    user = authenticate(username=username, password=password)
    if not user:
        return Response({'error': 'Invalid Credentials'},
                        status=HTTP_404_NOT_FOUND)
    token, _ = Token.objects.get_or_create(user=user)
    return Response({'token': token.key},
                    status=HTTP_200_OK)


class EconomicViewSet(viewsets.ModelViewSet):
    queryset = EconomicData.objects.all()
    serializer_class = EconomicDataSerializer


class VoteCountViewSet(viewsets.ModelViewSet):
    queryset = VoteCount.objects.all()
    serializer_class = VoteCountSerializer


class AdjacencyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Adjacency.objects.all()
    serializer_class = AdjacencySerializer
    @action(detail=False, methods=['POST'])
    def bulk_create(self, request):
        serializer=AdjacencySerializer(data=request.data, many=True)
        print(request.data)
        if serializer.is_valid():
            # new_adjacencies = serializer.create(validated_data=request.data)
            i = 0
            res = {}
            for elem in request.data:
                from_pre = Precinct.objects.get(id=elem["from_precinct"])
                to_pre = Precinct.objects.get(id=elem["to_precinct"])
                data = from_pre.add_adjacency(to_pre)
                res[i] = data
                i = i + 1
                # data={"from_precinct":from_pre, "to_precinct":to_pre}

                # print(type(data))
                # adj = serializer.create(validated_data=data)
            print(res)
            # print(json.dumps(request.data, indent=4))
            serializer.save()
            # return a list of tuples that looks like [(pk, description), (pk, description),..]\
            # list(new_precincts.map(lambda p: (p.pk, p.description)))
            return Response(data="", status=HTTP_200_OK)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

class AdjacencyTypeViewSet(viewsets.ModelViewSet):
    queryset = AdjacencyType.objects.all()
    serializer_class = AdjacencyTypeSerializer

class PrecinctViewSet(viewsets.ModelViewSet):
    queryset = Precinct.objects.all()
    serializer_class = PrecinctSerializer

    @action(detail=False, methods=['POST'])
    def bulk_create(self, request):
        serializer=PrecinctSerializer(data=request.data, many=True)
        if serializer.is_valid():
            new_precincts = serializer.save()
            # return a list of tuples that looks like [(pk, description), (pk, description),..]
            res=map(lambda p: (p.pk, p.description), new_precincts)
            print(res)
            return Response(data=res, status=HTTP_200_OK)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

class DistrictViewSet(viewsets.ModelViewSet):
    queryset = District.objects.all()
    serializer_class = DistrictSerializer

    @action(detail=False, methods=['GET'], url_path='state/')
    def state(self, request):
        state = None
        year = date.today()
        include_economic_data = None
        include_election_result_data = None
        include_demographic_data = None

        if 'state' not in request.query_params:
            return Response(status=HTTP_400_BAD_REQUEST)
        state = request.query_params['state']

        if state not in STATES:
            return Response(status=HTTP_400_BAD_REQUEST)

        if 'year' in request.query_params:
            try:
                year = date.fromisoformat(request.query_params['year'])
            except:
                return Response(status=HTTP_400_BAD_REQUEST)

        if 'include_economic_data' in request.query_params:
            if request.query_params['include_economic_data'] not in ('True', 'False'):
                return Response(status=HTTP_400_BAD_REQUEST)
            include_economic_data = request.query_params['include_economic_data'] == 'True'

        if 'include_demographic_data' in request.query_params:
            if request.query_params['include_demographic_data'] not in ('True', 'False'):
                return Response(status=HTTP_400_BAD_REQUEST)
            include_demographic_data =request.query_params['include_demographic_data'] == 'True'

        if 'include_election_result_data' in request.query_params:
            if request.query_params['include_election_result_data'] not in ('True', 'False'):
                return Response(status=HTTP_400_BAD_REQUEST)
            include_election_result_data = request.query_params['include_election_result_data'] == 'True'

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
                                                .annotate(_sel=Max('precinct__economics__year')) \
                                                .filter(year=F('_sel'))

        if include_election_result_data:
            election_result_data = ElectionResult.objects.filter(Q(precinct__in=precincts_in_district) & Q(election_year__lte=year)) \
                                                         .annotate(_sel=Max('precinct__vote_counts__election_year')) \
                                                         .filter(election_year='sel')
        if include_demographic_data:
            demographic_data = Demographic.objects.filter(Q(precinct__in=precincts_in_district) & Q(year__lte=year)) \
                                                  .annotate(_sel= Max('precinct__demographics__year')) \
                                                  .filter(year=F('_sel'))

        state = State(state, districts_in_state, adjacencies_in_state, economic_data, demographic_data, election_result_data)

        serializer = StateSerializer(state)

        return JsonResponse(serializer.data)
