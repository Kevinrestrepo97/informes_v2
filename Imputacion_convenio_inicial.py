import pandas as pd
from Format_fecha import formatear_fecha
from Format_precio import formatear_precio
from Format_recorrer_df import recorrer_df
from Imputacion_convenio_parte2 import contrato_funcion
from Imputacion_convenio_parte1 import convenio_funcion
from medir_tiempo import medir_tiempo

def imputacion_convenio(df:pd.DataFrame,contrato:str,CCosto):


    df = df.copy()

    df_imputacion_contrato = contrato_funcion(df,contrato,CCosto)

    df_imputacion_convenio = convenio_funcion(df,contrato,CCosto)

    pagos_acomulados = f'{df_imputacion_convenio["Valor_EPG"].sum():,.0f}'
    ejecucion_convenio = ((df_imputacion_convenio["Valor_EPG"].sum()/df_imputacion_convenio["Valor"].sum())*100).round(1)
    total_convenio = f'{df_imputacion_convenio["Valor"].sum():,.0f}'

    df_imputacion_convenio["Valor_ECO"] = df_imputacion_convenio["Valor_ECO"].apply(lambda x: f'{x:,.0f}')
    df_imputacion_convenio["Valor"] = df_imputacion_convenio["Valor"].apply(lambda x: f'{x:,.0f}')

    df_imputacion_contrato["Valor_EPG"] = df_imputacion_contrato["Valor_EPG"].apply(lambda x: f'{x:,.0f}')
    df_imputacion_contrato["Valor"] = df_imputacion_contrato["Valor"].apply(lambda x: f'{x:,.0f}')
    df_imputacion_contrato["Saldo"] = df_imputacion_contrato["Saldo"].apply(lambda x: f'{x:,.0f}')

    df_imputacion_convenio = recorrer_df(df_imputacion_convenio)
    df_imputacion_contrato = recorrer_df(df_imputacion_contrato)

    return df_imputacion_convenio,pagos_acomulados,ejecucion_convenio,total_convenio,df_imputacion_contrato