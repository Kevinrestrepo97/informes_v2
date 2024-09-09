from Format_fecha import formatear_fecha
from Format_precio import formatear_precio

def movimientos_general(df_dict:dict,contrato:str):

    adiciones = []
    ampliaciones = []
    suspensiones = []
    financiero = []
    otro_si = []

    df_movimientos = df_dict["Movimientos"]

    df_movimientos = df_movimientos.loc[df_movimientos["Contrato"] == contrato]


    Resultados_movimientos_contratos ={

    "fecha_inicial_contrato":  formatear_fecha(df_movimientos["Inicio_orden_clausula"].min()),
    "fecha_final_contrato":  formatear_fecha(df_movimientos["Fin_orden_clausula"].min()),
    "total_contrato_letra":  f'{formatear_precio(df_movimientos["Valor_orden_clausula"].sum())} $ ({df_movimientos["Valor_orden_clausula"].sum():,.0f})',
    "valor_inicial_contrato":  f'{df_movimientos.loc[df_movimientos["Inicio_orden_clausula"] == df_movimientos["Inicio_orden_clausula"].min(),
                                                "Valor_orden_clausula"].iloc[0]:,.0f}'
        }
    
    for row in df_movimientos.itertuples(index=False):
        columnas = row._asdict()
 
        # Condiciones de iteración
        if columnas['Movimiento_orden_clausula'] == "ADICION":
            adiciones.append({
                "Columna1": f'{columnas["Movimiento_orden_clausula"]} {columnas["Tipo_orden_clausula"]} {columnas["Orden_clausula"]}',
                "Columna2": f'{formatear_precio(columnas["Valor_orden_clausula"])} $ ({columnas["Valor_orden_clausula"]:,.0f}) Incluido {columnas["Impuesto_orden_clausula"]}'
                })
        
        elif columnas['Movimiento_orden_clausula'] == "AMPLIACION":
            ampliaciones.append({
                "Columna1": f'{columnas["Movimiento_orden_clausula"]} {columnas["Tipo_orden_clausula"]} {columnas["Orden_clausula"]}',
                "Columna2": f"Desde el {formatear_fecha(columnas["Inicio_orden_clausula"])}, Hasta el {formatear_fecha(columnas["Fin_orden_clausula"])}"
            })

        elif columnas['Movimiento_orden_clausula'] == "SUSPENSION":
            suspensiones.append({
                "Columna1": f'{columnas["Movimiento_orden_clausula"]} {columnas["Tipo_orden_clausula"]} {columnas["Orden_clausula"]}',
                "Columna2": f"Desde el {formatear_fecha(columnas["Inicio_orden_clausula"])}, Hasta el {formatear_fecha(columnas["Fin_orden_clausula"])}"
            })

        elif columnas['Movimiento_orden_clausula'] == "INICIO" or columnas['Movimiento_orden_clausula'] == "ADICION Y AMPLIACION":
            adiciones.append({
                "Columna1": f'{columnas["Movimiento_orden_clausula"]} {columnas["Tipo_orden_clausula"]} {columnas["Orden_clausula"]}',
                "Columna2": f'{formatear_precio(columnas["Valor_orden_clausula"])} $ ({columnas["Valor_orden_clausula"]:,.0f}) Incluido {columnas["Impuesto_orden_clausula"]}'
                })
            ampliaciones.append({
                "Columna1": f'{columnas["Movimiento_orden_clausula"]} {columnas["Tipo_orden_clausula"]} {columnas["Orden_clausula"]}',
                "Columna2": f"Desde el {formatear_fecha(columnas["Inicio_orden_clausula"])}, Hasta el {formatear_fecha(columnas["Fin_orden_clausula"])}"
            })
        elif columnas['Movimiento_orden_clausula'] == "OTRO SI":
            otro_si.append({
                "Columna1": f'{columnas["Movimiento_orden_clausula"]} {columnas["Tipo_orden_clausula"]} {columnas["Orden_clausula"]}',
                "Columna2": f"{columnas["Observaciones"]}"
            })


    return adiciones,ampliaciones,suspensiones,otro_si,Resultados_movimientos_contratos