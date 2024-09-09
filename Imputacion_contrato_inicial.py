import pandas as pd
from Imputacion_contrato_parte1 import contrato_funcion
from Format_recorrer_df import recorrer_df
import os

#Establece llamado a la funcion contrato_funcion para devolver el df y retornar las variables del documento
def imputacion_contrato(df_doce:pd.DataFrame,contrato:str):

    df_imputacion = contrato_funcion(df_doce,contrato)


    total_contrato = f'{df_imputacion["Valor"].sum():,.0f}'

    pagos = f'{df_imputacion["Valor_EPG"].sum():,.0f}'

    ejecucion = (((df_imputacion["Valor_EPG"].sum()-df_imputacion["Valor_EPX"].sum())/(df_imputacion["Valor"].sum() - df_imputacion["Valor_ECX"].sum()) )*100).round(1)

    df_imputacion["Valor"] = df_imputacion["Valor"].apply(lambda x: f'{x:,.0f}')
    df_imputacion["Valor_EPG"] = df_imputacion["Valor_EPG"].apply(lambda x: f'{x:,.0f}')
    df_imputacion["Saldo"] = df_imputacion["Saldo"].apply(lambda x: f'{x:,.0f}')
    df_imputacion = recorrer_df(df_imputacion)


    return df_imputacion,ejecucion,total_contrato,pagos