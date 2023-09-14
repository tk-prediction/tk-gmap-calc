from django.contrib.gis import admin
from Gmaps.models import G_surface , G_dir

#背景地図をOpenStreetMapにする
admin.site.register(G_surface, admin.OSMGeoAdmin)
admin.site.register(G_dir, admin.OSMGeoAdmin)
