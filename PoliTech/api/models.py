from django.db import models as models
from django.contrib.gis.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


# Create your models here.
# class Person(models.Model):
#   first_name = models.CharField(max_length=30, blank=True, null=True)
#  last_name = models.CharField(max_length=30)

class Precinct(models.Model):
    precinct_shape = models.MultiPolygonField(geography=True)  # 4386 corresponds to the World Geodetic System coordinates
    state = models.CharField(max_length=2)
    description = models.CharField(max_length=200)
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


class AdjacencyType(models.Model):
    description = models.CharField(max_length=200)


class Adjacency(models.Model):
    from_precinct = models.ForeignKey(Precinct, on_delete=models.PROTECT, related_name='from_precincts')
    to_precinct = models.ForeignKey(Precinct, on_delete=models.PROTECT, related_name='to_precincts')
    adjacency_types = models.ManyToManyField(AdjacencyType)

    def add_adjacency_type(self, type, sym=True):
        self.adjacency_types.add(type)
        if sym:
            Adjacency.objects.get(from_precinct=self.to_precinct, to_precinct=self).add_adjacency_type(type, False)

    class Meta:
        index_together = [
            ("from_precinct", "to_precinct")
        ]


class DemographicType(models.Model):
    description = models.CharField(max_length=200)


class Demographic(models.Model):
    contains_representative = models.BooleanField(null=True, blank=True)
    year = models.DateField()
    total_population = models.IntegerField(null=True, blank=True)
    precinct = models.ForeignKey(Precinct, on_delete=models.PROTECT)
    demographic_types = models.ManyToManyField(DemographicType, through='DemographicTypePopulation')

    class Meta:
        index_together = [
            ('precinct', 'year')
        ]


class DemographicTypePopulation(models.Model):
    demographic = models.ForeignKey(Demographic, on_delete=models.PROTECT)
    demographic_type = models.ForeignKey(DemographicType, on_delete=models.PROTECT)
    population = models.IntegerField()

    class Meta:
        index_together = [
            ('demographic', 'demographic_type')
        ]


class EconomicData(models.Model):
    gdp_per_capita = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    median_income = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    year = models.DateField()
    precinct = models.ForeignKey(Precinct, on_delete=models.PROTECT)


class PoliticalParty(models.Model):
    description = models.CharField(max_length=100)


class ElectionResult(models.Model):
    election_year = models.DateField()
    precinct = models.ForeignKey(Precinct, on_delete=models.PROTECT)
    votes = models.ManyToManyField(PoliticalParty, through='VoteCount', related_name='vote_counts')

    class Meta:
        index_together = [
            ('precinct', 'election_year')
        ]


class VoteCount(models.Model):
    election_result = models.ForeignKey(ElectionResult, on_delete=models.PROTECT)
    political_party = models.ForeignKey(PoliticalParty, on_delete=models.PROTECT)
    num_votes = models.IntegerField()


class District(models.Model):
    state = models.CharField(max_length=2)
    description = models.CharField(max_length=200)
    precincts = models.ManyToManyField(Precinct, through='DistrictMembership')


class DistrictMembership(models.Model):
    precinct = models.ForeignKey(Precinct, on_delete=models.PROTECT)
    district = models.ForeignKey(District, on_delete=models.PROTECT)
    from_year = models.DateField()
    to_year = models.DateField(null=True, blank=True)

    class Meta:
        index_together = [
            ('district', 'precinct', 'from_year')
        ]

class State(object):
    def __init__(self, state, districts, adjacencies, economic_data=None, demographic_data=None, election_result_data=None):
        self.state = state
        self.districts = districts
        self.adjacencies = adjacencies
        self.economic_data = economic_data
        self.demographic_data = demographic_data
        self.election_result_data = election_result_data

# For the admin panel
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
        print(post_save)