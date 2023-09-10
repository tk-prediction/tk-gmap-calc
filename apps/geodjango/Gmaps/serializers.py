from Gmaps.models import G_surface
from rest_framework_gis.serializers import GeoFeatureModelSerializer


class G_surface_Serializer(GeoFeatureModelSerializer):

    class Meta:
        model = G_surface
        geo_field = 'geom'
        auto_bbox = True
        fields = ('__all__')
