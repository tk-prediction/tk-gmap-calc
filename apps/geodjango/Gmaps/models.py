from django.contrib.gis.db import models
from django.db.models import Manager as GeoManager


# Create your models here.
class G_surface( models.Model):
    g_existence = models.FloatField()
    geom = models.MultiPolygonField(srid=4326) #表示系はすべてwgs84とする
    objects = GeoManager() 


# Create your models here.
class G_dir( models.Model):
    g_direction = models.FloatField()
    geom = models.MultiPolygonField(srid=4326) #表示系はすべてwgs84とする
    objects = GeoManager() 
