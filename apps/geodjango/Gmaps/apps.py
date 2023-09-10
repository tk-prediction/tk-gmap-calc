from django.apps import AppConfig
#from django.contrib.gis import admin
#from Gmaps.models import G_surface


#背景地図をOpenStreetMapにする
#admin.site.register( G_surface , admin.OSMGeoAdmin)


class GmapsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Gmaps'
    

