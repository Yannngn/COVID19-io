import data
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from data import df_estados

# Listas

label = ["Estado", "Regiao", "População", "Último Dado", "Data", "Dia", "Casos Confirmados",
         "Óbitos Confirmados", "Novos Casos", "Novas Mortes", "Incidência de Casos", "Mortalidade"]
  
color = ['#e8615d', '#f49436', '#2d9de5', '#3bbdbd', '#634792']
color2 = ['#00876c', '#379469', '#58a066', '#78ab63', '#98b561', '#b8bf62', '#dac767',
          '#deb256', '#e09d4b', '#e18745', '#e06f45', '#dc574a', '#d43d51']
color3 = ['#00876c', '#4ea06d', '#84b76e', '#bbcd73', '#f4e07f', '#f4ba61', '#ef9250', 
          '#e5694c', '#d43d51']

plt.rc('font', size=14)
plt.rcParams['figure.figsize'] = [14, 10]

plt.gca().spines["top"].set_visible(False)    
plt.gca().spines["right"].set_visible(False)
plt.gca().get_xaxis().tick_bottom()    
plt.gca().get_yaxis().tick_left()
plt.grid(True, axis = 'y', linestyle = "dashed", lw = 0.5, color = "black", alpha = 0.3)

from data import df_estados

estados = list(df_estados.loc[df_estados['is_last'], ['state']].sort_values('state', ascending = True)['state'].unique())

y_max = 20000
yp_max = 75000

plt.bar(estados[0], 1, label = 'Estimativa', color = (.3, .3, .3, .3))
plt.bar(estados[0], 1, label = 'Semana passada', color = (.3, .3, .3, .5))

for e in range(27) :      
    pop = max(df_estados.loc[(df_estados['state'] == estados[e]) & (df_estados['is_last']), 
                             ['population']].loc[:, 'population'])

    IFR = max(df_estados.loc[(df_estados['state'] == estados[e]) & (df_estados['is_last']),
                             ['IFR']].loc[:, 'IFR'])        
#         if IFR == 0 :
#             IFR = np.median(df_estados.loc[df_estados['is_last'], ['IFR']].loc[:, 'IFR'])

    y = np.median(df_estados.loc[(df_estados['state'] == estados[e]), 
                               :].sort_values('day', ascending = True).iloc[:-1, 6].tail(7))

    y_pop = (10 ** 6) * y / pop 

    if y_pop > y_max :
        y_max = y_pop

    y_last = np.median(df_estados.loc[(df_estados['state'] == estados[e]), 
                               :].sort_values('day', ascending = True).iloc[:-8, 6].tail(14))

    y_pop_last = (10 ** 6) * y_last / pop

    ratio = y_pop / y_max

    if ratio < .0625 :
        plt.bar(estados[e], y_pop, label = estados[e], color = color2[-11])
    elif (ratio >= .0625) & (ratio <= .125) :   
        plt.bar(estados[e], y_pop, label = estados[e], color = color2[-9])
    elif (ratio >= .125) & (ratio <= .25) :
        plt.bar(estados[e], y_pop, label = estados[e], color = color2[-7])
    elif (ratio >= .25) & (ratio <= .5) :
        plt.bar(estados[e], y_pop, label = estados[e], color = color2[-5])
    elif (ratio >= .5) & (ratio <= .75) :
         plt.bar(estados[e], y_pop, label = estados[e], color = color2[-3])
    else  :
        plt.bar(estados[e], y_pop, label = estados[e], color = color2[-1])
    
    plt.bar(estados[e], y_pop_last, color = (.3, .3, .3, .3))

    if (IFR != 0) :

        y_mortes = (10 ** 6) * np.median(df_estados.loc[(df_estados['state'] == estados[e]), 
                                         :].sort_values('day', ascending = True).iloc[:-1, 7].tail(7)) / pop
        y_est = (100 * y_mortes / IFR) - y_pop

        if ratio < .0625 :
            plt.bar(estados[e], y_est, bottom = y_pop, color = color2[-11])
        elif (ratio >= .0625) & (ratio <= .125) :   
            plt.bar(estados[e], y_est, bottom = y_pop, color = color2[-9])
        elif (ratio >= .125) & (ratio <= .25) :
            plt.bar(estados[e], y_est, bottom = y_pop, color = color2[-7])
        elif (ratio >= .25) & (ratio <= .5) :
            plt.bar(estados[e], y_est, bottom = y_pop, color = color2[-5])
        elif (ratio >= .5) & (ratio <= .75) :
             plt.bar(estados[e], y_est, bottom = y_pop, color = color2[-3])
        else  :
            plt.bar(estados[e], y_est, bottom = y_pop, color = color2[-1])           

        plt.bar(estados[e], y_est, bottom = y_pop, color = (.9, .9, .9, .3))

        if y_est + y_pop > yp_max : 
            yp_max = y_est + y_pop

    if (y_pop != 0) :
        plt.text(estados[e], y_pop + 1000, str(int(round(y_pop))), color = 'black', rotation = 'vertical',
                     fontsize = 14, horizontalalignment = 'center', verticalalignment = 'bottom')
        if IFR != 0 :
            plt.text(estados[e], 7500 + y_est + y_pop, str(int(round(y_pop + y_est))), color = (0.1, 0.1, 0.1, 0.7), rotation = 'vertical',
                     fontsize = 14, horizontalalignment = 'center', verticalalignment = 'bottom')

plt.xlabel('Estados')       
plt.ylim(0, yp_max * 1.3)         
plt.title(label[6] + " - Estimativa por milhão de habitantes - Brasil")
plt.legend(ncol = 5)
plt.ylabel(label[6] + " por milhão de habitantes")
plt.savefig('Graphics/' + label[6] + " 1M.png")
plt.show()

print("Gráfico criado com sucesso")