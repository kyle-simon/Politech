from rest_framework import serializers
from django.contrib.gis.db import models
from rest_framework_gis.fields import GeometryField
from .models import *


class AdjacencyTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdjacencyType
        fields = ('description')


class AdjacencySerializer(serializers.ModelSerializer):
    from_precinct = PrecinctSerializer(read_only=True)
    to_precinct = PrecinctSerializer(read_only=True)
    class Meta:
        model = Adjacency
        fields = ('from_precinct', 'to_precinct', 'adjacency_types')

class PrecinctSerializer(serializers.ModelSerializer):
    adjacencies = AdjacencySerializer(many=True, read_only=True)

    class Meta:
        model = Precinct
        fields = ('precinct_shape', 'state', 'description', 'adjacencies')


class DemographicTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DemographicType
        fields = ('description')


class DemographicSerializer(serializers.ModelSerializer):
    precinct = serializers.PrimaryKeyRelatedField(read_only=True)
    demographic_types = DemographicTypeSerializer(many = True, read_only=True)

    class Meta:
        model = Demographic
        fields = ('contains_representative', 'year', 'total_population', 'precinct', 'demographic_types')


class DemographicTypePopulationSerializer(serializers.ModelSerializer):
    # demographic = serializers.ForeignKey(Demographic, on_delete=models.PROTECT)
    demographic = serializers.PrimaryKeyRelatedField(read_only = True)
    # demographic_type = serializers.ForeignKey(DemographicType, on_delete=models.PROTECT)
    demographic_type = serializers.PrimaryKeyRelatedField(read_only = True)
    # population = serializers.IntegerField()

    class Meta:
        model = DemographicTypePopulation
        fields = ('demographic', 'demographic_type', 'population')


class EconomicDataSerializer(serializers.ModelSerializer):
    # gdp_per_capita = serializers.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    # median_income = serializers.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    # year = serializers.DateField()
    # precinct = serializers.ForeignKey(Precinct, on_delete=models.PROTECT)
    precinct = PrecinctSerializer(many = True, read_only=True)

    class Meta:
        model = EconomicData
        fields = ('gdp_per_capita', 'median_income', 'year', 'precinct')


class PoliticalPartySerializer(serializers.NodelSerializer):
    # description = serializers.CharField(max_length=100)
    class Meta:
        model = PoliticalParty
        fields = ('description')


class ElectionResultSerializer(serializers.ModelSerializer):
    # precinct = serializers.ForeignKey(Precinct, on_delete=models.PROTECT)
    # votes = serializers.ManyToManyField(PoliticalParty, through='VoteCount')
    precinct = PrecinctSerializer(read_only=True)
    votes = PoliticalPartySerializer(many=True, read_only=True)

    class Meta:
        model = ElectionResult
        fields = ('election_year', 'precinct', 'votes')

class VoteCountSerializer(serializers.ModelSerializer):
    election_result = ElectionResultSerializer(read_only=True)
    political_party = PoliticalPartySerializer(read_only=True)
    class Meta:
        model = VoteCount
        fields = ('election_result', 'political_party', 'num_votes')


class DistrictSerializer(serializers.ModelSerializer):
    # state = serializers.CharField(max_length=2)
    # description = serializers.CharField(max_length=200)
    # precincts = serializers.ManyToManyField(Precinct, through='DistrictMembership')
    precincts = PrecinctSerializer(many=True)

    class Meta:
        model = District
        fields = ('state','description','precincts')


class DistrictMembershipSerializer(serializers.ModelSerializer):
    # precinct = serializers.ForeignKey(Precinct, on_delete=models.PROTECT)
    # district = serializers.ForeignKey(District, on_delete=models.PROTECT)
    # from_year = serializers.DateField()
    # to_year = serializers.DateField(null=True, blank=True)
    precinct = PrecinctSerializer(read_only=True)
    district = DistrictSerializer(read_only=True)
    class Meta:
        model = DistrictMembership
        fields = ('precinct', 'district', 'from_year', 'to_year')
