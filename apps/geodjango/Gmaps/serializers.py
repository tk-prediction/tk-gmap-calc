from Gmaps.models import G_surface , G_dir
from rest_framework_gis.serializers import GeoFeatureModelSerializer


class G_surface_Serializer(GeoFeatureModelSerializer):

    class Meta:
        model = G_surface
        geo_field = 'geom'
        auto_bbox = True
        fields = ('__all__')


class G_dir_Serializer(GeoFeatureModelSerializer):

    class Meta:
        model = G_dir
        geo_field = 'geom'
        auto_bbox = True
        fields = ('__all__')
