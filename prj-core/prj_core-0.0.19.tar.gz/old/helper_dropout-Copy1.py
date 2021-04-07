import pandas as pd
import numpy as np
from functools import reduce
from simpledbf import Dbf5
import gc
import time
import os

def get_variables_altamente_correlacionadas(X_train):
    threshold = 0.9
    # Absolute value correlation matrix
    corr_matrix = X_train.corr().abs()
    upper = corr_matrix.where(np.triu(np.ones(corr_matrix.shape), k=1).astype(np.bool))
    to_drop = [column for column in upper.columns if any(upper[column] > threshold)]
    return to_drop

def get_participacion_juntos_por_anio(anio):       
    dtypes_columns = {
                      'ID_PERSONA':int,#nurvo
                      'JUNTOS':int,
                      }           
    columns_n_ = ['ID_PERSONA','JUNTOS'] 
    if(anio<2019):
        url = "../PROYECTO_AVISE/00.CARGA/00.HOMOGENEO_NOMINAL_SIAGIE/NOMINAL_{}.csv"
        df = pd.read_csv(url.format(anio), usecols=columns_n_,encoding="latin-1",sep="|",dtype=dtypes_columns)
    else:
        list_df = []
        for nivel in ["A0","B0","F0"]:
            url = "../PROYECTO_AVISE/00.CARGA/00.HOMOGENEO_NOMINAL_SIAGIE/NOMINAL_{}_{}.csv"
            ds_2020 = pd.read_csv(url.format(nivel,anio), usecols=columns_n_,encoding="latin-1",
                                  sep="|",dtype=dtypes_columns)
            list_df.append(ds_2020)
        df = pd.concat(list_df)
    return df


def get_situacion_final_recuperacion_por_anio(anio):       
    dtypes_columns = {
                      'ID_PERSONA':int,#nurvo
                      'SITUACION_FINAL':str,
                      'SF_RECUPERACION':str,
                      }           
    columns_n_ = ['ID_PERSONA','SITUACION_FINAL','SF_RECUPERACION'] 
    if(anio<2019):
        url = "../PROYECTO_AVISE/00.CARGA/00.HOMOGENEO_NOMINAL_SIAGIE/NOMINAL_{}.csv"
        df = pd.read_csv(url.format(anio), usecols=columns_n_,encoding="latin-1",sep="|",dtype=dtypes_columns)
    else:
        list_df = []
        for nivel in ["A0","B0","F0"]:
            url = "../PROYECTO_AVISE/00.CARGA/00.HOMOGENEO_NOMINAL_SIAGIE/NOMINAL_{}_{}.csv"
            ds_2020 = pd.read_csv(url.format(nivel,anio), usecols=columns_n_,encoding="latin-1",
                                  sep="|",dtype=dtypes_columns)
            list_df.append(ds_2020)
        df = pd.concat(list_df)
    return df

def generar_kpis_sfr(df,ANIO,T_ANIOS):
    
    ID_PERSONA_SERIES = df['ID_PERSONA']
    ultimo_anio =ANIO- T_ANIOS

    num = 1
    list_df_m_tras = []
    cols_to_sum_des = []
    cols_to_sum_ret = []
    cols_to_drop = []
    ANIO = ANIO-1
    for anio in range(ANIO,ultimo_anio,-1):
        if(anio<=2013):
            break
        col_name_des="DESAPROBADO_T"
        col_name_ret="RETIRADO_T"
        
        if(num>0):
            posfix="_MENOS_{}".format(num)
            col_name_des = col_name_des+posfix
            col_name_ret = col_name_ret+posfix
            
        cols_to_drop.append(col_name_des)
        cols_to_drop.append(col_name_ret)
        
        cols_to_sum_des.append(col_name_des)
        cols_to_sum_ret.append(col_name_ret)
        
        df_m_t = pd.merge(ID_PERSONA_SERIES, get_situacion_final_recuperacion_por_anio(anio),left_on="ID_PERSONA",
                          right_on="ID_PERSONA", how='left')
        
        df_m_t[col_name_des] = np.where((df_m_t['SITUACION_FINAL']=='DESAPROBADO') |
                                                (df_m_t['SF_RECUPERACION']=='DESAPROBADO'),1,0)
        
        df_m_t[col_name_ret] = np.where((df_m_t['SITUACION_FINAL']=='RETIRADO'),1,0)
        
        df_m_t.drop(['SITUACION_FINAL','SF_RECUPERACION'], axis = 1,inplace=True)  

        list_df_m_tras.append(df_m_t)
        num+=1

    df_final = reduce(lambda left,right: pd.merge(left,right,on='ID_PERSONA'), list_df_m_tras)
    df_final['TOTAL_DESAPROBADO'] = df_final[cols_to_sum_des].sum(axis=1)
    df_final['MEAN_DESAPROBADO'] = df_final[cols_to_sum_des].mean(axis=1)
    df_final['STD_DESAPROBADO'] = df_final[cols_to_sum_des].std(axis=1)
    
    
    df_final['TOTAL_RETIRADO'] = df_final[cols_to_sum_ret].sum(axis=1)
    df_final['MEAN_RETIRADO'] = df_final[cols_to_sum_ret].mean(axis=1)
    df_final['STD_RETIRADO'] = df_final[cols_to_sum_ret].std(axis=1)
    
    df_final.drop(cols_to_drop, axis = 1,inplace=True)    
    
    df = pd.merge(df, df_final, left_on=["ID_PERSONA"],  right_on=["ID_PERSONA"],  how='inner')
    
    return df


def generar_kpis_juntos(df,ANIO,T_ANIOS):
    
    ID_PERSONA_SERIES = df['ID_PERSONA']
    ultimo_anio =ANIO- T_ANIOS

    num = 0
    list_df_m_tras = []
    cols_to_sum = []
    cols_to_drop = []
    for anio in range(ANIO,ultimo_anio,-1):
        if(anio<=2013):
            break
        col_name="JUNTOS_T"
        if(num>0):
            posfix="_MENOS_{}".format(num)
            col_name = col_name+posfix
        cols_to_drop.append(col_name)
        cols_to_sum.append(col_name)
        df_m_t = pd.merge(ID_PERSONA_SERIES, get_participacion_juntos_por_anio(anio),left_on="ID_PERSONA",
                          right_on="ID_PERSONA", how='left')
        df_m_t.fillna({'JUNTOS':0}, inplace=True)
        df_m_t.rename(columns={'JUNTOS': col_name}, inplace=True)
        list_df_m_tras.append(df_m_t)
        num+=1

    df_final = reduce(lambda left,right: pd.merge(left,right,on='ID_PERSONA'), list_df_m_tras)
    df_final['TOTAL_JUNTOS'] = df_final[cols_to_sum].sum(axis=1)
    df_final['MEAN_JUNTOS'] = df_final[cols_to_sum].mean(axis=1)
    df_final['STD_JUNTOS'] = df_final[cols_to_sum].std(axis=1)
    df_final.drop(cols_to_drop, axis = 1,inplace=True)    
    
    df = pd.merge(df, df_final, left_on=["ID_PERSONA"],  right_on=["ID_PERSONA"],  how='inner')
    
    return df


def get_desertores_por_anio(anio):
    url = "../PROYECTO_AVISE/01.DESERCION/DESERCION_{}"
    anios_str=str(anio)+"_"+str(anio+1)
    ds_2020 = pd.read_csv(url.format("{}.csv".format(anios_str)))
    #print(anios_str)
    return ds_2020

