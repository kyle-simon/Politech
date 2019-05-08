from rest_framework import serializers, fields
from django.contrib.auth.models import User, Group
from django.contrib.gis.db import models
from rest_framework_gis.fields import GeometryField
from .models import *
from .constants import STATES

class AdjacencyTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdjacencyType
        fields = ['description']


class AdjacencySerializer(serializers.ModelSerializer):
    adjacency_types = AdjacencyTypeSerializer(many=True, read_only=True)
    class Meta:
        model = Adjacency
        fields = ['from_precinct', 'to_precinct', 'adjacency_types']



class PrecinctSerializer(serializers.ModelSerializer):
    adjacencies = AdjacencySerializer(many=True, read_only=True, source='to_precincts')
    state = serializers.ChoiceField(choices=STATES)

    class Meta:
        model = Precinct
        fields = ['precinct_shape', 'state', 'description', 'adjacencies']


class DemographicTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DemographicType
        fields = ['description']


class DemographicSerializer(serializers.ModelSerializer):
    precinct = serializers.PrimaryKeyRelatedField(read_only=True)
    demographic_types = DemographicTypeSerializer(many = True, read_only=True)

    class Meta:
        model = Demographic
        fields = ['contains_representative', 'year', 'total_population', 'precinct', 'demographic_types']


class DemographicTypePopulationSerializer(serializers.ModelSerializer):
    # demographic = serializers.ForeignKey(Demographic, on_delete=models.PROTECT)
    demographic = serializers.PrimaryKeyRelatedField(read_only = True)
    # demographic_type = serializers.ForeignKey(DemographicType, on_delete=models.PROTECT)
    demographic_type = serializers.PrimaryKeyRelatedField(read_only = True)
    # population = serializers.IntegerField()

    class Meta:
        model = DemographicTypePopulation
        fields = ['demographic', 'demographic_type', 'population']


class EconomicDataSerializer(serializers.ModelSerializer):
    # gdp_per_capita = serializers.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    # median_income = serializers.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    year = fields.DateField(input_formats=['%Y','iso-8601'])
    precinct = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = EconomicData
        # list_serializer_class = BulkListSerializer
        fields = ['gdp_per_capita', 'median_income', 'year', 'precinct']


class PoliticalPartySerializer(serializers.ModelSerializer):
    # description = serializers.CharField(max_length=100)
    class Meta:
        model = PoliticalParty
        fields = ['description']

class VoteCountSerializer(serializers.ModelSerializer):
    # election_result = ElectionResultSerializer(read_only=True)
    political_party = PoliticalPartySerializer(read_only=True)
    class Meta:
        model = VoteCount
        fields = ['political_party', 'num_votes']

class ElectionResultSerializer(serializers.ModelSerializer):
    # precinct = serializers.ForeignKey(Precinct, on_delete=models.PROTECT)
    # votes = serializers.ManyToManyField(PoliticalParty, through='VoteCount')
    precinct = serializers.PrimaryKeyRelatedField(read_only=True)
    votes = VoteCountSerializer(source='vote_counts', many=True, read_only=True)

    class Meta:
        model = ElectionResult
        fields = ['election_year', 'precinct',]




class DistrictSerializer(serializers.ModelSerializer):
    precincts = PrecinctSerializer(many=True)
    state = serializers.ChoiceField(choices=STATES)

    class Meta:
        model = District
        # list_serializer_class = BulkListSerializer
        fields = ['state','description','precincts']


class DistrictMembershipSerializer(serializers.ModelSerializer):
    # precinct = serializers.ForeignKey(Precinct, on_delete=models.PROTECT)
    # district = serializers.ForeignKey(District, on_delete=models.PROTECT)
    # from_year = serializers.DateField()
    # to_year = serializers.DateField(null=True, blank=True)
    precinct = PrecinctSerializer(read_only=True)
    district = DistrictSerializer(read_only=True)
    class Meta:
        model = DistrictMembership
        # list_serializer_class = BulkListSerializer
        fields = ['precinct', 'district', 'from_year', 'to_year']

# serializers for admin panel
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']

class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']

class StateSerializer(serializers.Serializer):
    state = serializers.ChoiceField(choices=STATES, read_only=True)
    districts = DistrictSerializer(many=True, read_only=True)
    adjacencies = AdjacencySerializer(many=True, read_only=True)
    # Economic data
    economic_data = EconomicDataSerializer(many=True, read_only=True, required=False)
    # Voting results data
    election_result_data = ElectionResultSerializer(many=True, read_only=True, required=False)
    # Demographic data
    demographic_data = DemographicSerializer(many=True, read_only=True, required=False)

