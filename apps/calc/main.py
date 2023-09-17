import os 
import yaml 
import numpy as np 
import pandas as pd 
import geopandas as gpd 

import matplotlib.pyplot as plt

import subprocess 

import SetFile as SetFile
import ExecKriging as ExecKriging 
import CreateGeojson as CreateGeojson
import CalcExistence as CalcExistence
import CalcDmd as CalcDmd
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
    
    
    #データの更新====================================================
    #メモ：処理がかぶらないように、前ステップの計算結果をdata_tmpにコピーし、data_outを更新する
    subprocess.run( ["./SetTempFile.sh" , "arguments"] , shell = True )


    '''
    #内挿補間手法（クリギング）==================================================
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
    '''MODEL1
    CalcExist = CalcExistence.calc_existence_model1( Datas.gdf_transfered ,
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
        z_pred = CalcExist.predict_mat( np.arange( -20 , -5 , 0.5 ) ) 
        ViewPredict.view_predict( z_pred , 0 , 4 , 100 , 1000 )     
    '''
    CalcExist = CalcExistence.calc_existence_model2(  Datas.gdf_transfered ,
                                                config['Model']['srid_calc'] , 
                                                config['Model']['sigma_amp'] , 
                                                config['Model']['lambda'] , 
                                                config['Model2']['C_cofficient'] , 
                                                config['Model2']['D_cofficient'] , 
                                                config['Model2']['parallel_threads'] )
    
    CalcExist.set_bound_and_grid( np.min( Datas.gdf_transfered.geometry.x ) - config['Model']['buff_meter'] , 
                                  np.max( Datas.gdf_transfered.geometry.x ) + config['Model']['buff_meter'] ,
                                  np.min( Datas.gdf_transfered.geometry.y ) - config['Model']['buff_meter'] ,
                                  np.max( Datas.gdf_transfered.geometry.y ) + config['Model']['buff_meter'] , 
                                  config['Model']['buff_meter'] ,  config['Model']['delta_mesh'] ) 
    
    past_day  = 20
    pred_day  = 1
    steps = 200
    z_pred = CalcExist.calc_existence_fp( past_day , pred_day , steps , config['Model']['check_surface'] )
    present_step = int( past_day / ( pred_day + past_day ) * steps )
    z_data = z_pred[ present_step ]

    if config['Model']['check_predict'] == True:
        ViewPredict.view_predict( z_pred , 0 , 4 , 100 , 1000 )     
    
    
    if config['Model']['output'] == True:
        Z_Geojson = CreateGeojson.create_geojson( 
                                        CalcExist.grid_x , 
                                        CalcExist.grid_y , 
                                        z_data , 
                                        CalcExist.crs   )
        
        Z_Geojson.set_surface4map( )
        Z_Geojson.transfer_crs( config['Model']['srid_org'] )
        Z_Geojson.output_geojson( Z_Geojson.cell_transfered , 'result_ex' )
          
        
    #DMDモード分析を実施===============================================================
    if config['Model']['check_predict'] == True and config['Model']['check_dmdmode'] == True:
        DMD = CalcDmd.dmd( z_pred , 4 , 2 , 9 , 10 , config['Model']['show_dmdmode']) 
        dmd_pred , dmd_mode = DMD.exec()
        
        for i in range( np.shape(dmd_mode)[0] ):
            fi = os.getcwd() + os.sep + 'data_out_dmd' + os.sep + 'dmdmode_' + str(i+1) + '.csv'
            df = pd.DataFrame( np.real( dmd_mode[i] ) ) 
            df.to_csv( fi , sep = "," )
            
        #pred
        ViewPredict.view_predict( np.real(dmd_pred ) , 0 , 1 , 300 , 1000 )
    

                                  
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
    
    

    
    