def generar_kpis_desercion(df,ANIO,T_ANIOS):
    
    ID_PERSONA_SERIES = df['ID_PERSONA']
    ultimo_anio =ANIO- T_ANIOS

    num = 1
    list_df_m_tras = []
    cols_to_sum = []
    cols_to_drop = []
    ANIO = ANIO-1
    for anio in range(ANIO,ultimo_anio,-1):
        if(anio<=2013):
            break
        col_name="DESERTARA_DESPUES_DE_T"
        if(num>0):
            posfix="_MENOS_{}".format(num)
            col_name = col_name+posfix
            cols_to_drop.append(col_name)
        cols_to_sum.append(col_name)
        df_m_t = pd.merge(ID_PERSONA_SERIES, get_desertores_por_anio(anio),left_on="ID_PERSONA",
                          right_on="ID_PERSONA", how='left')
        anios_str=str(anio)+"_"+str(anio+1)
        original_col = "DESERCION_"+anios_str

        df_m_t.fillna({original_col:0}, inplace=True)
        df_m_t.rename(columns={original_col: col_name}, inplace=True)

        list_df_m_tras.append(df_m_t)
        num+=1

    df_final = reduce(lambda left,right: pd.merge(left,right,on='ID_PERSONA'), list_df_m_tras)
    df_final['TOTAL_DESERCIONES'] = df_final[cols_to_sum].sum(axis=1)
    df_final['MEAN_DESERCIONES'] = df_final[cols_to_sum].mean(axis=1)
    df_final['STD_DESERCIONES'] = df_final[cols_to_sum].std(axis=1)
    df_final.drop(cols_to_drop, axis = 1,inplace=True)    
    
    df = pd.merge(df, df_final, left_on=["ID_PERSONA"],  right_on=["ID_PERSONA"],  how='inner')
    
    return df

def get_traslados_por_anio(anio,TIPO_TRASLADO='EN EL MISMO AÑO'):
    url_trasl = '../PROYECTO_AVISE/DATA/DATA_SIAGIE/Siagie_Traslados_{}.txt'.format(anio)
    sep = "|"
    encoding = 'latin-1'
    cols_tras = ['ID_PERSONA','TIPO_TRASLADO']

    #df_trasl = pd.read_csv(url_trasl ,encoding='utf-8',usecols=cols_tras,  sep=sep,dtype={'PERSONA_NRO_DOC':str})
    df_trasl = pd.read_csv(url_trasl ,encoding=encoding,usecols=cols_tras,  sep=sep,dtype={'ID_PERSONA':int})
    #if(anio==2019):
        #df_trasl = df_trasl[df_trasl.TIPO_TRASLADO==TIPO_TRASLADO].copy()
        #df_trasl.reset_index(drop=True,inplace=True)
 
    df_agg_t  = df_trasl.assign(
     TOTAL_TRASLADOS =   1
    ).groupby(['ID_PERSONA']).agg({'TOTAL_TRASLADOS':'sum'})

    df_agg_t.sort_values(by='TOTAL_TRASLADOS', ascending=False,inplace=True)
    df_agg_t.reset_index(inplace=True)
    
    return df_agg_t

def get_traslados_a_publico(anio,df_servicios):
    url_trasl = '../PROYECTO_AVISE/DATA/DATA_SIAGIE/Siagie_Traslados_{}.txt'.format(anio)
    sep = "|"
    encoding = 'latin-1'
    cols_tras = ['ID_PERSONA','TIPO_TRASLADO','COD_MOD_ORIGEN','ANEXO_ORIGEN','COD_MOD_DESTINO','ANEXO_DESTINO']

    cl_s = ["COD_MOD","ANEXO","ES_PUBLICO"]
    #df_trasl = pd.read_csv(url_trasl ,encoding='utf-8',usecols=cols_tras,  sep=sep,dtype={'PERSONA_NRO_DOC':str})
    df_trasl = pd.read_csv(url_trasl ,encoding=encoding,usecols=cols_tras,  sep=sep,dtype={'ID_PERSONA':int,
                                                                                           'COD_MOD_ORIGEN':str,
                                                                                           'ANEXO_ORIGEN':int,
                                                                                           'COD_MOD_DESTINO':str,                                                                                           
                                                                                           'ANEXO_DESTINO':int,
                                                                                            })

    df_trasl_origen = pd.merge(df_trasl,df_servicios[cl_s],left_on=["COD_MOD_ORIGEN","ANEXO_ORIGEN"],
                               right_on=["COD_MOD","ANEXO"],how="inner")

    df_trasl_origen.drop(columns=['COD_MOD', 'ANEXO'],inplace=True)
    df_trasl_origen.rename(columns={'ES_PUBLICO': 'ES_PUBLICO_ORIGEN'}, inplace=True)


    df_trasl_destino = pd.merge(df_trasl_origen,df_servicios[cl_s],left_on=["COD_MOD_DESTINO","ANEXO_DESTINO"],
                               right_on=["COD_MOD","ANEXO"],how="inner")

    df_trasl_destino.drop(columns=['COD_MOD', 'ANEXO'],inplace=True)
    df_trasl_destino.rename(columns={'ES_PUBLICO': 'ES_PUBLICO_DESTINO'}, inplace=True)

    df_trasl_destino['TRASLADO_A_PUBLICO'] = np.where((df_trasl_destino.ES_PUBLICO_ORIGEN==0) & 
                                                      (df_trasl_destino.ES_PUBLICO_DESTINO==1),1,0)


    df_trasl_destino = df_trasl_destino[df_trasl_destino["TRASLADO_A_PUBLICO"]==1].copy()
    
    df_agg_t  = df_trasl_destino.assign(
     TOTAL_TRASLADOS =   1
    ).groupby(['ID_PERSONA']).agg({'TOTAL_TRASLADOS':'sum'})

    df_agg_t.sort_values(by='TOTAL_TRASLADOS', ascending=False,inplace=True)
    df_agg_t.reset_index(inplace=True)
    

    return df_agg_t

def generar_kpis_traslado(df,ANIO,T_ANIOS):
    
    ID_PERSONA_SERIES = df['ID_PERSONA']
    ultimo_anio =ANIO- T_ANIOS

    num = 0
    list_df_m_tras = []
    cols_to_sum = []
    cols_to_drop = []
    for anio in range(ANIO,ultimo_anio,-1):
        if(anio<=2013):
            break
        col_name="TOTAL_TRASLADOS_T"
        if(num>0):
            posfix="_MENOS_{}".format(num)
            col_name = col_name+posfix
            cols_to_drop.append(col_name)
        cols_to_sum.append(col_name)
        df_m_t = pd.merge(ID_PERSONA_SERIES, get_traslados_por_anio(anio),left_on="ID_PERSONA",
                          right_on="ID_PERSONA", how='left')
        df_m_t.fillna({'TOTAL_TRASLADOS':0}, inplace=True)
        df_m_t.rename(columns={'TOTAL_TRASLADOS': col_name}, inplace=True)
        list_df_m_tras.append(df_m_t)
        num+=1

    df_final = reduce(lambda left,right: pd.merge(left,right,on='ID_PERSONA'), list_df_m_tras)
    df_final['TOTAL_TRASLADOS'] = df_final[cols_to_sum].sum(axis=1)
    df_final['MEAN_TRASLADOS'] = df_final[cols_to_sum].mean(axis=1)
    df_final['STD_TRASLADOS'] = df_final[cols_to_sum].std(axis=1)
    df_final.drop(cols_to_drop, axis = 1,inplace=True)    
    
    df = pd.merge(df, df_final, left_on=["ID_PERSONA"],  right_on=["ID_PERSONA"],  how='inner')
    
    return df

