# -*- coding: utf-8 -*-
"""
Created on Fri Apr  9 00:36:06 2021

@author: User
"""
import pandas as pd
import numpy as np
import src.Prj_Core.core_helper.helper_acces_db as hadb
import src.Prj_Core.core_helper.helper_clean as hc
import src.Prj_Core.core_helper.helper_general as hg

def agregar_sisfoh(df,df_sisfoh=None):    
    
    if df_sisfoh is None:
        df_sisfoh = hadb.get_sisfoh()  
    
    if 'NUMERO_DOCUMENTO_APOD' not in df.columns:
        msg = "ERROR: No existe la columnna NUMERO_DOCUMENTO_APOD en el DF proporcionado"
        raise Exception(msg)
        
    df['NUMERO_DOCUMENTO_APOD'] = df['NUMERO_DOCUMENTO_APOD'].str.replace('.0', '')
    df['NUMERO_DOCUMENTO_APOD']=df['NUMERO_DOCUMENTO_APOD'].apply(lambda x: '{0:0>8}'.format(x))
    df['NUMERO_DOCUMENTO_APOD'] = df['NUMERO_DOCUMENTO_APOD'].str.replace('00000nan', '00000000')     
    
    df = pd.merge(df, df_sisfoh, left_on=["NUMERO_DOCUMENTO_APOD"], right_on=["PERSONA_NRO_DOC"],  how='left')
    df = hc.fill_nan_with_nan_category_in_cls(df , ["SISFOH_CSE"])

    del df["PERSONA_NRO_DOC"]
    
    return df

# solo disponible 2019 y 2021 , B0 y F0
def agregar_shock_economico(df,df_se=None,anio=None,modalidad="EBR"):
    
    if df_se is None:
        df_se = hadb.get_shock_economico(anio,modalidad)
    
    
    df = pd.merge(df, df_se, left_on="ID_PERSONA", right_on="ID_PERSONA",  how='left')

    #df.fillna({'LOG_ING_T_MAS_1_IMP_DIST':0 }, inplace=True)

    return df

'''
dtypes_columns = {'COD_MOD': str,
                  'ANEXO':int,                
                  'COD_MOD_T_MENOS_1':str,
                  'ANEXO_T_MENOS_1':int,                  
                  'UBIGEO_NACIMIENTO_RENIEC':str,
                  'N_DOC':str,
                  'ID_GRADO':int,
                  'ID_PERSONA':int,#nurvo
                  'CODIGO_ESTUDIANTE':str,
                  'NUMERO_DOCUMENTO':str,
                  'NUMERO_DOCUMENTO_APOD':str,
                  'CODOOII':str
                  } 
url = hg.get_base_path()+"\\src\\Prj_Interrupcion_Estudios\\Prj_Desercion\\_02_Preparacion_Datos\\_02_Estructura_Base\\_data_\\nominal\\estructura_base_EBR_{}_{}_delta_1.csv"
url = url.format(5,2019)
df =pd.read_csv(url, dtype=dtypes_columns ,encoding="utf-8")


df = hadb.get_siagie_por_anio(2019,id_grado=5) 
print(df.shape)
df = agregar_shock_economico(df,anio=2019)
print(df.shape)
df_se = hadb.get_shock_economico(2019)
df_temp = df.head(100)
'''