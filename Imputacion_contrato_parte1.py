import pandas as pd

def contrato_funcion(df_doce: pd.DataFrame, contrato: str) -> pd.DataFrame:
    # Convertir columna 'Contrato' a tipo string
    df_doce["Contrato"] = df_doce["Contrato"].astype(str)

    # Filtrar DataFrame basado en condiciones
    df_imputacion = df_doce.loc[
        (~df_doce["CCosto"].astype(str).str.startswith("1")) &
        (~df_doce["Nombre Rubro"].str.contains("GMF|GRAVAMEN|HONORARIOS/CONSULTORÍAS|SEGUROS GENERALES|SERVICIOS TÉCNICOS", case=False, na=False)) &
        (df_doce["Contrato"].str.contains(fr"^{contrato}", na=False)) &
        (df_doce["Fecha"] != "01/01/2024")
    ]

    # Filtrar por 'Tipo Documento' y agrupar
    df_groups = {tipo: df_imputacion[df_imputacion["Tipo Documento"] == tipo].groupby("Compromiso", as_index=False).agg({"Valor": "sum"}) 
                  for tipo in ["EPG", "ECX", "EPX"]}

    df_ECO = df_imputacion[df_imputacion["Tipo Documento"] == "ECO"]

    # Agrupar 'df_imputacion' por varias columnas
    df_imputacion = df_ECO.groupby(["Contrato", "Numero", "Convenio", "CCosto", "Nombre Rubro"], as_index=False).agg({
        "Fuente Financiacion": lambda x: ', '.join(set(map(str, x))),
        "Disponibilidad": lambda x: ', '.join(set(map(str, x))),
        "Valor": "sum",
    })

    # Unir DataFrames por 'Numero'
    for tipo in ["EPG", "EPX", "ECX"]:
        df_final = pd.merge(df_imputacion, df_groups[tipo], how='left', left_on="Numero", right_on="Compromiso", suffixes=('', f'_{tipo}'))
        df_imputacion = df_final



    # Limpiar columnas y calcular saldo
    df_final = df_final.drop(columns=["Compromiso","Compromiso_ECX","Compromiso_EPX"])
    df_final = df_final.fillna(0)
    df_final["Saldo"] = ((df_final["Valor"] - df_final["Valor_ECX"])-(df_final["Valor_EPG"]-df_final["Valor_EPX"]))
    
    return df_final