def generar_kpis_traslado_a_publico(df,ANIO,T_ANIOS,df_servicios):
    
    ID_PERSONA_SERIES = df['ID_PERSONA']
    ultimo_anio =ANIO- T_ANIOS

    num = 0
    list_df_m_tras = []
    cols_to_sum = []
    cols_to_drop = []
    for anio in range(ANIO,ultimo_anio,-1):
        if(anio<=2013):
            break
        col_name="TOTAL_TRASLADOS_A_PUBLICO_T"
        if(num>0):
            posfix="_MENOS_{}".format(num)
            col_name = col_name+posfix
            cols_to_drop.append(col_name)
        cols_to_sum.append(col_name)
        df_m_t = pd.merge(ID_PERSONA_SERIES, get_traslados_a_publico(anio,df_servicios),left_on="ID_PERSONA",
                          right_on="ID_PERSONA", how='left')
        df_m_t.fillna({'TOTAL_TRASLADOS':0}, inplace=True)
        df_m_t.rename(columns={'TOTAL_TRASLADOS': col_name}, inplace=True)
        list_df_m_tras.append(df_m_t)
        num+=1

    df_final = reduce(lambda left,right: pd.merge(left,right,on='ID_PERSONA'), list_df_m_tras)
    df_final['TOTAL_TRASLADOS_A_PUBLICO'] = df_final[cols_to_sum].sum(axis=1)
    df_final['MEAN_TRASLADOS_A_PUBLICO'] = df_final[cols_to_sum].mean(axis=1)
    df_final['STD_TRASLADOS_A_PUBLICO'] = df_final[cols_to_sum].std(axis=1)
    df_final.drop(cols_to_drop, axis = 1,inplace=True)    
    
    df = pd.merge(df, df_final, left_on=["ID_PERSONA"],  right_on=["ID_PERSONA"],  how='inner')
    
    return df


def agregar_traslado(df,df_t):
    df = pd.merge(df, df_t, left_on=["ID_PERSONA"],  right_on=["ID_PERSONA"],  how='left')
    df.fillna(0,inplace=True)
    df.fillna({'TOTAL_TRASLADOS':0 }, inplace=True)
    return df

def agregar_sisfoh(df,df_sisfoh):
    df = pd.merge(df, df_sisfoh, left_on=["NUMERO_DOCUMENTO_APOD"],
                  right_on=["PERSONA_NRO_DOC"],  how='left')

    df.fillna({'SISFOH_CSE':'OTROS' }, inplace=True)
    del df["PERSONA_NRO_DOC"]
    
    return df


def get_sisfoh():
    url_sisfoh = 'DATA_FASE_1/SISFOH/NOMINAL_SISFOH.csv'
    cols = ['PERSONA_NRO_DOC','SISFOH_CSE']    
    df_sisfoh = pd.read_csv(url_sisfoh ,usecols=cols, encoding='utf-8', dtype={'PERSONA_NRO_DOC':str})
    return df_sisfoh

def get_list_regiones():
    df = get_df_ser_risk("","")
    return df.D_REGION.unique()

def get_df_ser_risk(region,gestion):
    url_ser_risk = 'DATA_FASE_1/SSEE_Desercion.dta'
    df_ser_risk = pd.read_stata(url_ser_risk)
    df_ser_risk = df_ser_risk[df_ser_risk['select']==1]
    df_ser_risk.rename(columns={'cod_mod': 'COD_MOD', 'anexo': 'ANEXO', 'd_region': 'D_REGION'}, inplace=True)
    df_ser_risk['ANEXO'] = df_ser_risk['ANEXO'].astype('uint8') 
    print(df_ser_risk.columns)
    if region!="" or gestion!="":
        if(region!=""):
            df_ser_risk = df_ser_risk[df_ser_risk.D_REGION==region].copy()
            df_ser_risk.reset_index(drop=True,inplace=True)
            
        if(gestion!=""):
            df_ser_risk = df_ser_risk[df_ser_risk.gestion==gestion].copy()
            df_ser_risk.reset_index(drop=True,inplace=True)            
                
        return df_ser_risk
    else:
        return df_ser_risk
    
    
def get_df_ser_risk_old():    
    url_ser_risk_old = 'DATA_FASE_1/Base_Desercion_5.dta'
    df_ser_risk_old = pd.read_stata(url_ser_risk_old)
    df_ser_risk_old = df_ser_risk_old[df_ser_risk_old['uid']==1]
    df_ser_risk_old.rename(columns={'cod_mod': 'COD_MOD', 'anexo': 'ANEXO', 'd_region': 'D_REGION'}, inplace=True)
    #df_ser_risk_old = df_ser_risk_old[['COD_MOD','ANEXO']].copy()
    df_ser_risk_old['ANEXO'] = df_ser_risk_old['ANEXO'].astype('uint8')
    df_ser_risk_old.reset_index(drop=True,inplace=True)    
    return df_ser_risk_old
 

def get_df_notas(anio,region):
    url_notas = 'DATA_FASE_1/notas/{}/NOTAS_POR_ALUMNO_FULL_{}.csv'.format(region,anio)
    df_notas = pd.read_csv(url_notas ,encoding='utf-8', dtype={'COD_MOD':str,'ANEXO':int})
    return df_notas

'''
def get_df_notas(anio):
    url_notas = 'DATA_FASE_1/NOTAS_POR_ALUMNO_{}.csv'.format(anio)
    df_notas = pd.read_csv(url_notas ,encoding='utf-8', dtype={'COD_MOD':str,'ANEXO':int})
    return df_notas
'''

def get_df_por_alum(df_notas_f):

    dataSet_por_alumno = df_notas_f.assign(

     #A3 A2 A5  B0 F0
     NOTA_MATEMATICA_X_ALUMNO =   np.where((df_notas_f['DSC_AREA']=='MATEMÁTICA') &
                                            (df_notas_f['NOTA_AREA_REGULAR']>=0),
                                             df_notas_f['NOTA_AREA_REGULAR'],np.NaN),   

     NOTA_COMUNICACION_X_ALUMNO =   np.where((df_notas_f['DSC_AREA']=='COMUNICACIÓN') &
                                             (df_notas_f['NOTA_AREA_REGULAR']>=0),
                                              df_notas_f['NOTA_AREA_REGULAR'],np.NaN), 
        
     NOTA_OTROS_X_ALUMNO =   np.where((df_notas_f['DSC_AREA']!='MATEMÁTICA') &
                                      (df_notas_f['DSC_AREA']!='COMUNICACIÓN') &
                                            (df_notas_f['NOTA_AREA_REGULAR']>=0),
                                             df_notas_f['NOTA_AREA_REGULAR'],np.NaN), 

    ).groupby(['COD_MOD','ANEXO','ID_PERSONA']).agg({

                                                     'NOTA_MATEMATICA_X_ALUMNO':'mean',
                                                     'NOTA_COMUNICACION_X_ALUMNO':'mean',
                                                     'NOTA_OTROS_X_ALUMNO':'mean',
                                                   })
    

    return dataSet_por_alumno



