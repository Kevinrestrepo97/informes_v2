from datetime import datetime
import locale
locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
from Format_fecha import formatear_fecha
from Format_recorrer_df import recorrer_df

def seguridad_contrato(df_dict:dict,contrato:str):

    df_seguridad = df_dict["Seguridad_social"]

    df_seguridad = df_seguridad.loc[df_seguridad["Contrato"] == contrato]

    df_seguridad["Fecha_certificacion"] = df_seguridad["Fecha_certificacion"].apply(formatear_fecha)
    df_seguridad["Fecha_inicio_cobertura"] = df_seguridad["Fecha_inicio_cobertura"].apply(formatear_fecha)
    df_seguridad["Fecha_fin_cobertura"] = df_seguridad["Fecha_fin_cobertura"].apply(formatear_fecha)
    df_seguridad["Total_pagado"] = df_seguridad["Total_pagado"].apply(lambda x: f'{x:,.0f}')
    df_seguridad = recorrer_df(df_seguridad)

    return df_seguridad