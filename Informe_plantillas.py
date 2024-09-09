
import os
from medir_tiempo import medir_tiempo


def plantillas(tipo):

    ruta_plantilla = f"../Datalake/Plantillas/"

    archivos = []

    if tipo == "Contrato":
        plantilla1 = os.path.join(ruta_plantilla,"Plantilla5.docx")
        plantilla2 = os.path.join(ruta_plantilla,"Plantilla6.docx")
        archivos.extend([plantilla1, plantilla2])
    elif tipo == "Convenio":
        plantilla1 = os.path.join(ruta_plantilla,"Plantilla7.docx")
        plantilla2 = os.path.join(ruta_plantilla,"Plantilla8.docx")
        archivos.extend([plantilla1, plantilla2])
    
    return archivos