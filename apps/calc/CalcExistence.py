import os 
import numpy as np 
import pandas as pd 
from datetime import datetime, timedelta

import shapely
import geopandas as gpd

import matplotlib.pyplot as plt 


class calc_existence():
    def __init__(self , data , crs , sigma_amp , ll ):
        '''
        データ（レコード）数:data_num
        データ:data        (geopandas dataframe)
        データcrs: crs 
        空間分布のシグマ（空間広がり度）：sigma(2・2対角行列)
        時間分布のλ：ll
        
        '''
        self.data_num = np.shape( data )[0]
        self.data = data 
        self.crs = crs 
        
        self.sigma = np.array( [ 1, 0 , 0, 1 ] ).reshape((2,2)) * sigma_amp #単位行列×sigma_amp
        self.ll = ll
            
    
    #計算領域の範囲を指定    
    def set_bound_and_grid( self , x_min , x_max , y_min , y_max , buff_meter , delta_mesh ):

        self.x_bound = [ x_min - buff_meter , x_max + buff_meter ]  
        self.y_bound = [ y_min - buff_meter , y_max + buff_meter ]
        
        x_position = np.arange( self.x_bound[0] , self.x_bound[1] , delta_mesh )
        y_position = np.arange( self.y_bound[0] , self.y_bound[1] , delta_mesh )
        
        self.grid_x , self.grid_y = np.meshgrid(x_position , y_position )  
    

    #各データの観測日からの経過時間を計測
    def deltatimes( self ):
        datetime_data = pd.to_datetime( self.data.iloc[:,0] ) #取得データの日付をdatetime型に変換
        dt = datetime.now() - datetime_data.dt.to_pydatetime()
        
        day = []
        for i in dt:
            day.append( ( i.days * 86400  + i.seconds )  / 86400 )
        return day
        
        
    #生息分布を計算
    def calc_existence_proj(self , time_buff , check_view) : 
        
        passedtimes = self.deltatimes()  #計算用経過時間(単位：日)
        x_tmp = self.grid_x.flatten()
        y_tmp = self.grid_y.flatten()        
        
        xy_data = np.vstack( (self.data.geometry.x , self.data.geometry.y) ) #観測地点のxy座標

        
        for n in range( self.data_num ):

            xy_tmp = np.vstack( (x_tmp - xy_data[0,n], y_tmp - xy_data[1,n] ) ) #計算用グリッド座標                            
            
            #passedtimes - time_buff < 0 のデータは反映しない
            if passedtimes[n] + time_buff < 0:
                usability = 0 
            else: 
                usability = 1 
            
            #P_tmp = 時間分布×空間分布
            P = np.exp( -1.0 * ( passedtimes[n] + time_buff ) * self.ll ) * \
                np.exp( -1.0 * np.diag(  xy_tmp.T @ np.linalg.inv( self.sigma ) @  xy_tmp  ) ) * \
                usability
                    
            P = np.reshape( P , (np.shape(self.grid_x)[0] , np.shape(self.grid_x)[1] ) )#メッシュサイズに変形
            
            if n == 0:                 
                z = P
        
            else: 
                z = z + P
        
                
        #生息分布をチェックする
        def check_response_surface( gridX , gridY , z_interpolate , point_x , point_y , point_z ):
            fig, ax = plt.subplots()

            im = ax.contourf(  gridX , gridY ,  z_interpolate )
            fig.colorbar(im)
            ax.scatter( point_x , point_y , s=30 ,  c = 'w' ,linewidths=1 , ec = 'k' ) #c = point_z 
            plt.show()        
        
        #生息分布データのチェック
        if check_view == True :             
            check_response_surface( self.grid_x , 
                                    self.grid_y , 
                                    z ,
                                    self.data.geometry.x , 
                                    self.data.geometry.y , 
                                    np.ones(self.data_num) )            
            
        return z #結果を返す
            
    
    #数日先の縮退を想定したマップ
    def predict_mat(self , days_buff ):        
        z = np.array([])
        
        for buff in days_buff:
            print( "days buff:" , buff )
            z_tmp = self.calc_existence_proj( buff, None )
            z = np.append( z , z_tmp )
            
        z = np.reshape( z , ( np.size(days_buff) , np.shape(z_tmp)[0] , np.shape(z_tmp)[1] ) )
        
        return z 
        
    