def get_df_por_grado_serv(df_notas_f):

    dataSet_por_nivel_grado = df_notas_f.assign(   

    ############## mean ##############   
     #A3 A2 A5  B0 F0
     MEAN_NOTA_MATEMATICA_X_CODMOD_NVL_GR =  np.where(df_notas_f['DSC_AREA']=='MATEMÁTICA', 
                                                       df_notas_f['NOTA_AREA_REGULAR'],np.NaN),  
        
     MEAN_NOTA_COMUNICACION_X_CODMOD_NVL_GR = np.where(df_notas_f['DSC_AREA']=='COMUNICACIÓN',
                                                       df_notas_f['NOTA_AREA_REGULAR'],np.NaN),  
        
     MEAN_NOTA_OTROS_X_CODMOD_NVL_GR =   np.where((df_notas_f['DSC_AREA']!='MATEMÁTICA') &
                                                  (df_notas_f['DSC_AREA']!='COMUNICACIÓN') &
                                                  (df_notas_f['NOTA_AREA_REGULAR']>=0),
                                                   df_notas_f['NOTA_AREA_REGULAR'],np.NaN), 

     ############## std ##############   
     #A3 A2 A5  B0 F0
     STD_NOTA_MATEMATICA_X_CODMOD_NVL_GR =   np.where(df_notas_f['DSC_AREA']=='MATEMÁTICA', 
                                                      df_notas_f['NOTA_AREA_REGULAR'],np.NaN),   
     STD_NOTA_COMUNICACION_X_CODMOD_NVL_GR =   np.where(df_notas_f['DSC_AREA']=='COMUNICACIÓN',
                                                        df_notas_f['NOTA_AREA_REGULAR'],np.NaN),  
        
     STD_NOTA_OTROS_X_CODMOD_NVL_GR =   np.where((df_notas_f['DSC_AREA']!='MATEMÁTICA') &
                                                  (df_notas_f['DSC_AREA']!='COMUNICACIÓN') &
                                                  (df_notas_f['NOTA_AREA_REGULAR']>=0),
                                                   df_notas_f['NOTA_AREA_REGULAR'],np.NaN), 


    ).groupby(['COD_MOD','ANEXO']).agg({
                                        'MEAN_NOTA_MATEMATICA_X_CODMOD_NVL_GR':'mean',
                                        'MEAN_NOTA_COMUNICACION_X_CODMOD_NVL_GR':'mean',  
                                        'MEAN_NOTA_OTROS_X_CODMOD_NVL_GR':'mean', 

                                        'STD_NOTA_MATEMATICA_X_CODMOD_NVL_GR':'std',
                                        'STD_NOTA_COMUNICACION_X_CODMOD_NVL_GR':'std',
                                        'STD_NOTA_OTROS_X_CODMOD_NVL_GR':'std',
                                       })
    
    #dataSet_por_nivel_grado['COD_MOD']=dataSet_por_nivel_grado['COD_MOD'].apply(lambda x: '{0:0>7}'.format(x))
    #dataSet_por_nivel_grado['ANEXO']=dataSet_por_nivel_grado['ANEXO'].astype('int')

    return dataSet_por_nivel_grado

def get_df_final_notas_alumn(df_notas_f):
    print(df_notas_f.dtypes)
    df_a = get_df_por_alum(df_notas_f)
    df_a.reset_index(inplace=True)
    df_a['COD_MOD']=df_a['COD_MOD'].apply(lambda x: '{0:0>7}'.format(x))
    df_a['ANEXO']=df_a['ANEXO'].astype('int')

    #dataSet_por_alumno.head()


    dataSet_por_nivel_grado = get_df_por_grado_serv(df_notas_f)
    dataSet_por_nivel_grado.reset_index(inplace=True)
    dataSet_por_nivel_grado['COD_MOD']=dataSet_por_nivel_grado['COD_MOD'].apply(lambda x: '{0:0>7}'.format(x))
    dataSet_por_nivel_grado['ANEXO']=dataSet_por_nivel_grado['ANEXO'].astype('int')
    #dataSet_por_nivel_grado.head()
    #print(df_a.dtypes)
    #print(dataSet_por_nivel_grado.dtypes)

    
    df_a = pd.merge(df_a, dataSet_por_nivel_grado, left_on=["COD_MOD","ANEXO"],  right_on=["COD_MOD","ANEXO"],  how='inner')
    
    z_m = 'Z_NOTA_MAT_T_MENOS_1'
    z_c = 'Z_NOTA_COM_T_MENOS_1'
    z_o = 'Z_NOTA_OTROS_T_MENOS_1'
    
    n_m = 'NOTA_MATEMATICA_X_ALUMNO'
    n_c = 'NOTA_COMUNICACION_X_ALUMNO'
    n_o = 'NOTA_OTROS_X_ALUMNO'

    df_a[z_m] = (df_a[n_m] -df_a['MEAN_NOTA_MATEMATICA_X_CODMOD_NVL_GR'])/df_a['STD_NOTA_MATEMATICA_X_CODMOD_NVL_GR']
    df_a[z_c] = (df_a[n_c] - df_a['MEAN_NOTA_COMUNICACION_X_CODMOD_NVL_GR'])/df_a['STD_NOTA_COMUNICACION_X_CODMOD_NVL_GR']
    df_a[z_o] = (df_a[n_o] - df_a['MEAN_NOTA_OTROS_X_CODMOD_NVL_GR'])/df_a['STD_NOTA_OTROS_X_CODMOD_NVL_GR']
    

    #df_a.fillna(0,inplace=True)
    return df_a




def agregar_notas(df,anio,region):
   
    df_notas = get_df_notas(anio,region)
    
    df_notas_f = pd.merge(df_notas , df['ID_PERSONA'], left_on='ID_PERSONA', 
                       right_on='ID_PERSONA', how='inner')
    
    df_alum_nota = get_df_final_notas_alumn(df_notas_f)
    
    column_j_alum_not = ['COD_MOD','ANEXO','ID_PERSONA']    
    
    #print(df.dtypes)
    #print(df_alum_nota.dtypes)
    
    df_join_model = pd.merge(df , df_alum_nota, left_on=['COD_MOD_T_MENOS_1','ANEXO_T_MENOS_1','ID_PERSONA'], 
                             right_on=column_j_alum_not, how='left',suffixes=('','_x'))
    del df_join_model['COD_MOD_x']
    del df_join_model['ANEXO_x']

    z_m = 'Z_NOTA_MAT_T_MENOS_1'
    z_c = 'Z_NOTA_COM_T_MENOS_1'
    z_o = 'Z_NOTA_OTROS_T_MENOS_1'
    
    agregar_na(df_join_model,z_m)
    agregar_na(df_join_model,z_c)
    agregar_na(df_join_model,z_o)
    
    #df_join_model.fillna(0,inplace=True)
    return df_join_model



def get_df_join_train_eval(idgrado,anio_model,anio_eval,delta,desercion_eval,short):

    if short:
        columns = ["ID_PERSONA","COD_MOD","ANEXO",'COD_MOD_T_MENOS_1','ANEXO_T_MENOS_1']
    else:
        columns = None
    
    #df_sisfoh = get_sisfoh()

    deser_column_model = 'DESERCION_{}_{}'.format(anio_model,anio_model+delta)
    deser_column_eval  = 'DESERCION_{}_{}'.format(anio_eval,anio_eval+delta)
    
    edad_c_model = 'EDAD_AL_{}'.format(anio_model)
    edad_c_eval  = 'EDAD_AL_{}'.format(anio_eval)
    
    url_alumn = 'DATA_FASE_1/nominal/nominal_large_{}_{}_delta_{}.csv'.format(idgrado,anio_model,delta)
    df_alumn = pd.read_csv(url_alumn ,usecols=columns, encoding='utf-8', dtype={'COD_MOD':str,'ANEXO':int,'N_DOC':str,
                                                                 'COD_MOD_T_MENOS_1':str,'ANEXO_T_MENOS_1':int,
                                                                 'NUMERO_DOCUMENTO_APOD':str})
    df_alumn.rename(columns={deser_column_model: 'DESERCION',edad_c_model:'EDAD'}, inplace=True)
  
    

    url_alumn_eval = 'DATA_FASE_1/nominal/nominal_large_{}_{}_delta_{}.csv'.format(idgrado,anio_eval,delta)
    df_alumn_eval = pd.read_csv(url_alumn_eval,usecols=columns ,encoding='utf-8', dtype={'COD_MOD':str,'ANEXO':int,'N_DOC':str,
                                                                           'COD_MOD_T_MENOS_1':str,'ANEXO_T_MENOS_1':int,
                                                                           'NUMERO_DOCUMENTO_APOD':str})
    if desercion_eval:
        df_alumn_eval.rename(columns={deser_column_eval: 'DESERCION',edad_c_eval:'EDAD'}, inplace=True)
    else:
        df_alumn_eval.rename(columns={edad_c_eval:'EDAD'}, inplace=True)
        
    print("url_alumn : ",url_alumn," : ",df_alumn.shape)
    print("url_alumn_eval : ",url_alumn_eval," : ",df_alumn_eval.shape)
    
    return df_alumn, df_alumn_eval

