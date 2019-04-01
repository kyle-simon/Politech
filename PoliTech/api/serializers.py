from rest_framework import serializers
from django.contrib.gis.db import models
from api.models import *


class PrecinctSerializer(serializers.Serializer):
    precinct_shape = models.PolygonField(geography=True)  # 4386 corresponds to the World Geodetic System coordinates
    state = serializers.CharField(max_length=2)
    description = serializers.CharField(max_length=200)
    adjacencies = models.ManyToManyField('self', through='Adjacency', symmetrical=False, related_name='related_to+')

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
