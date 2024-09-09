from datetime import datetime
import locale
locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
from dateutil.relativedelta import relativedelta

#Funcion que devuelve los resutados desde la hoja general, convenios
def general_convenio(df_dict:dict,contrato:str):

    df_general = df_dict["General"]

    df_general = df_general.loc[df_general["Convenio"] == contrato]


    resultado_general_convenio = {
    #Establecer periodo verificacion mes actual menos 1
    "periodoverificacion": (datetime.now() - relativedelta(months=1)).strftime('%B'),
    "fechaelaboracion":(datetime.now()).strftime('%d de %B de %Y'),
    "contratante":df_general["Contratante"].iloc[0],
    "nit_contratante":df_general["Nit_contratante"].iloc[0],
    "contratista":"EMPRESA PARA LA SEGURIDAD Y SOLUCIONES URBANA - ESU",
    "nit_contratista":'890.984.761-8',
    "cargo_supervisor":df_general["Cargo"].iloc[0],
    "nombresupervisor":df_general["Nombre_supervisor_encargado"].iloc[0],
    "correo":df_general["Correo_supervisor"].iloc[0],
    "objeto_convenio":df_general["Objeto_convenio"].iloc[0],
    "convenio":df_general["Convenio"].iloc[0]
    }

    return resultado_general_convenio