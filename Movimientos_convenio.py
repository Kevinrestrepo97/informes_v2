from Format_fecha import formatear_fecha
from Format_precio import formatear_precio
from medir_tiempo import medir_tiempo

def movimientos_convenio(df_dict:dict,contrato:str):

    adiciones = []
    ampliaciones = []
    suspensiones = []
    financiero = []
    otro_si = []

    df_movimientos = df_dict["Movimientos"]

    df_movimientos = df_movimientos.loc[df_movimientos["Convenio"] == contrato]

    Resultados_movimientos_convenios ={

    "fecha_inicial_convenio":  formatear_fecha(df_movimientos["Inicio_convenio"].min()),
    "fecha_final_convenio":  formatear_fecha(df_movimientos["Fin_convenio"].min()),
    "total_convenio_letra":  f'{formatear_precio(df_movimientos["Valor_convenio"].sum())} $ ({df_movimientos["Valor_convenio"].sum():,.0f})',
    "valor_inicial_convenio":  f'{df_movimientos.loc[df_movimientos["Inicio_convenio"] == df_movimientos["Inicio_convenio"].min(),
                                                "Valor_convenio"].iloc[0]:,.0f}'
        }
    
    for row in df_movimientos.itertuples(index=False):
        columnas = row._asdict()
 
        # Condiciones de iteración
        if columnas['Movimiento_convenio'] == "ADICION":
            adiciones.append({
                "columna1": f'{columnas["Movimiento_convenio"]} INTERADMINISTRATIVO {columnas["Convenio"]}',
                "columna2": f'{formatear_precio(columnas["Valor_convenio"])} $ ({columnas["Valor_convenio"]:,.0f}) Incluido {columnas["Impuesto_convenio"]}'
                })
        
        elif columnas['Movimiento_convenio'] == "AMPLIACION":
            ampliaciones.append({
                "columna1": f'{columnas["Movimiento_convenio"]} INTERADMINISTRATIVO {columnas["Convenio"]}',
                "columna2": f"Desde el {formatear_fecha(columnas["Inicio_convenio"])}, Hasta el {formatear_fecha(columnas["Fin_convenio"])}"
            })

        elif columnas['Movimiento_convenio'] == "SUSPENSION":
            suspensiones.append({
                "columna1": f'{columnas["Movimiento_convenio"]} INTERADMINISTRATIVO {columnas["Convenio"]}',
                "columna2": f"Desde el {formatear_fecha(columnas["Inicio_convenio"])}, Hasta el {formatear_fecha(columnas["Fin_convenio"])}"
            })

        elif columnas['Movimiento_convenio'] == "INICIO" or columnas['Movimiento_convenio'] == "ADICION Y AMPLIACION":
            adiciones.append({
                "columna1": f'{columnas["Movimiento_convenio"]} INTERADMINISTRATIVO {columnas["Convenio"]}',
                "columna2": f'{formatear_precio(columnas["Valor_convenio"])} $ ({columnas["Valor_convenio"]:,.0f}) Incluido {columnas["Impuesto_convenio"]}'
                })
            ampliaciones.append({
                "columna1": f'{columnas["Movimiento_convenio"]} INTERADMINISTRATIVO {columnas["Convenio"]}',
                "columna2": f"Desde el {formatear_fecha(columnas["Inicio_convenio"])}, Hasta el {formatear_fecha(columnas["Fin_convenio"])}"
            })
        elif columnas['Movimiento_convenio'] == "OTRO SI":
            otro_si.append({
                "columna1": f'{columnas["Movimiento_Convenio"]} INTERADMINISTRATIVO {columnas["Convenio"]}',
                "columna2": f"{columnas["Observaciones"]}"
            })


    return adiciones,ampliaciones,suspensiones,otro_si,Resultados_movimientos_convenios