def agregar_na(df,c_name):
    new_c = 'NA_'+c_name 
    df[new_c] = np.where((df[c_name].isna()) , 1 , 0 )

def load_data_correccion(idgrado,anio_model,anio_eval,delta,region,gestion,estrategia,df_sisfoh,df_servicios,df,df_eval):
    
    column_key_serv = ['COD_MOD','ANEXO']
    
    df_ser_risk = get_df_ser_risk(region,gestion)
    #df_ser_risk = get_df_ser_risk_old()
    print("before df_ser_risk: ", df_ser_risk.shape)
    df_ser_risk = pd.merge(df_ser_risk , df_servicios[column_key_serv+['ES_URBANA','ES_PUBLICO','ES_MIXTO']], left_on=column_key_serv, 
                       right_on=column_key_serv, how='inner',suffixes=('','_x'))
    print("before df_ser_risk: ", df_ser_risk.shape)
    df_alumn = df.copy()
    df_alumn_eval = df_eval.copy()

    ## join con servicios en riesgo
    
    
   

    df_alumn.ANEXO = df_alumn.ANEXO.astype(int)
        
    df_ser_risk.ANEXO = df_ser_risk.ANEXO.astype(int)

    column_forein_serv = ['D_REGION','ES_URBANA','ES_PUBLICO','ES_MIXTO']
    df_join = pd.merge(df_alumn , df_ser_risk[column_key_serv+column_forein_serv], left_on=column_key_serv, 
                       right_on=column_key_serv, how='inner',suffixes=('','_x'))
    #print(df_join.columns)

    #############################################################
    #join con notas: model

    
    anio_model_menos_1 = anio_model -1
    
    df_join_model = agregar_notas(df_join,anio_model_menos_1,region)
    
  
    ##### eval ##########
    
    
    df_join_eval = pd.merge(df_alumn_eval , df_ser_risk[column_key_serv+column_forein_serv], 
                            left_on=column_key_serv,right_on=column_key_serv, how='inner',suffixes=['','_x'])

    #join con notas: eval
    anio_eval_menos_1 = anio_eval-1
    
    df_join_new_eval = agregar_notas(df_join_eval,anio_eval_menos_1,region)
    
    
    c = ['ID_PERSONA',
         'Z_NOTA_MAT_T_MENOS_1','NA_Z_NOTA_MAT_T_MENOS_1',
         'Z_NOTA_COM_T_MENOS_1','NA_Z_NOTA_COM_T_MENOS_1',
         'Z_NOTA_OTROS_T_MENOS_1','NA_Z_NOTA_OTROS_T_MENOS_1',
         'ES_URBANA','ES_PUBLICO','ES_MIXTO'
        ]
    
    c_to_delete = ['Z_NOTA_MAT_T_MENOS_1','Z_NOTA_COM_T_MENOS_1','Z_NOTA_OTROS_T_MENOS_1']
    
    return df_join_model[c] , df_join_new_eval[c] , c_to_delete



def load_data4(idgrado,anio_model,anio_eval,delta,region,gestion,estrategia,df_sisfoh,df_servicios,df,df_eval):
    
    df_ser_risk = get_df_ser_risk(region,gestion)
    #df_ser_risk = get_df_ser_risk_old()
    
    
    df_alumn = df.copy()
    df_alumn_eval = df_eval.copy()

    ## join con servicios en riesgo
    
    column_key_serv_left = ['COD_MOD','ANEXO']
    column_key_serv_right = ['COD_MOD','ANEXO']


    df_alumn.ANEXO = df_alumn.ANEXO.astype(int)
        
    df_ser_risk.ANEXO = df_ser_risk.ANEXO.astype(int)

    column_forein_serv = ['D_REGION']
    df_join = pd.merge(df_alumn , df_ser_risk[column_key_serv_right+column_forein_serv], left_on=column_key_serv_left, 
                       right_on=column_key_serv_right, how='inner',suffixes=('','_x'))
    #print(df_join.columns)

    #############################################################
    #join con notas: model

    
    anio_model_menos_1 = anio_model -1
    
    df_join_model = agregar_notas(df_join,anio_model_menos_1,region)
    
  
    ##### eval ##########
    
    
    df_join_eval = pd.merge(df_alumn_eval , df_ser_risk[column_key_serv_right+column_forein_serv], left_on=column_key_serv_left, 
                       right_on=column_key_serv_right, how='inner',suffixes=['','_x'])

    #join con notas: eval
    anio_eval_menos_1 = anio_eval-1
    
    df_join_new_eval = agregar_notas(df_join_eval,anio_eval_menos_1,region)
    
      
        
    ################################################

    df_join_model = agregar_sisfoh(df_join_model,df_sisfoh)
    df_join_new_eval = agregar_sisfoh(df_join_new_eval,df_sisfoh)
    
    df_join_model = generar_kpis_traslado(df_join_model,anio_model,7)
    df_join_new_eval = generar_kpis_traslado(df_join_new_eval,anio_eval,7)
    
    df_join_model = generar_kpis_traslado_a_publico(df_join_model,anio_model,7,df_servicios)
    df_join_new_eval = generar_kpis_traslado_a_publico(df_join_new_eval,anio_eval,7,df_servicios)
           
    df_join_model = generar_kpis_desercion(df_join_model,anio_model,7)
    df_join_new_eval = generar_kpis_desercion(df_join_new_eval,anio_eval,7)
    
    df_join_model = generar_kpis_sfr(df_join_model,anio_model,7)
    df_join_new_eval = generar_kpis_sfr(df_join_new_eval,anio_eval,7)
    
           
    df_join_model = generar_kpis_juntos(df_join_model,anio_model,7)
    df_join_new_eval = generar_kpis_juntos(df_join_new_eval,anio_eval,7)
          
    formatear_dias_decimales(df_join_model)    
    formatear_dias_decimales(df_join_new_eval)    
    
    formatear_ES_MUJER(df_join_model)    
    formatear_ES_MUJER(df_join_new_eval)       
    
    formatear_ES_MUJER_APOD(df_join_model)    
    formatear_ES_MUJER_APOD(df_join_new_eval)  
    
    #print(df_join_model.columns)
    formatear_lengua_nacionalidad(df_join_model)    
    formatear_lengua_nacionalidad(df_join_new_eval)      
    
    formatear_TIENE_DNI(df_join_model)    
    formatear_TIENE_DNI(df_join_new_eval)       
    
    formatear_TIENE_DISCAPACIDAD(df_join_model)    
    formatear_TIENE_DISCAPACIDAD(df_join_new_eval)    
        
    formatear_NO_VIVE_ALGUN_PADRE(df_join_model)    
    formatear_NO_VIVE_ALGUN_PADRE(df_join_new_eval)       
    
    formatear_TIENE_PADRES_COMO_APODERADO(df_join_model)    
    formatear_TIENE_PADRES_COMO_APODERADO(df_join_new_eval)  

    formatear_TIENE_TRABAJO(df_join_model)    
    formatear_TIENE_TRABAJO(df_join_new_eval)  
    
    
    return df_join_model , df_join_new_eval


def formatear_TIENE_TRABAJO(df):
    df['TIENE_TRABAJO'] = np.where((df.TRABAJA==1) | (df.HORAS_SEMANALES_TRABAJO>0) , 1 , 0 )
    df.drop(['TRABAJA','HORAS_SEMANALES_TRABAJO'], axis = 1,inplace=True) 
    

