# -*- coding: utf-8 -*-
from django.urls import path

from .views import gmaps_base , GeojsonAPI_existence , GeojsonAPI_direction
from djgeojson.views import GeoJSONLayerView
from .models import G_surface , G_dir

urlpatterns = [
    path("base/",gmaps_base.as_view(), name='gmaps_base'),
    path("geojson/ex" , GeoJSONLayerView.as_view(model=G_surface), name='testdata'),
    path("geojson/ex" , GeojsonAPI_existence.as_view(), name='testdata'),
    path("geojson/dir" , GeoJSONLayerView.as_view(model=G_dir), name='testdata'),
    path("geojson/dir" , GeojsonAPI_direction.as_view(), name='testdata'),
]
