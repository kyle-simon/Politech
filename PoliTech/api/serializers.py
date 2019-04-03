from rest_framework import serializers
from django.contrib.gis.db import models
from rest_framework_gis.fields import GeometryField
from api.models import *


class PrecinctSerializer(serializers.ModelSerializer):
    adjacencies = AdjacencySerializer(many=true, read_only=true)

    class Meta:
        model = Precinct
        fields = ('precinct_shape', 'state', 'description', 'adjacencies')


class AdjacencyTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdjacencyType
        fields = ('description')


class AdjacencySerializer(serializers.ModelSerializer):
    adjacency_types = AdjacencyTypeSerializer(many = true, read_only=true)
    class Meta:
        model = Adjacency
        fields = ('adjacency_types')


class DemographicTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DemographicType
        fields = ('description')


class DemographicSerializer(serializers.ModelSerializer):
    precinct = serializers.PrimaryKeyRelatedField(read_only=true)
    demographic_types = DemographicTypeSerializer(many = true, read_only=true)

    class Meta:
        model = Demographic
        fields = ('contains_representative', 'year', 'total_population', 'precinct', 'demographic_types')


class DemographicTypePopulationSerializer(serializers.Serializer):
    demographic = serializers.ForeignKey(Demographic, on_delete=models.PROTECT)
    demographic_type = serializers.ForeignKey(DemographicType, on_delete=models.PROTECT)
    population = serializers.IntegerField()

    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        return DemographicTypePopulation.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Snippet` instance, given the validated data.
        """
        instance.demographic = validated_data.get('demographic', instance.demographic)
        instance.demographic_type = validated_data.get('demographic_type', instance.demographic_type)
        instance.population = validated_data.get('population', instance.population)
        instance.save()
        return instance


class EconomicDataSerializer(serializers.Serializer):
    gdp_per_capita = serializers.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    median_income = serializers.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    year = serializers.DateField()
    precinct = serializers.ForeignKey(Precinct, on_delete=models.PROTECT)

    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        return EconomicData.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Snippet` instance, given the validated data.
        """
        instance.gdp_per_capita = validated_data.get('gdp_per_capita', instance.gdp_per_capita)
        instance.median_income = validated_data.get('median_income', instance.median_income)
        instance.year = validated_data.get('year', instance.year)
        instance.precinct = validated_data.get('precinct', instance.precinct)
        instance.save()
        return instance


class PoliticalPartySerealizer(serializers.Serializer):
    description = serializers.CharField(max_length=100)

    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        return PoliticalParty.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Snippet` instance, given the validated data.
        """
        instance.description = validated_data.get('description', instance.description)
        instance.save()
        return instance


class ElectionResultSerializer(serializers.Serializer):
    election_year = serializers.DateField()
    precinct = serializers.ForeignKey(Precinct, on_delete=models.PROTECT)
    votes = serializers.ManyToManyField(PoliticalParty, through='VoteCount')

    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        return ElectionResult.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Snippet` instance, given the validated data.
        """
        instance.election_year = validated_data.get('election_year', instance.election_year)
        instance.precinct = validated_data.get('precinct', instance.precinct)
        instance.votes = validated_data.get('votes', instance.votes)
        instance.save()
        return instance


class VoteCountSerializer(serializers.Serializer):
    election_result = serializers.ForeignKey(ElectionResult, on_delete=models.PROTECT)
    political_party = serializers.ForeignKey(PoliticalParty, on_delete=models.PROTECT)
    num_votes = serializers.IntegerField()

    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        return VoteCount.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Snippet` instance, given the validated data.
        """
        instance.election_result = validated_data.get('election_result', instance.election_result)
        instance.political_party = validated_data.get('political_party', instance.political_party)
        instance.num_votes = validated_data.get('num_votes', instance.num_votes)
        instance.save()
        return instance


class DistrictSerializer(serializers.Serializer):
    state = serializers.CharField(max_length=2)
    description = serializers.CharField(max_length=200)
    precincts = serializers.ManyToManyField(Precinct, through='DistrictMembership')

    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        return District.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Snippet` instance, given the validated data.
        """
        instance.state = validated_data.get('state', instance.state)
        instance.description = validated_data.get('description', instance.description)
        instance.precincts = validated_data.get('precincts', instance.precincts)
        instance.save()
        return instance


class DistrictMembershipSerializer(serializers.Serializer):
    precinct = serializers.ForeignKey(Precinct, on_delete=models.PROTECT)
    district = serializers.ForeignKey(District, on_delete=models.PROTECT)
    from_year = serializers.DateField()
    to_year = serializers.DateField(null=True, blank=True)

    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        return DistrictMembership.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Snippet` instance, given the validated data.
        """
        instance.precinct = validated_data.get('precinct', instance.precinct)
        instance.district = validated_data.get('district', instance.district)
        instance.from_year = validated_data.get('from_year', instance.from_year)
        instance.to_year = validated_data.get('to_year', instance.to_year)
        instance.save()
        return instance
