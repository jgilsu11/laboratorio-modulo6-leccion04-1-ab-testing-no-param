import pandas as pd
import numpy as np
from scipy import stats
import seaborn as sns

import matplotlib.pyplot as plt
from itertools import combinations


def crear_df_grupo(dataframe,columna_grupo,columna_metrica):
    lista= []
    for valor in dataframe[columna_grupo].unique():
        datos_filtrados=dataframe[dataframe[columna_grupo]== valor][columna_metrica]
        lista.append(datos_filtrados)

    return lista

def elegir_test(lista_datos,dependencia=False):
        if len(lista_datos) > 2:
            print("El test óptimo es Kruskall-Wallis")
            return stats.kruskal(*lista_datos)
        elif len(lista_datos) == 2 and dependencia:
            print("El test óptimo es Willcoxon")
            return stats.wilcoxon(*lista_datos)
        else:
            print("El test óptimo es Mann-Whitney")
            return stats.mannwhitneyu(*lista_datos)
        


def usar_whitney(df,columna_grupo , columna_metrica):
    lista_generos=df[columna_grupo].unique()
    combinaciones=list(combinations(lista_generos,2))
    for indice, valor in enumerate(combinaciones):
        estadistico, p_value= stats.mannwhitneyu(df[df[columna_grupo]== valor[0]][columna_metrica],df[df[columna_grupo]== valor[1]][columna_metrica])
        print(f"La evaluación de la hipótesis entre {valor[0]} y {valor[1]} da un p-value de {p_value}")
        if p_value >= 0.05:
            print("No hay diferencia")
            print(".................")
        else:
            print("Hay diferencia")
            print(".................")





def usar_kolmogorov(df,columna_grupo , columna_metrica):
    lista_genero= df[columna_grupo].unique().tolist()
    for indice, genero in enumerate(lista_genero):
        normalizale = df[df[columna_grupo] == genero][columna_metrica]
        media, desviacion = stats.norm.fit(normalizale) #esto se hace para ajustar los datos a una distribucion normal 
        estadistico, p_value = stats.kstest(normalizale, 'norm',args=(media,desviacion))   #aqui la _ es para que ahí se almacene el estadístico y en la otra solo el p-value
        resultado = p_value > 0.05
        print(f"la metrica para {genero} sigue una distribución normal según el test de Kolmogorov-Smirnov. Esta afirmación es {resultado}")  