def formatear_TIENE_PADRES_COMO_APODERADO(df):
    df['TIENE_PADRES_COMO_APODERADO'] = np.where((df.PARENTESCO=="MADRE") | (df.PARENTESCO=="PADRE") , 1 , 0 )
    df.drop(['PARENTESCO'], axis = 1,inplace=True) 

def formatear_NO_VIVE_ALGUN_PADRE(df):
    df['NO_VIVE_ALGUN_PADRE'] = np.where((df.PADRE_VIVE=="NO") | (df.MADRE_VIVE=="NO") , 1 , 0 )
    df.drop(['PADRE_VIVE','MADRE_VIVE'], axis = 1,inplace=True) 

def formatear_TIENE_DISCAPACIDAD(df):
    df['TIENE_DISCAPACIDAD'] = np.where((df.DSC_DISCAPACIDAD!=0) | (df.TIENE_CERTIFICADO_DISCAPACIDAD=="SI") , 1 , 0 )
    df.drop(['DSC_DISCAPACIDAD','TIENE_CERTIFICADO_DISCAPACIDAD'], axis = 1,inplace=True) 

def formatear_TIENE_DNI(df):
    df['TIENE_DNI'] = np.where(df.N_DOC==0 , 0 , 1 )
    #df.drop(['EDAD_EN_DIAS_T','EDAD'], axis = 1,inplace=True)  

def formatear_dias_decimales(df):
    df['EDAD_EN_DECIMALES_T'] = df.EDAD_EN_DIAS_T/365.25
    df['EDAD_EN_DECIMALES_T'] = df.EDAD_EN_DECIMALES_T.round(2)
    df.drop(['EDAD_EN_DIAS_T','EDAD'], axis = 1,inplace=True)  

def formatear_ES_MUJER(df):
    df['ES_MUJER'] = np.where(df.SEXO=="MUJER" , 1 , 0 )
    df.drop(['SEXO'], axis = 1,inplace=True)  
    
def formatear_ES_MUJER_APOD(df):
    df['ES_MUJER_APOD'] = np.where(df.SEXO_APOD=="MUJER" , 1 , 0 )
    df.drop(['SEXO_APOD'], axis = 1,inplace=True) 

def formatear_lengua_nacionalidad(df):
    df['ES_LENGUA_CASTELLANA'] = np.where(df.DSC_LENGUA=="CASTELLANO" , 1 , 0 )
    df['ES_PERUANO'] = np.where(df.DSC_PAIS.str.startswith('Per', na=False) , 1 , 0 )    
    #df.drop(['DSC_LENGUA','DSC_PAIS'], axis = 1,inplace=True)  
    
    

def limpiar_SITUACION_FINAL_T_MENOS_1(df):
    df.loc[df['SITUACION_MATRICULA_T'] == 'REENTRANTE', 'SITUACION_FINAL_T_MENOS_1'] = 'RETIRADO' 
    
    df.loc[(df['SITUACION_MATRICULA_T'] == 'PROMOVIDO') & 
           (df['SITUACION_FINAL_T_MENOS_1'] == 'MATRICULADO') , 'SITUACION_FINAL_T_MENOS_1'] = 'APROBADO' 

    df.loc[(df['SITUACION_MATRICULA_T'] == 'PROMOVIDO') & 
           (df['SITUACION_FINAL_T_MENOS_1'] == 'DESAPROBADO') , 'SITUACION_FINAL_T_MENOS_1'] = 'APROBADO' 
    
    df.loc[(df['SITUACION_MATRICULA_T'] == 'PROMOVIDO') & 
           (df['SITUACION_FINAL_T_MENOS_1'] == 'SIN EVALUAR CALLAO') , 'SITUACION_FINAL_T_MENOS_1'] = 'APROBADO' 
    
        
    df.loc[(df['SITUACION_MATRICULA_T'] == 'PROMOVIDO') & 
           (df['SITUACION_FINAL_T_MENOS_1'] == 'FALLECIDO') , 'SITUACION_FINAL_T_MENOS_1'] = 'APROBADO' 
    
    df.loc[(df['SITUACION_MATRICULA_T'] == 'PROMOVIDO') & 
           (df['SITUACION_FINAL_T_MENOS_1'] == 'POSTERGACION') , 'SITUACION_FINAL_T_MENOS_1'] = 'APROBADO' 

    df.loc[(df['SITUACION_MATRICULA_T'] == 'REPITE') & 
           (df['SITUACION_FINAL_T_MENOS_1'] == 'APROBADO') , 'SITUACION_FINAL_T_MENOS_1'] = 'DESAPROBADO' 

    df.loc[(df['SITUACION_MATRICULA_T'] == 'REPITE') & 
           (df['SITUACION_FINAL_T_MENOS_1'] == 'MATRICULADO') , 'SITUACION_FINAL_T_MENOS_1'] = 'RETIRADO' 

    
    
    
    
