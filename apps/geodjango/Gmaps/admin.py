from django.contrib.gis import admin
from Gmaps.models import G_surface

#背景地図をOpenStreetMapにする
admin.site.register(G_surface, admin.OSMGeoAdmin)