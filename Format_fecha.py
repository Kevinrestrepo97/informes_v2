import pandas as pd

#Funcion para establecer tipo de fecha
def formatear_fecha(fecha:str):

    Fecha = fecha.strftime('%d de %B de %Y')

    return Fecha

