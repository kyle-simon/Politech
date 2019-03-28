from django.db import models


# Create your models here.
#class Person(models.Model):
#   first_name = models.CharField(max_length=30, blank=True, null=True)
#  last_name = models.CharField(max_length=30)

class Precinct(models.Model):
    precinct_shape = models.PolygonField(srid=4386) # 4386 corresponds to the World Geodetic System coordinates
    state = models.CharField(max_length=2)
    description = models.CharField(max_length=200)
    adjacencies = models.ManyToManyField('self', through='Adjacency', symmetrical=False, related_name='related_to+')
    # The + after related_to is required, it makes it so Django will not expose the backwards relationship
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
            Adjacency.objects.filter(from_precinct=self.to_precinct, to_precinct=self)[0].add_adjacency_type(type, False)

    class Meta:
        index_together = [
            ("from_precinct", "to_precinct")
        ]

class AdjacencyType(models.Model):
    description = models.CharField(max_length=200)
    