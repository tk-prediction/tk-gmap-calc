import os 
import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt 
import matplotlib.cm as cm 
from matplotlib import animation


class view_predict:
    def __init__(self, pred_res , val_min , val_max, intval , rep_dely):
        #flood_re[ t , i , j ]=>t = 時間ステップ、 j , i =>メッシュij
        self.timesteps = np.shape( pred_res )[0]
        self.pred_res = pred_res 

        self.val_min = val_min   #コンター高さ最小値
        self.val_max = val_max   #コンター高さ最大値
        self.intval = intval     #コンター更新のΔt（再生速度）
        self.rep_dely = rep_dely #コンター映像リプレイ時のディレイ

        #if config == "output":#出力
        #    self.output_countour() 
            
        #elif config == "check": #可視化
        #    self.view_result()

        
    def view_result(self):
        fig, ax = plt.subplots()
        ims=[]
    
        for i in range( self.timesteps ):     
            im = ax.imshow( np.flipud( self.pred_res[i] ) ,  #縦が反転しているので、修正する
                            animated=True, 
                            vmin = self.val_min , 
                            vmax = self.val_max  )
            
            ims.append([im])

        anim = animation.ArtistAnimation(fig, ims, 
                                         interval=self.intval ,
                                         repeat_delay = self.rep_dely )
        plt.show()

        #ani.save('anim.gif', writer="imagemagick")
        #ani.save('anim.mp4', writer="ffmpeg")

    #pngとして出力用
    def output_countour(self, folder ):
        
        y_tmp = np.arange( np.shape( np.flipud( self.pred_res[0])  )[0] ) 
        x_tmp = np.arange( np.shape( np.flipud( self.pred_res[0])  )[1] ) 
        
        x , y = np.meshgrid( x_tmp , y_tmp )
        
                
        for i in range( self.timesteps ):                 
            fig, ax = plt.subplots()
            ax.axis("off") #軸はなしにする
            
            #cmap=cm.YlOrRd
            cmap=cm.viridis
            cmap.set_under('w', alpha=0)            
            cmap.set_over('r')    
            
            ax = plt.contourf( x, y, np.flipud( self.pred_res[i]) , 
                              np.arange(0.02 , 1.0 , 0.05 ) , 
                              cmap = cmap )  
            
            
            
            f = folder + 'result_' + str(i+1) 
            plt.savefig(f , transparent = True )
            plt.close()
            
            
        
        
        