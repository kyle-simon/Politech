from rest_framework import serializers
from django.contrib.gis.db import models
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from api.models import *


class PrecinctSerializer(serializers.Serializer):
    precinct_shape = models.PolygonField(geography=True)  # 4386 corresponds to the World Geodetic System coordinates
    state = serializers.CharField(max_length=2)
    description = serializers.CharField(max_length=200)
    adjacencies = models.ManyToManyField('self', through='Adjacency', symmetrical=False, related_name='related_to+')

    class Meta:
        index_together = [("state", "description")]
        # The + after related_to is required, it makes it so Django will not expose the backwards relationship
        # Adjacency is a symmetric relationship but Django doesn't support symmetric relationships with a through table
        # So we must create these helper methods to properly expose a symmetric-like way to interact with our Precinct records

    def add_adjacency(self, precinct, sym=True):
        adjacency, created = Adjacency.objects.get_or_create(from_precinct=self, to_precinct=precinct)

        if sym:
            precinct.add_adjacency(self, False)

        return adjacency

    def remove_adjacency(self, precinct, sym=True):
        Adjacency.objects.filter(from_precinct=self, to_precinct=precinct).delete()

        if sym:
            precinct.remove_relationship(self, False)

    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        return Precinct.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Snippet` instance, given the validated data.
        """
        instance.precinct_shape = validated_data.get('precinct_shape', instance.precinct_shape)
        instance.state = validated_data.get('state', instance.state)
        instance.description = validated_data.get('description', instance.description)
        instance.adjacencies = validated_data.get('adjacencies', instance.adjacencies)
        instance.save()
        return instance


class AdjacencyTypeSerializer(serializers.Serializer):
    description = serializers.CharField(max_length=200)

    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        return AdjacencyType.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Snippet` instance, given the validated data.
        """
        instance.description = validated_data.get('description', instance.description)
        instance.save()
        return instance


class AdjacencySerializer(serializers.Serializer):
    from_precinct = serializers.ForeignKey(Precinct, on_delete=models.PROTECT, related_name='from_precincts')
    to_precinct = serializers.ForeignKey(Precinct, on_delete=models.PROTECT, related_name='to_precincts')
    adjacency_types = serializers.ManyToManyField(AdjacencyType)

    def add_adjacency_type(self, type, sym=True):
        self.adjacency_types.add(type)
        if sym:
            Adjacency.objects.get(from_precinct=self.to_precinct, to_precinct=self).add_adjacency_type(type, False)

    class Meta:
        index_together = [
            ("from_precinct", "to_precinct")
        ]

    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        return Adjacency.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Snippet` instance, given the validated data.
        """
        instance.from_precinct = validated_data.get('from_precinct', instance.from_precinct)
        instance.to_precinct = validated_data.get('to_precinct', to_precinct.state)
        instance.adjacency_types = validated_data.get('adjacency_types', instance.adjacency_types)
        instance.save()
        return instance


class DemographicTypeSerializer(serializers.Serializer):
    description = serializers.CharField(max_length=200)

    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        return DemographicType.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Snippet` instance, given the validated data.
        """
        instance.description = validated_data.get('description', instance.description)
        instance.save()
        return instance


class DemographicSerializer(serializers.Serializer):
    contains_representative = serializers.BooleanField(null=True, blank=True)
    year = serializers.DateField()
    total_population = serializers.IntegerField(null=True, blank=True)
    precinct = serializers.ForeignKey(Precinct, on_delete=models.PROTECT)
    demographic_types = serializers.ManyToManyField(DemographicType, through='DemographicTypePopulation')

    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        return Demographic.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Snippet` instance, given the validated data.
        """
        instance.contains_representative = validated_data.get('contains_representative', instance.contains_representative)
        instance.year = validated_data.get('year', instance.year)
        instance.total_population = validated_data.get('total_population', instance.total_population)
        instance.precinct = validated_data.get('precinct', instance.precinct)
        instance.demographic_types = validated_data.get('demographic_types', instance.demographic_types)
        instance.save()
        return instance


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
