import data
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from datetime import datetime, timedelta

from data import df_estados
from data import Regiao
from data import df_Brasil

label = ["Estado", "Regiao", "População", "Último Dado", "Data", "Dia", "Casos Confirmados",
         "Óbitos Confirmados", "Novos Casos", "Novas Mortes", "Incidência de Casos", "Mortalidade"]

reg = ['Nordeste', 'Norte', 'Sudeste', 'Sul', 'Centro Oeste']

color = ['#e8615d', '#f49436', '#2d9de5', '#3bbdbd', '#634792']
color2 = ['#00876c', '#379469', '#58a066', '#78ab63', '#98b561', '#b8bf62', '#dac767',
          '#deb256', '#e09d4b', '#e18745', '#e06f45', '#dc574a', '#d43d51']
color3 = ['#00876c', '#4ea06d', '#84b76e', '#bbcd73', '#f4e07f', '#f4ba61', '#ef9250', 
          '#e5694c', '#d43d51']

dia = len(df_Brasil.index)

for f in range(6, 10) :
    
    plt.rc('font', size = 14)
    plt.rcParams['figure.figsize'] = [14, 10]

    plt.gca().spines["top"].set_visible(False)    
    plt.gca().spines["right"].set_visible(False)
    plt.gca().get_xaxis().tick_bottom()    
    plt.gca().get_yaxis().tick_left()
    plt.grid(True, axis = 'y', linestyle = "dashed", lw = 0.5, color = "black", alpha = 0.3)
    
    estados = list(df_estados.loc[df_estados['is_last'], 
                                  [df_estados.columns[f], 'state']                              
                                 ].sort_values(df_estados.columns[f], ascending = False)['state'].unique())
    
    # Brasil data
    FMT = '%Y-%m-%d'
    
    x = list(df_Brasil.index.map(lambda x : (datetime.strptime(x, FMT) - datetime.strptime("2020-02-25", FMT)).days))
    x_max = dia

    if f in [6, 7] :
        y = list(df_Brasil.iloc[:, f - 6])
        y_max = max(df_Brasil.iloc[:, f - 6])

#         plt.plot(x, [np.exp(X * np.log(2) / b[f - 6] ) * a[f - 6] for X in x], label = "Dobra a cada " + str(b[f - 6]) + " dias", 
#                  linestyle = 'dashed', color = (.5, .5, .5, .3))

        plt.plot(x, y, marker = ' ', color = 'black', label = "Brasil", lw = 2.5) 
        plt.text(x_max * 1.01, 1.01 * y[-1], "Brasil", color = "black", fontsize = 14)        
        
        for e in range(27) :  

            x = list(df_estados.loc[df_estados['state'] == estados[e],
                                    'date'].map(lambda x : (datetime.strptime(x, FMT) - 
                                                            datetime.strptime("2020-02-25", FMT)).days))

            y = list(df_estados.loc[df_estados['state'] == estados[e], df_estados.columns[f]])

            if e < 5 :
                plt.plot(x, y, marker = ' ', label = estados[e], color = color[e], lw = 2.5)
                if y[-1] > 0 :
                    plt.text(x_max * 1.01, y[-1], estados[e], color = color[e], fontsize = 14)
                elif y[-2] > 0 :
                    plt.text(x_max * 1.01, y[-2], estados[e], color = color[e], fontsize = 14)
                elif y[-3] > 0 :
                    plt.text(x_max * 1.01, y[-3], estados[e], color = color[e], fontsize = 14)

            elif e == 5 :
                plt.plot(x, y, marker = ' ', color = (.5, .5, .5, .1), lw = 1.5)
                plt.plot(1, 1, marker = ' ', label = 'Outros estados', color = (.5, .5, .5, .3), lw = 1.5)
            else :
                plt.plot(x, y, marker = ' ', color = (.5, .5, .5, .1), lw = 1.5)
        
        plt.title(label[f] + " no Brasil (log)")
    
    else : 
        y = list(df_Brasil.iloc[:, f - 6].rolling(window = 7).mean())
        y_max = max(df_Brasil.iloc[:, f - 6])

        plt.plot(x, y, marker = ' ', color = 'black', label = "Brasil", lw = 2.5) 
        plt.text(x_max * 1.01, 1.01 * y[-1], "Brasil", color = "black", fontsize = 14) 
        
        for e in range(27) :  

            x = list(df_estados.loc[df_estados['state'] == estados[e],
                                    'date'].map(lambda x : (datetime.strptime(x, FMT) - 
                                                            datetime.strptime("2020-02-25", FMT)).days))

            y = list(df_estados.loc[df_estados['state'] == estados[e], df_estados.columns[f]].rolling(window = 7).mean())

            if e < 5 :
                plt.plot(x, y, marker = ' ', label = estados[e], color = color[e], lw = 2.5)
                if y[-1] > 0 :
                    plt.text(x_max * 1.01, y[-1], estados[e], color = color[e], fontsize = 14)
                elif y[-2] > 0 :
                    plt.text(x_max * 1.01, y[-2], estados[e], color = color[e], fontsize = 14)
                elif y[-3] > 0 :
                    plt.text(x_max * 1.01, y[-3], estados[e], color = color[e], fontsize = 14)

            elif e == 5 :
                plt.plot(x, y, marker = ' ', color = (.5, .5, .5, .1), lw = 1.5)
                plt.plot(1, 1, marker = ' ', label = 'Outros estados', color = (.5, .5, .5, .3), lw = 1.5)
            else :
                plt.plot(x, y, marker = ' ', color = (.5, .5, .5, .1), lw = 1.5)
            
        plt.title(label[f] + " no Brasil (log) - Média 7 dias")
    
    plt.xlim(20, x_max + 1)
    plt.ylim(1, y_max * 1.1)
    plt.xticks(np.arange(20, x_max, 5))
    
    plt.legend(loc = 2)
    plt.yscale('log')
    plt.xlabel("Dias após 25/02/2020")
    plt.ylabel(label[f])
    plt.savefig('Graphics/' + label[f] + " Brasil log.png")
    plt.show()
    
print("Gráficos criados com sucesso")