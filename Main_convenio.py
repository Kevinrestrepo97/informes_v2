import pandas as pd
import os
from General_convenio import general_convenio
from Movimientos_convenio import movimientos_convenio
from Polizas_convenio import polizas_convenio
from Seguridad_convenio import seguridad_convenio
from Imputacion_convenio_inicial import imputacion_convenio
from Pagos_convenio import pagos_convenio
from Informe_contrato import combinar_plantillas
from Informe_plantillas import plantillas
from docxtpl import DocxTemplate
from medir_tiempo import medir_tiempo
from cInforme_change_font import change_font
from docx import Document
from consolidado import concatenado_oficial


def main():

    ruta = '../Formularios/'
    doce = '../Datalake/Doce'

    # if tipo == "Convenio":
    ruta_oficial = os.path.join(ruta,'Propuesta_convenio.xlsx')
    ruta_doce = os.path.join(doce,'Doce_archivo.xlsx')
    ruta_cincuenta = os.path.join(doce,'Cincuenta.xlsx')

    df_hojas = pd.read_excel(ruta_oficial,sheet_name=None)
    df_doce = pd.read_excel(ruta_doce,usecols=["Rubro","Nombre Rubro","Fecha","Tipo Documento","Numero","Valor","CCosto","Nombre CCosto",
                                                "Fuente Financiacion","Contrato","Compromiso","Disponibilidad","Disponibilidad PPTO","Convenio"])
    df_cincuenta = pd.read_excel(ruta_cincuenta)

    return df_hojas,df_doce,df_cincuenta


concatenado_oficial()


#Variables de llamada
tipo = "Convenio"
contratos = ["57C DE 2024"]
CCosto = 33271
mes = "agosto"

#Lectura de archivo
main_llamado,doce,cincuenta = main()

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
        font_name = 'Arial'
        # Tamaño de la fuente deseada
        font_size = 11
        #Funcion que realiza el compose de los archivos en la ruta especificada, tambien contiene funcion change_font
        combinar_plantillas(archivos,output_path)

        doc = Document('Plantilla.docx')

        doc = change_font(doc,font_name, font_size, 1.4, 1.4, 1.0, 1.0)

        doc.save("Plantilla.docx")

        doc = DocxTemplate("Plantilla.docx")

        doc = DocxTemplate('Plantilla.docx')

if tipo == "Convenio":
    #Llamado convenio
    Resultado_general_convenio = general_convenio(main_llamado,contrato)
    adiciones,ampliaciones,suspensiones,otro_si,Resultados_movimientos_convenios = movimientos_convenio(main_llamado,contrato)
    Resultados_polizas_convenio = polizas_convenio(main_llamado,contrato)
    Resultados_seguridad_convenio = seguridad_convenio(main_llamado,contrato)
    Resultados_imputacion_convenio,pagos_acomulados,ejecucion_convenio,total_convenio,df_imputacion_contrato = imputacion_convenio(doce,contrato,CCosto)
    Resultados_pagos_convenio = pagos_convenio(cincuenta,contrato)

    

    contextInforme = {
    # desde general
    "contrato": Resultado_general_convenio["convenio"],
    "periodoverificacion": Resultado_general_convenio["periodoverificacion"],
    "fechaelaboracion":Resultado_general_convenio["fechaelaboracion"],
    "contratante": Resultado_general_convenio["contratante"],
    "nit": Resultado_general_convenio["nit_contratante"],
    "contratista": Resultado_general_convenio["contratista"],
    "nitcontratista": Resultado_general_convenio["nit_contratista"],
    "objeto": Resultado_general_convenio["objeto_convenio"],
    "nombresupervisor": Resultado_general_convenio["nombresupervisor"],
    "cargo_supervisor": Resultado_general_convenio["cargo_supervisor"],
    "correo": Resultado_general_convenio["correo"],
    

    # desde movimientos
    "adiciones": adiciones,
    "ampliaciones": ampliaciones,
    "suspensiones": suspensiones,
    "otrosi":otro_si,
    "valorinicialnumero":Resultados_movimientos_convenios["valor_inicial_convenio"],
    "fechainicial": Resultados_movimientos_convenios["fecha_inicial_convenio"],
    "fechafinal": Resultados_movimientos_convenios["fecha_final_convenio"],
    "totalconvenionombre": Resultados_movimientos_convenios["total_convenio_letra"],

    #Desde imputacion 1
    "financiero": Resultados_imputacion_convenio,
    "pagosacomulados": pagos_acomulados,
    "ejecucion_porcentaje" : ejecucion_convenio,
    "totalcontrato": total_convenio,

    #Desde imputacion 2
    "ejecucion":df_imputacion_contrato,

    # desde polizas
    "polizas": Resultados_polizas_convenio,

    # desde pagos
    "pagos": Resultados_pagos_convenio,

    # desde seguridad
    "seguridad": Resultados_seguridad_convenio,

    # # desde ejecucion
    # "novedad":Resultados_novedades_convenio,


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


        



    






