from num2words import num2words

#Funcion para formatear valor en letras
def formatear_precio(precio):

    precio = num2words(round(precio), lang='es_CO', to='currency')

    return precio