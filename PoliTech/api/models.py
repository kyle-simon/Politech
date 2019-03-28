from django.db import models
from django.contrib.gis.db import models


# Create your models here.
#class Person(models.Model):
#   first_name = models.CharField(max_length=30, blank=True, null=True)
#  last_name = models.CharField(max_length=30)

class Precinct(models.Model):
    precinct_shape = models.PolygonField(geography=True) # 4386 corresponds to the World Geodetic System coordinates
    state = models.CharField(max_length=2)
    description = models.CharField(max_length=200)
    adjacencies = models.ManyToManyField('self', through='Adjacency', symmetrical=False, related_name='related_to+')
    # The + after related_to is required, it makes it so Django will not expose the backwards relationship
    # Adjacency is a symmetric relationship but Django doesn't support symmetric relationships with a through table
    # So we must create these helper methods to properly expose a symmetric-like way to interact with our Precinct records
    def add_adjacency(self, precinct, sym = True):
        adjacency, created = Adjacency.objects.get_or_create(from_precinct=self, to_precinct=precinct)

        if sym:
            precinct.add_adjacency(self, False)

        return adjacency

    def remove_adjacency(self, precinct, sym=True):
        Adjacency.objects.filter(from_precinct=self, to_precinct=precinct).delete()

        if sym:
            precinct.remove_relationship(self, False)


    class Meta:
        index_together = [
            ("sequence", "stock")    
        ]
    


class Adjacency(models.Model):
    from_precinct = models.ForeignKey(Precinct)
    to_precinct = models.ForeignKey(Precinct)
    adjacency_types = models.ManyToManyField(AdjacencyType)


    def add_adjacency_type(self, type, sym=True):
        self.adjacency_types.add(type)
        if sym:
            Adjacency.objects.get(from_precinct=self.to_precinct, to_precinct=self).add_adjacency_type(type, False)

    class Meta:
        index_together = [
            ("from_precinct", "to_precinct")
        ]

class AdjacencyType(models.Model):
    description = models.CharField(max_length=200)

class Demographic(models.Model):
    contains_representative = models.BooleanField(null=True, blank=True)
    year = models.DateField()
    total_population = models.IntegerField(null=True, blank=True)
    precinct = models.ForeignKey(Precinct)
    demographic_types = models.ManyToManyField(DemographicType, through='DemographicTypePopulation')

    class Meta:
        index_together = [
            ('precinct', 'year')    
        ]

class DemographicTypePopulation:
    demographic = models.ForeignKey(Demographic)
    demographic_type = models.ForeignKey(DemographicType)
    population = models.IntegerType()

    class Meta:
        index_together =[
            ('demographic', 'demographic_type')    
        ]

class DemographicType(models.Model):
    description = models.CharField(max_length=200)

class EconomicData(models.Model):
    gdp_per_capita = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    median_income = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    year = models.DateField()
    precinct = models.ForeignKey(Precinct)

class ElectionResult(models.Model):
    election_year = models.Date()
    precinct = models.ForeignKey(Precinct)
    votes = models.ManyToManyField(PoliticalParties, through='VoteCount')

    class Meta:
        index_together = [
            ('precinct', 'election_year')    
        ]

class VoteCount(models.Model):
    election_result = models.ForeignKey(ElectionResult)
    political_party = models.ForeignKey(PoliticalParty)
    num_votes = models.IntegerField()

class PoliticalParty(models.Model):
    description = models.CharField(max_length=100)
    
class District(models.Model):
    state = models.CharField(max_length=2)
    description = models.CharField(max_length=200)
    precincts = models.ManyToManyField(Precinct, through='DistrictMembership')

class DistrictMembership(models.Model):
    precinct = models.ForeignKey(Precinct)
    district = models.ForeignKey(District)
    from_year = models.Date()
    to_year = models.Date(null=True, blank=True)

    class Meta:
        index_together = [
            ('district', 'precinct', 'from_year')    
        ]