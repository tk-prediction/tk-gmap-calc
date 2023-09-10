from django.shortcuts import render
from django.views import View

from rest_framework_gis.pagination import GeoJsonPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import json

from django.core.serializers import serialize
import traceback

from Gmaps.models import G_surface , G_dir


# Create your views here.

class gmaps_base(View):
    def get(self, request, *args, **keywords):
        """
        地図表示画面
        参考：https://chigusa-web.com/blog/django-leaflet/
        参考：https://homata.gitbook.io/geodjango/geodjango/tutorial
        """
        contexts = {} 
        
        return render( request , 'map/index.html')


#class GeojsonAPIView(APIView):
class GeojsonAPI_existence(APIView):
    def get(self, request, *args, **keywords):
        queryset = G_surface.objects.all()
        try:
            encjson  = serialize('geojson', srid=4326, geometry_field='geom', fields=('g_existence',) )
            result   = json.loads(encjson)
            response = Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            traceback.print_exc()
            response = Response({}, status=status.HTTP_404_NOT_FOUND)
        except:
            response = Response({}, status=status.HTTP_404_NOT_FOUND)

        return response

class GeojsonAPI_direction(APIView):
    def get(self, request, *args, **keywords):
        queryset = G_dir.objects.all()
        try:
            encjson  = serialize('geojson', srid=4326, geometry_field='geom', fields=('g_direction',) )
            result   = json.loads(encjson)
            response = Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            traceback.print_exc()
            response = Response({}, status=status.HTTP_404_NOT_FOUND)
        except:
            response = Response({}, status=status.HTTP_404_NOT_FOUND)

        return response
