from pathlib import Path 
from django.contrib.gis.utils import LayerMapping
from .models import G_surface , G_dir


#生息分布をロード
def load_existence(verbose=True):
    g_mapping = { 
        'g_existence' : 'z' , 
        'geom' : 'MULTIPOLYGON' ,
        }
    g_shp = Path(__file__).resolve().parent / 'data_out' / 'result_ex.geojson' 

    lm = LayerMapping(G_surface, g_shp, g_mapping, transform=False)
    lm.save(strict=True, verbose=verbose)


#方向データをロード
def load_direction(verbose=True):
    g_mapping = { 
        'g_direction' : 'z' , 
        'geom' : 'MULTIPOLYGON' ,
        }
    g_shp = Path(__file__).resolve().parent / 'data_out' / 'result_dir.geojson' 

    lm = LayerMapping(G_dir , g_shp, g_mapping, transform=False)
    lm.save(strict=True, verbose=verbose)
