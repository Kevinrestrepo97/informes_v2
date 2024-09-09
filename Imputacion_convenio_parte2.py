import pandas as pd

def contrato_funcion(df_doce: pd.DataFrame, contrato: str, CCosto) -> pd.DataFrame:
    # Convertir columna 'Contrato' a tipo string
    df_doce["Convenio"] = df_doce["Convenio"].astype(str)
    df_doce["Rubro"] = df_doce["Rubro"].str.split("-").str[0]

    # Filtrar DataFrame basado en condiciones
    df_imputacion = df_doce.loc[
        (~df_doce["CCosto"].astype(str).str.startswith("1")) &
        (~df_doce["Nombre Rubro"].str.contains("GMF|GRAVAMEN|HONORARIOS/CONSULTORÍAS|SEGUROS GENERALES|SERVICIOS TÉCNICOS", case=False, na=False)) &
        (df_doce["Convenio"].str.contains(fr"^{contrato}", na=False)) &
        (df_doce["Fecha"] != "01/01/2024") &
        (df_doce["CCosto"]== CCosto)
    ]

    # Filtrar por 'Tipo Documento' y agrupar
    df_groups = {tipo: df_imputacion[df_imputacion["Tipo Documento"] == tipo].groupby(["Compromiso","CCosto","Rubro"], as_index=False).agg({"Valor": "sum"}) 
                  for tipo in ["EPG", "ECX", "EPX"]}

    df_ECO = df_imputacion[df_imputacion["Tipo Documento"] == "ECO"]

    # Agrupar 'df_imputacion' por varias columnas
    df_imputacion = df_ECO.groupby(["Contrato", "Numero", "Convenio", "CCosto", "Nombre Rubro","Rubro"], as_index=False).agg({
        "Fuente Financiacion": lambda x: ', '.join(set(map(str, x))),
        "Disponibilidad": lambda x: ', '.join(set(map(str, x))),
        "Valor": "sum",
    })

    # Unir DataFrames por 'Numero'
    for tipo in ["EPG", "EPX", "ECX"]:
        df_final = pd.merge(df_imputacion, df_groups[tipo], how='left', left_on=["Numero","CCosto","Rubro"], right_on=["Compromiso","CCosto","Rubro"], suffixes=('', f'_{tipo}'))
        df_imputacion = df_final

    df_final["Valor"] = pd.to_numeric(df_final["Valor"], errors='coerce')
    df_final["Valor_ECX"] = pd.to_numeric(df_final["Valor_ECX"], errors='coerce')
    df_final["Valor_EPG"] = pd.to_numeric(df_final["Valor_EPG"], errors='coerce')
    df_final["Valor_EPX"] = pd.to_numeric(df_final["Valor_EPX"], errors='coerce')

        # Opcional: redondear después de la conversión
    df_final["Valor"] = df_final["Valor"].round()
    df_final["Valor_ECX"] = df_final["Valor_ECX"].round()
    df_final["Valor_EPG"] = df_final["Valor_EPG"].round()
    df_final["Valor_EPX"] = df_final["Valor_EPX"].round()

    # Limpiar columnas y calcular saldo
    df_final = df_final.drop(columns=["Compromiso","Compromiso_ECX","Compromiso_EPX"])
    df_final = df_final.fillna(0)
    df_final["Saldo"] = ((df_final["Valor"] - df_final["Valor_ECX"])-(df_final["Valor_EPG"]-df_final["Valor_EPX"]))

    df_final.sort_values("Contrato",inplace=True)
    
    return df_final