def fe_df(df_join,df_join_eval):

    df_join.rename(columns={'COD_MOD': 'COD_MOD_T','ANEXO':'ANEXO_T'}, inplace=True)
    df_join_eval.rename(columns={'COD_MOD': 'COD_MOD_T','ANEXO':'ANEXO_T'}, inplace=True)
        
    df_join['DESERCION_T_MENOS_1__T'] = np.where((df_join['COD_MOD_T']=="000000") , 1 , 0 )
    #print("rarooooooooooooooooo")
    #print(df_join_eval.columns)
    df_join_eval['DESERCION_T_MENOS_1__T'] = np.where((df_join_eval['COD_MOD_T']=="000000") , 1 , 0 )
    
    ######  limpiar columnas ######################
    if 'SITUACION_MATRICULA_T' in df_join.columns:        
        df_join['SITUACION_MATRICULA_T'] = df_join['SITUACION_MATRICULA_T'].astype('str')
        df_join['SITUACION_MATRICULA_T'] = df_join['SITUACION_MATRICULA_T'].str.strip()
        
    if 'SITUACION_MATRICULA_T' in df_join_eval.columns:        
        df_join_eval['SITUACION_MATRICULA_T'] = df_join_eval['SITUACION_MATRICULA_T'].astype('str')
        df_join_eval['SITUACION_MATRICULA_T'] = df_join_eval['SITUACION_MATRICULA_T'].str.strip()
        
        #df_join_eval.loc[df_join_eval['SITUACION_MATRICULA'] == '0', 'SITUACION_MATRICULA'] = 'PROMOVIDO' 
        
    if 'SITUACION_MATRICULA_T_MENOS_1' in df_join.columns:        
        df_join['SITUACION_MATRICULA_T_MENOS_1'] = df_join['SITUACION_MATRICULA_T_MENOS_1'].astype('str')
        df_join['SITUACION_MATRICULA_T_MENOS_1'] = df_join['SITUACION_MATRICULA_T_MENOS_1'].str.strip()
        df_join.loc[df_join['SITUACION_MATRICULA_T_MENOS_1'] == '0', 'SITUACION_MATRICULA_T_MENOS_1'] = 'PROMOVIDO' 

    if 'SITUACION_MATRICULA_T_MENOS_1' in df_join_eval.columns:        
        df_join_eval['SITUACION_MATRICULA_T_MENOS_1'] = df_join_eval['SITUACION_MATRICULA_T_MENOS_1'].astype('str')
        df_join_eval['SITUACION_MATRICULA_T_MENOS_1'] = df_join_eval['SITUACION_MATRICULA_T_MENOS_1'].str.strip()
        df_join_eval.loc[df_join_eval['SITUACION_MATRICULA_T_MENOS_1'] == '0', 'SITUACION_MATRICULA_T_MENOS_1'] = 'PROMOVIDO' 
    
    
    limpiar_SITUACION_FINAL_T_MENOS_1(df_join)
    limpiar_SITUACION_FINAL_T_MENOS_1(df_join_eval) 
        
    if 'SF_RECUPERACION_T_MENOS_1' in df_join.columns:         
        df_join['SF_RECUPERACION_T_MENOS_1'] = df_join['SF_RECUPERACION_T_MENOS_1'].astype('str')
        df_join['SF_RECUPERACION_T_MENOS_1'] = df_join['SF_RECUPERACION_T_MENOS_1'].str.strip()       


    if 'SF_RECUPERACION_T_MENOS_1' in df_join_eval.columns:    
        df_join_eval['SF_RECUPERACION_T_MENOS_1'] = df_join_eval['SF_RECUPERACION_T_MENOS_1'].astype('str')
        df_join_eval['SF_RECUPERACION_T_MENOS_1'] = df_join_eval['SF_RECUPERACION_T_MENOS_1'].str.strip()

        
    if 'SF_RECUPERACION' in df_join.columns:         
        df_join['SF_RECUPERACION'] = df_join['SF_RECUPERACION'].astype('str')
        df_join['SF_RECUPERACION'] = df_join['SF_RECUPERACION'].str.strip()        
        
    if 'SF_RECUPERACION' in df_join_eval.columns:    
        df_join_eval['SF_RECUPERACION'] = df_join_eval['SF_RECUPERACION'].astype('str')
        df_join_eval['SF_RECUPERACION'] = df_join_eval['SF_RECUPERACION'].str.strip()        
        
    if 'NIVEL_INSTRUCCION_APOD' in df_join.columns:  
        
        df_join['NIVEL_INSTRUCCION_APOD'].fillna('OTRO', inplace=True)
        df_join_eval['NIVEL_INSTRUCCION_APOD'].fillna('OTRO', inplace=True)

        df_join['NIVEL_INSTRUCCION_APOD'] = df_join['NIVEL_INSTRUCCION_APOD'].astype('str')
        df_join['NIVEL_INSTRUCCION_APOD'] = df_join['NIVEL_INSTRUCCION_APOD'].str.strip()

        df_join_eval['NIVEL_INSTRUCCION_APOD'] = df_join_eval['NIVEL_INSTRUCCION_APOD'].astype('str')
        df_join_eval['NIVEL_INSTRUCCION_APOD'] = df_join_eval['NIVEL_INSTRUCCION_APOD'].str.strip()

        ##### crear variables derivadas ###############

        anios_esc = {'NINGUNO':0,              
                     'OTRO':0,
                     'PRIMARIA INCOMPLETA':4,
                     'PRIMARIA COMPLETA':6,
                     'SECUNDARIA INCOMPLETA':9,
                     'SECUNDARIA COMPLETA':11,
                     'SUPERIOR NO UNIV.INCOMPLETA':14,
                     'SUPERIOR NO UNIV.COMPLETA':16,
                     'SUPERIOR UNIV.INCOMPLETA':14,
                     'SUPERIOR UNIV.COMPLETA':16,
                     'SUPERIOR POST GRADUADO':20
                    }

        t_edc_apo = {'NINGUNO':'NINGUNO',              
                     'OTRO':'NINGUNO',
                     'PRIMARIA INCOMPLETA':'BASICA_INCOMPLETA',
                     'PRIMARIA COMPLETA':'BASICA_INCOMPLETA',
                     'SECUNDARIA INCOMPLETA':'BASICA_INCOMPLETA',
                     'SECUNDARIA COMPLETA':'BASICA_COMPLETA',
                     'SUPERIOR NO UNIV.INCOMPLETA':'SUPERIOR_INCOMPLETA',  
                     'SUPERIOR UNIV.INCOMPLETA':'SUPERIOR_INCOMPLETA',  
                     'SUPERIOR NO UNIV.COMPLETA':'SUPERIOR_COMPLETA',            
                     'SUPERIOR UNIV.COMPLETA':'SUPERIOR_COMPLETA',
                     'SUPERIOR POST GRADUADO':'SUPERIOR_COMPLETA',
                    }


        df_join['ANIOS_ESCOLARIDAD_APOD'] = df_join['NIVEL_INSTRUCCION_APOD'].map(anios_esc)
        df_join_eval['ANIOS_ESCOLARIDAD_APOD'] = df_join_eval['NIVEL_INSTRUCCION_APOD'].map(anios_esc)

        df_join['ANIOS_ESCOLARIDAD_APOD'].fillna(0, inplace=True)
        df_join_eval['ANIOS_ESCOLARIDAD_APOD'].fillna(0, inplace=True)
      
        
        df_join['NIVEL_INSTRUCCION_APOD_SHORT'] = df_join['NIVEL_INSTRUCCION_APOD'].map(t_edc_apo)
        df_join_eval['NIVEL_INSTRUCCION_APOD_SHORT'] = df_join_eval['NIVEL_INSTRUCCION_APOD'].map(t_edc_apo)

        df_join['NIVEL_INSTRUCCION_APOD_SHORT'] = df_join['NIVEL_INSTRUCCION_APOD_SHORT'].astype('str')
        df_join['NIVEL_INSTRUCCION_APOD_SHORT'] = df_join['NIVEL_INSTRUCCION_APOD_SHORT'].str.strip()

        df_join_eval['NIVEL_INSTRUCCION_APOD_SHORT'] = df_join_eval['NIVEL_INSTRUCCION_APOD_SHORT'].astype('str')
        df_join_eval['NIVEL_INSTRUCCION_APOD_SHORT'] = df_join_eval['NIVEL_INSTRUCCION_APOD_SHORT'].str.strip()
    

    
def get_df_servicios():
    dbf_ser = Dbf5("DATA_FASE_1/Padron_web.dbf", codec='ISO-8859-1')
    df_servicios = dbf_ser.to_dataframe()
    df_servicios = df_servicios[["COD_MOD","ANEXO","CODGEO","CODCCPP","GESTION","DAREACENSO",'D_TIPSSEXO']].copy() 
    df_servicios["ANEXO"] =df_servicios['ANEXO'].astype("int8")
    df_servicios["GESTION"] =df_servicios['GESTION'].astype("int8")    

    #df_servicios["AREA_CENSO"] =df_servicios['AREA_CENSO'].astype("int8")
    df_servicios['ES_PUBLICO'] = np.where(df_servicios['GESTION'].isin([1,2]),1,0)
    df_servicios['ES_URBANA'] = np.where(df_servicios['DAREACENSO']=='Urbana',1,0)
    df_servicios['ES_MIXTO'] = np.where(df_servicios['D_TIPSSEXO']=='Mixto',1,0)
    df_servicios['COD_MOD']=df_servicios['COD_MOD'].apply(lambda x: '{0:0>7}'.format(x))

    
    return df_servicios
'''    
def get_shock_economico(anio):
    columns_n = ["id_persona","id_hog_imp_f","log_ing_t_mas_1_imp_dist"]
    #columns_n = ["id_persona","log_ing_t_imp_dist","p_t_mas_1_hat"]    
    url = "workfile_{}.csv".format(anio)
    ds_ = pd.read_csv(url,usecols=columns_n) #
    ds_["NA_LOG_ING_T_MAS_1"] = np.where((ds_["id_hog_imp_f"].isna()) , 1 , 0 )
    ds_["LOG_ING_T_MAS_1"] = np.where((ds_["id_hog_imp_f"].isna()) , ds_["id_hog_imp_f"] , ds_["log_ing_t_mas_1_imp_dist"] )
    del ds_["id_hog_imp_f"]
    ds_.columns = [x.upper() for x in ds_.columns]
    return ds_
'''
def get_shock_economico(anio):
    columns_n = ["ID_PERSONA","LOG_ING_T_MAS_1_IMP_DIST"]   
    url = "workfile_{}_v2.csv".format(anio)
    ds_ = pd.read_csv(url,usecols=columns_n) #
    return ds_


