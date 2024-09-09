import time

tiempos = {}

def medir_tiempo(funcion):
    def wrapper(*args,**kwargs):
        inicio = time.time()
        resultado = funcion(*args,**kwargs)
        fin = time.time()
        ejecucion = fin-inicio
        tiempos[funcion.__name__] = ejecucion
        print(f"Tiempo de ejecución de {funcion.__name__}: {ejecucion:.6f} segundos")
        return resultado
    return wrapper

