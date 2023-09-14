import os 
import yaml 
import numpy as np 
import pandas as pd 
import geopandas as gpd 

import matplotlib.pyplot as plt

import SetFile as SetFile
import ExecKriging as ExecKriging 
import CreateGeojson as CreateGeojson
import CalcExistence as CalcExistence
import CalcDirection as CalcDirection
import ViewPredict as ViewPredict


if __name__ == '__main__':
    
    #カレントディレクトリの移動
    os.chdir(os.path.dirname(os.path.abspath('__file__'))) 
    
    #計算条件はconfig.ymlファイルから読みとる
    with open('config.yml', 'r') as yml:
        config = yaml.safe_load(yml)
    
    
    #データの読み込み===============================================
    data_path = os.getcwd() + os.sep + 'data_in' + os.sep + 'test.csv'
    Datas = SetFile.data(data_path , config['Model']['srid_org'] ) #データ読み込みクラスの設定
        
    Datas.read_and_transfer_data( config['Model']['srid_calc'] ) 


    '''
    #内挿補間手法======================================================
    SFIP = ExecKriging.surface_interpolate( Datas.gdf_transfered , config['Model']['srid_calc']  )
    SFIP.make_kriging_model()
    SFIP.create_surface( config['Model']['buff_meter'] , 
                         config['Model']['delta_mesh'] ,
                         config['Model']['check_surface'] )
    SFIP.set_surface4map()
    SFIP.transfer_crs(  config['Model']['srid_org']  )
    SFIP.output_geojson( SFIP.cell_transfered )
    '''
    
    #時空間的な生息分布の計算=====================================================
    CalcExist = CalcExistence.calc_existence( Datas.gdf_transfered ,
                                              config['Model']['srid_calc'] , 
                                              config['Model']['sigma_amp'] , 
                                              config['Model']['lambda'] )
    
    CalcExist.set_bound_and_grid( np.min( Datas.gdf_transfered.geometry.x ) - config['Model']['buff_meter'] , 
                                  np.max( Datas.gdf_transfered.geometry.x ) + config['Model']['buff_meter'] ,
                                  np.min( Datas.gdf_transfered.geometry.y ) - config['Model']['buff_meter'] ,
                                  np.max( Datas.gdf_transfered.geometry.y ) + config['Model']['buff_meter'] , 
                                  config['Model']['buff_meter'] ,  config['Model']['delta_mesh'] ) 
    
    z_data = CalcExist.calc_existence_proj( 0 , config['Model']['check_surface']  )
    
    if config['Model']['check_predict'] == True:
        z_pred = CalcExist.predict_mat( np.arange( 0 , 20 , 4 ) ) 
        ViewPredict.view_predict( z_pred , 0 , 4 , 300 , 1000 )
        
    if config['Model']['output'] == True:
        Z_Geojson = CreateGeojson.create_geojson( 
                                        CalcExist.grid_x , 
                                        CalcExist.grid_y , 
                                        z_data , 
                                        CalcExist.crs   )
        
        Z_Geojson.set_surface4map( )
        Z_Geojson.transfer_crs( config['Model']['srid_org'] )
        Z_Geojson.output_geojson( Z_Geojson.cell_transfered , 'result_ex' )

                                  
    #生息分布に基づく、directデータを計算===============================================
    CalcDir = CalcDirection.DIR()
    dir_data = CalcDir.exec( z_data , config['Model']['check_dir'])

     
    if config['Model']['output'] == True:
        DIR_Geojson = CreateGeojson.create_geojson( 
                                        CalcExist.grid_x , 
                                        CalcExist.grid_y , 
                                        dir_data , 
                                        CalcExist.crs )
        
        DIR_Geojson.set_surface4map( )
        DIR_Geojson.transfer_crs( config['Model']['srid_org'] )
        DIR_Geojson.output_geojson( DIR_Geojson.cell_transfered , 'result_dir' )    
    
    

    
    