def get_distancia_prim_sec():
    
    df_sec_cerca =pd.read_csv("SecundariaCerca.csv", encoding="utf-8",index_col=0) 

    df_sec_cerca.loc[(df_sec_cerca['Distancia'] == 0), 'GRUPO_DISTANCIA'] = '0K'
    df_sec_cerca.loc[(df_sec_cerca['Distancia'] > 0) & (df_sec_cerca['Distancia'] <= 1000), 'GRUPO_DISTANCIA'] = 'MENOR_1K'
    df_sec_cerca.loc[(df_sec_cerca['Distancia'] > 1000) & (df_sec_cerca['Distancia'] <= 5000), 'GRUPO_DISTANCIA'] = '1K_5K'
    df_sec_cerca.loc[(df_sec_cerca['Distancia'] > 5000), 'GRUPO_DISTANCIA'] = 'MAYOR_5K'

    df_sec_cerca.columns = [x.upper() for x in df_sec_cerca.columns]

    df_sec_cerca[['COD_MOD','ANEXO']] = df_sec_cerca.CODIGOLUGAR.str.split("-",expand=True)
    df_sec_cerca['ANEXO'] = df_sec_cerca['ANEXO'].astype('uint8')

    df_sec_cerca['COD_MOD']=df_sec_cerca['COD_MOD'].apply(lambda x: '{0:0>7}'.format(x))
    del df_sec_cerca['SECUNDARIACERCA']
    del df_sec_cerca['CODIGOLUGAR']
    
    
    return df_sec_cerca

def get_hermanos():
    df_hermanos =pd.read_csv("hermanos.csv", encoding="utf-8") 
    return df_hermanos


def incorporar_campos_corregidos(lista_regiones,lista_grados):

    ANIO_MODEL = 2019
    ANIO_EVAL  = 2020 #test real
    
    desercion_eval = False
    delta = 1
    estrategia = 5
    df_sisfoh = None

    df_se = get_shock_economico(ANIO_MODEL)
    df_se2020 = get_shock_economico(ANIO_EVAL)
    df_servicios = get_df_servicios()
    
    #df_dist = get_distancia_prim_sec()
    
    #df_hermanos = get_hermanos()

    for ID_GRADO in lista_grados:   
        
        df , df_eval = get_df_join_train_eval(ID_GRADO,ANIO_MODEL,ANIO_EVAL,delta,desercion_eval,True)

        for region in lista_regiones:
            gc.collect()
            print(region)
            start = time.time()

            url_dir = "{}/{}/".format(region,ID_GRADO)
            
            df_join , df_join_eval , c_to_delete = load_data_correccion(ID_GRADO,ANIO_MODEL,ANIO_EVAL,
                                                                        delta,region,"", estrategia,
                                                                        df_sisfoh,df_servicios,df,df_eval)
            
  
            df_join_sv , df_join_eval_sv = get_saved_join_data(url_dir,sub_dir="out")
            df_join_sv.drop(c_to_delete, axis = 1,inplace=True) 
            df_join_eval_sv.drop(c_to_delete, axis = 1,inplace=True) 

            df_join_f = pd.merge(df_join_sv , df_join, left_on=['ID_PERSONA'],   
                                 right_on=['ID_PERSONA'], how='inner',suffixes=('','_x'))
            
            df_join_eval_f = pd.merge(df_join_eval_sv , df_join_eval, left_on=['ID_PERSONA'],   
                                      right_on=['ID_PERSONA'], how='inner',suffixes=('','_x'))
            
            '''
            print("variables hermanos : ")
            
            print("before df_join_f: ",df_join_f.shape)
            df_join_f = pd.merge(df_join_f , df_hermanos, left_on=['ID_PERSONA'],   
                                 right_on=['ID_PERSONA'], how='left',suffixes=('','_x'))
            print("after df_join_f: ",df_join_f.shape)
            '''
            
            print("variables economicas : ")
            
            print("before df_join_f: ",df_join_f.shape)
            df_join_f = pd.merge(df_join_f , df_se, left_on=['ID_PERSONA'],   
                                 right_on=['ID_PERSONA'], how='inner',suffixes=('','_x'))
            print("after df_join_f: ",df_join_f.shape)
            
            print("before df_join_eval_f: ",df_join_eval_f.shape)
            df_join_eval_f = pd.merge(df_join_eval_f , df_se, left_on=['ID_PERSONA'],   
                                      right_on=['ID_PERSONA'], how='inner',suffixes=('','_x'))
            print("after df_join_eval_f: ",df_join_eval_f.shape)
            
            '''
            print("variables de distancia : ")            
          
            print("before df_join_f: ",df_join_f.shape)
            df_join_f = pd.merge(df_join_f , df_dist, left_on=['COD_MOD','ANEXO'],   
                                 right_on=['COD_MOD','ANEXO'], how='inner',suffixes=('','_x'))
            print("after df_join_f: ",df_join_f.shape)
            
            print("before df_join_eval_f: ",df_join_eval_f.shape)
            df_join_eval_f = pd.merge(df_join_eval_f , df_dist, left_on=['COD_MOD','ANEXO'],   
                                      right_on=['COD_MOD','ANEXO'], how='inner',suffixes=('','_x'))
            print("after df_join_eval_f: ",df_join_eval_f.shape)
            '''
            
            #exportar data 
            exportar_data_innominada(df_join_f,df_join_eval_f,url_dir)
            
def get_saved_join_data(url_dir,sub_dir="data"):
    
    if not url_dir:
        url_dir="reporte_modelo/"+sub_dir+"/"
    else:
        url_dir = '{}/{}'.format("reporte_modelo/"+sub_dir,url_dir)
        if not os.path.exists(url_dir):
            os.makedirs(url_dir)
        print("reporte generado en : "+url_dir)
    
    specific_url = url_dir+"data.csv"
    specific_url_eval = url_dir+"data_eval.csv"
    
    dt = {'COD_MOD':str,'COD_MOD_T':str,'ANEXO':int,'ANEXO_T':int,'EDAD':int,
          'N_DOC':str,'COD_MOD_T_MENOS_1':str,
          'ANEXO_T_MENOS_1':int,'NUMERO_DOCUMENTO_APOD':str,'ID_PERSONA':int}

    df=pd.read_csv(specific_url,dtype=dt, encoding="utf-8") 
    df_eval=pd.read_csv(specific_url_eval,dtype=dt, encoding="utf-8") 
    
    return df,df_eval


def exportar_data_innominada(df_join,df_join_eval,url_dir):
   
    df_join["ID_PERSONA"] = np.random.randint(1,100, df_join.shape[0])
    df_join_eval["ID_PERSONA"] = np.random.randint(1,100, df_join_eval.shape[0])

    df_join["N_DOC"] = np.random.randint(1,100, df_join.shape[0])
    df_join_eval["N_DOC"] = np.random.randint(1,100, df_join_eval.shape[0])

    df_join["NUMERO_DOCUMENTO_APOD"] = np.random.randint(1,100, df_join.shape[0])
    df_join_eval["NUMERO_DOCUMENTO_APOD"] = np.random.randint(1,100, df_join_eval.shape[0])
     
    if not url_dir:
        url_dir="reporte_modelo/data/"  
    else:

        url_dir = '{}/{}'.format("reporte_modelo/data",url_dir)
        if not os.path.exists(url_dir): 
            os.makedirs(url_dir)
        #print("reporte generado en : "+url_dir) 
    
    specific_url = url_dir+"data.csv"
    specific_url_eval = url_dir+"data_eval.csv"
    print("reporte generado en : "+specific_url)
    print("reporte generado en : "+specific_url_eval)
    #df_result_nom_geo[cls_export].to_excel(specific_url,index=False) 
    df_join.to_csv(specific_url,index =False , encoding="utf-8")
    df_join_eval.to_csv(specific_url_eval,index =False , encoding="utf-8")