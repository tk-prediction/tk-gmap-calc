# -*- coding: utf-8 -*-
from django.urls import path

from .views import gmaps_base , GeojsonAPI_existence , GeojsonAPI_direction , ExistenceViewSet ,DirectionViewSet
from djgeojson.views import GeoJSONLayerView
from .models import G_surface , G_dir

urlpatterns = [
    path("base/",gmaps_base.as_view(), name='gmaps_base'),
    #path("geojson_ex/" , GeoJSONLayerView.as_view(model=G_surface), name='testdata'),
    path("geojson_ex_tmp/" ,  ExistenceViewSet(), name='testdata'),
    path("geojson_ex/" , GeojsonAPI_existence.as_view(), name='testdata'),
    #path("geojson_dir/" , GeoJSONLayerView.as_view(model=G_dir), name='testdata'),
    path("geojson_dir_tmp/" ,  DirectionViewSet.as_view() , name='testdata'),
    path("geojson_dir/" , GeojsonAPI_direction.as_view(), name='testdata'),
]
