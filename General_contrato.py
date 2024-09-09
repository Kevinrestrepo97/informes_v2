from datetime import datetime
import locale
locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')

#Funcion que devuelve los resutados desde la hoja general, contratos
def general(df_dict:dict,contrato:str):

    df_general = df_dict["General"]

    df_general = df_general.loc[df_general["Contrato"] == contrato]

    #crear variables

    resultado_general = {
    "periodoverificacion":(datetime.now()).strftime('%B'),
    "fechaelaboracion":(datetime.now()).strftime('%d de %B de %Y'),
    "contratante":"EMPRESA PARA LA SEGURIDAD Y SOLUCIONES URBANA - ESU",
    "nit":'890.984.761-8',
    "contratista":df_general["Contratista"].iloc[0],
    "nit_contratista":df_general["Nit_contratista"].iloc[0],
    "representante":df_general["Representante"].iloc[0],
    "cedula_representante":df_general["Identificacion_representante"].iloc[0],
    "objeto":df_general["Obeto_contrato"].iloc[0] 
    }

    return resultado_general