from django.contrib import admin
from django.urls import include, path

#from floodpredict.views import floodpredictedViewSet 
#from floodpredict.views import GeojsonAPIView , floodmap
from Gmaps.views import gmaps_base


urlpatterns = [
    path('admin/', admin.site.urls),
    path('gmap/' , include('Gmaps.urls'))

]
