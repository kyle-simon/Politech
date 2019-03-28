from django.db import models


# Create your models here.
#class Person(models.Model):
#   first_name = models.CharField(max_length=30, blank=True, null=True)
#  last_name = models.CharField(max_length=30)

class Precinct(models.Model):
    precinct_shape = models.PolygonField(srid=4386) # 4386 corresponds to the World Geodetic System coordinates
    state = models.CharField(max_length=2)
    description = models.CharField(max_length=200)

    class Meta:
        index_together = [
            ("sequence", "stock")    
        ]