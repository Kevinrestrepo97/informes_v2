import pandas as pd
import os
from General_contrato import general
from General_convenio import general_convenio
from Movimientos_contrato import movimientos_general
from Movimientos_convenio import movimientos_convenio
from Polizas_contrato import polizas_contrato
from Polizas_convenio import polizas_convenio
from Seguridad_contrato import seguridad_contrato
from Seguridad_convenio import seguridad_convenio
from Imputacion_contrato_inicial import imputacion_contrato
from Imputacion_convenio_inicial import imputacion_convenio
# from Imputacion_convenio2 import imputacion_convenio2
from Pagos_contrato import pagos_contrato
from Pagos_convenio import pagos_convenio
from cInforme_change_font import change_font
from Informe_contrato import combinar_plantillas
from Informe_plantillas import plantillas
from docxtpl import DocxTemplate
from docx import Document
from consolidado import concatenado_oficial

def main(tipo:str):

    ruta = '../Formularios/'
    doce = '../Datalake/Doce'

    if tipo == "Contrato":
        ruta_oficial = os.path.join(ruta,'Propuesta_contrato.xlsx')
        ruta_doce = os.path.join(doce,'Doce_archivo.xlsx')
        ruta_cincuenta = os.path.join(doce,'Cincuenta.xlsx')

        df_hojas = pd.read_excel(ruta_oficial,sheet_name=None)
        df_doce = pd.read_excel(ruta_doce)
        df_cincuenta = pd.read_excel(ruta_cincuenta)

    return df_hojas,df_doce,df_cincuenta


concatenado_oficial()

#Variables de llamada
tipo = "Contrato"
contratos = [202300270]
mes = "mayo"

#Lectura de archivo
main_llamado,doce,cincuenta = main(tipo)

for contrato in contratos:

    docx_dir = f"../Informes_tecnicos_proveedores/{contrato}/{mes}/"

    #Funncion que selecciona las plantillas dependiendo del tipo
    archivos = plantillas(tipo)

    #Iteracion de los archivos.docx de la ruta docx_dir para hacer compose del componente tecnico
    for archivo in os.listdir(docx_dir):
        if archivo.endswith('.docx'):
            posicion = 1
            ruta_completa = os.path.join(docx_dir,archivo)
            archivos.insert(posicion,ruta_completa)
            posicion += 1

        # Ruta de salida para el documento combinado
        output_path = 'Plantilla.docx'
        # Nombre de la fuente deseada
        font_name = 'Montserrat'
        # Tamaño de la fuente deseada
        font_size = 12
        #Funcion que realiza el compose de los archivos en la ruta especificada, tambien contiene funcion change_font
        combinar_plantillas(archivos,output_path)

        doc = Document('Plantilla.docx')

        doc = change_font(doc,font_name, font_size, 1.4, 1.4, 1.0, 1.0)

        doc.save("Plantilla.docx")

        doc = DocxTemplate("Plantilla.docx")

if tipo == "Contrato":
    #Llamado contrato
    Resultado_general_contrato = general(main_llamado,contrato)
    adiciones,ampliaciones,suspensiones,otro_si,Resultados_movimientos_contratos = movimientos_general(main_llamado,contrato)
    Resultados_polizas_contrato = polizas_contrato(main_llamado,contrato)
    Resultados_seguridad_contrato = seguridad_contrato(main_llamado,contrato)
    #Desde archivos doce y cincuenta
    Resultados_imputacion_contrato,ejecucion_pagos,total_contrato,pagos= imputacion_contrato(doce,contrato)
    Resultados_pagos = pagos_contrato(cincuenta,contrato)

    

    contextInforme = {
    # desde general
    "periodoverificacion": Resultado_general_contrato["periodoverificacion"],
    "fechaelaboracion":Resultado_general_contrato["fechaelaboracion"],
    "contratante": Resultado_general_contrato["contratante"],
    "nit": Resultado_general_contrato["nit"],
    "contratista": Resultado_general_contrato["contratista"],
    "nitcontratista": Resultado_general_contrato["nit_contratista"],
    "representante": Resultado_general_contrato["representante"],
    "cedularepresentante": Resultado_general_contrato["cedula_representante"],
    "objeto": Resultado_general_contrato["objeto"],

    # desde movimientos
    "adiciones":    adiciones,
    "ampliaciones": ampliaciones,
    "suspensiones": suspensiones,
    "otrosi":otro_si,
    "totalcontrato": total_contrato,
    "valorinicialnumero":Resultados_movimientos_contratos["valor_inicial_contrato"],
    "fechainicial": Resultados_movimientos_contratos["fecha_inicial_contrato"],
    "fechafinal": Resultados_movimientos_contratos["fecha_final_contrato"],
    "totalcontratonombre": Resultados_movimientos_contratos["total_contrato_letra"],
    "financiero": Resultados_imputacion_contrato,
    "contrato": contrato,

    # desde polizas
    "polizas": Resultados_polizas_contrato,
    # desde pagos
    "pagos": Resultados_pagos,
    "pagosacomulados": pagos,
    # desde seguridad
    "seguridad": Resultados_seguridad_contrato,
    # desde ejecucion
    "ejecucion":Resultados_imputacion_contrato,
    #"ejecucion_porcentaje": ejecucion_resultado[1],
    "ejecucion_porcentaje" : ejecucion_pagos

}

# Crear la carpeta en la cual se guardara el informe si no existe
contrato_dir = f"../Informes/{contrato}"
if not os.path.exists(contrato_dir):
    os.makedirs(contrato_dir)

# Definir la ruta y nombre del archivo
temp_output_path = os.path.join(contrato_dir, f"Informe_proveedor_temp_{mes}_{contrato}.docx")

#Llama el cntexto dependiendo del tipo
doc.render(contextInforme)

#Guarda el informe en la ruta especificada
doc.save(temp_output_path)

os.remove("Plantilla.docx")


    # else:
    #     #Llamado convenio
    #     Resultado_general_convenio = general_convenio(main_llamado,contrato)
    #     adiciones,ampliaciones,suspensiones,otro_si,total_convenio,Resultados_movimientos_convenios = movimientos_convenio(main_llamado,contrato)
    #     Resultados_polizas_convenio = polizas_convenio(main_llamado,contrato)
    #     Resultados_seguridad_convenio = seguridad_convenio(main_llamado,contrato)
    #     Resultados_imputacion_convenio = imputacion_convenio(main_llamado,contrato)
    #     Resultados_imputacion_convenio2 = imputacion_convenio2(main_llamado,contrato)
    #     Resultados_pagos_convenio = pagos_convenio(main_llamado,contrato)
    #     Resultados_novedades_convenio = novedades_convenio(main_llamado,contrato)
        



    






