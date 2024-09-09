from datetime import datetime
import locale
locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
from Format_fecha import formatear_fecha
from Format_precio import formatear_precio
from Format_recorrer_df import recorrer_df


def polizas_contrato(df_dict:dict,contrato:str):

    df_polizas = df_dict["Polizas"]

    df_polizas = df_polizas.loc[df_polizas["Contrato"] == contrato]

    df_polizas["Fecha_inicial"] = df_polizas["Fecha_inicial"].apply(formatear_fecha)
    df_polizas["Fecha_final"] = df_polizas["Fecha_final"].apply(formatear_fecha)
    df_polizas["Valor_amparado"] = df_polizas["Valor_amparado"].apply(lambda x: f'{x:,.0f}')
    df_polizas = recorrer_df(df_polizas)

    return df_polizas