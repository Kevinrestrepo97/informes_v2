import os
import pandas as pd

def concatenado_oficial():
    # Definir las rutas de las carpetas
    carpetas = ['../Formularios_supervision/Logistica','../Formularios_supervision/Tecnologia', '../Formularios_supervision/Vigilancia']

    # Diccionario para almacenar los datos por nombre de archivo y nombre de hoja
    hojas_dict = {}

    # Recorrer cada carpeta
    for carpeta in carpetas:
        for archivo in os.listdir(carpeta):
            if archivo.endswith('.xlsx'):
                ruta_archivo = os.path.join(carpeta, archivo)
                # Leer el archivo Excel
                xls = pd.ExcelFile(ruta_archivo)
                # Recorrer las hojas del archivo
                for hoja in xls.sheet_names:
                    df = pd.read_excel(ruta_archivo, sheet_name=hoja)
                    # Guardar los datos en el diccionario
                    if (archivo, hoja) not in hojas_dict:
                        hojas_dict[(archivo, hoja)] = []
                    hojas_dict[(archivo, hoja)].append(df)
                                

    # Diccionarios para almacenar DataFrames por archivo
    dataframes_por_archivo = {
        'Propuesta_contrato.xlsx': [],
        'Propuesta_convenio.xlsx': []
    }

    # Agregar DataFrames a los diccionarios correspondientes
    for (archivo, hoja), dfs in hojas_dict.items():
        if archivo in dataframes_por_archivo:
            concatenado = pd.concat(dfs, ignore_index=True)  # Concatenar todos los DataFrames para esa hoja
            dataframes_por_archivo[archivo].append((hoja, concatenado))

    ruta = '../Formularios'
    # Guardar cada archivo con sus hojas correspondientes en un solo archivo Excel
    for archivo, hojas in dataframes_por_archivo.items():
        ruta_archivo = os.path.join(ruta, archivo.replace('.xlsx', '1.xlsx'))
        with pd.ExcelWriter(ruta_archivo, engine='openpyxl') as writer:
            for hoja, df in hojas:
                df.to_excel(writer, sheet_name=hoja, index=False)