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

plt.rc('font', size = 14)
plt.rcParams['figure.figsize'] = [14, 14]

plt.gca().spines["top"].set_visible(False)    
plt.gca().spines["right"].set_visible(False)
plt.gca().get_xaxis().tick_bottom()    
plt.gca().get_yaxis().tick_left()
plt.grid(True, axis = 'x', linestyle = "dashed", lw = 0.5, color = "black", alpha = 0.3)

estados = list(df_estados.loc[df_estados['is_last'], ['state']
                             ].sort_values('state', ascending = True)['state'].unique())

estados.extend(["Brasil", "EUA", "Reino Unido", "Belgica"])

y_max = 695
yp_max = 1500

plt.barh(0, 1, label = 'Semana passada', color = (.3, .3, .3, .5))

# plt.axvline(862.37, 0, label = 'Belgica (862.37)', lw = 1.2, color = "black", alpha = 0.4)
# plt.axvline(695, 0, label = 'Reino Unido (695)', lw = 1, color = "black", alpha = 0.4)
# plt.axvline(474.45, 0, label = 'EUA (474.45)', lw = .8, color = "black", alpha = 0.4)
# plt.axvline(451.93, 0, label = 'Brasil (451.93)', lw = .6, color = "black", alpha = 0.4)

for e in range(31) :      
    if e < 27 :
        pop = max(df_estados.loc[(df_estados['state'] == estados[e]) & (df_estados['is_last']), 
                                 ['population']].loc[:, 'population'])

        y = np.median(df_estados.loc[(df_estados['state'] == estados[e]), 
                                   :].sort_values('day', ascending = True).iloc[:-1, 7].tail(7))

        y_pop = (10 ** 6) * y / pop

        y_last = np.median(df_estados.loc[(df_estados['state'] == estados[e]), 
                                   :].sort_values('day', ascending = True).iloc[:-8, 7].tail(14))

        y_pop_last = (10 ** 6) * y_last / pop
        
    elif e == 30:
        y_pop = 862.37
        y_pop_last = y_pop
        
    elif e == 29:
        y_pop = 695
        y_pop_last = y_pop
        
    elif e == 28:
        y_pop = 474.45
        y_pop_last = y_pop
        
    else:
        y_pop = 451.93
        y_pop_last = y_pop

    ratio = y_pop / y_max

    if ratio < .0625 :
        plt.barh(e, y_pop, label = estados[e], color = color2[-11])
    elif (ratio >= .0625) & (ratio < .125) :   
        plt.barh(e, y_pop, label = estados[e], color = color2[-9])
    elif (ratio >= .125) & (ratio < .25) :
        plt.barh(e, y_pop, label = estados[e], color = color2[-7])
    elif (ratio >= .25) & (ratio < .5) :
        plt.barh(e, y_pop, label = estados[e], color = color2[-5])
    elif (ratio >= .5) & (ratio < .75) :
         plt.barh(e, y_pop, label = estados[e], color = color2[-3])
    else  :
        plt.barh(e, y_pop, label = estados[e], color = color2[-1])
    
    plt.barh(e, y_pop_last, color = (.3, .3, .3, .3))

    plt.text(y_pop + 32, e, str(int(round(y_pop))), color = 'black',  
             fontsize = 14, horizontalalignment = 'left', verticalalignment = 'center')       

#plt.barh(27, 862.37, label = 'Belgica', color = color2[-1])
#plt.barh(28, 695, 0, label = 'Reino Unido', color = color2[-3])
#plt.barh(29, 474.45, 0, label = 'EUA', color = color2[-5])
#plt.barh(30, 451.93, 0, label = 'Brasil', color = color2[-5])       
               
plt.yticks(range(len(estados)), estados)

plt.ylabel('Estados')       
plt.xlim(0, yp_max * 1.2)         
plt.title(label[7] + " per capita - Brasil")
plt.legend(ncol = 2)
plt.xlabel(label[7] + " per capita")
plt.savefig('Graphics/' + label[7] + " per capita.png")
plt.show()

print("Gráfico criado com sucesso")