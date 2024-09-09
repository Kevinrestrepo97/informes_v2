import pandas as pd

#Recorrer dataframes para convertirlos en diccionarios y retornarlos
def recorrer_df(df:pd.DataFrame):

    lista = []

    for indice,fila in df.iterrows():
        dic = {f"columna{i}":valor for i,valor in enumerate(fila)}
        lista.append(dic)
    

    return lista