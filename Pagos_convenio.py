from datetime import datetime
import locale
locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
from Format_recorrer_df import recorrer_df
import pandas as pd
from medir_tiempo import medir_tiempo

def pagos_convenio(df_dict:pd.DataFrame,contrato:str):

    df_pagos = df_dict.copy()


    df_pagos = df_pagos.loc[df_pagos["Convenio"] == contrato]

    df_pagos["Valor"] = df_pagos["Valor"].apply(lambda x: f'{x:,.0f}')

    df_pagos.sort_values("Contrato",inplace=True)

    df_pagos = recorrer_df(df_pagos)

    

    return df_pagos