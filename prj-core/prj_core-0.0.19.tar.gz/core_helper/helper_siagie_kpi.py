# -*- coding: utf-8 -*-
"""
Created on Sun Mar 21 12:21:41 2021

@author: User
"""

import numpy as np
import pandas as pd
from functools import reduce
#from core_helper import helper_acces_db as hadb
import src.Prj_Core.core_helper.helper_acces_db as hadb

from core_helper import helper_dataframe as hdf

import src.Prj_Core.core_helper.helper_clean as hc

def generar_kpis_historicos(df,anio_df=None,anio_h=None,cls_json=None,t_anios=0,modalidad="EBR"):
    
    if(t_anios<=1):            
        print("ERROR: El numero minimo de t_anios debe ser = ",2)        
        return False
    
    ultimo_anio =anio_h- t_anios
    
    if(ultimo_anio<2014):            
        print("ERROR: Se pretende consultar hasta el anio ",ultimo_anio,", solo se tiene data hasta el 2014")        
        return False    
    
    
    if(anio_h>anio_df):            
        print("ERROR: El parametro anio_h no puede ser mayor al parametro anio_h ")        
        return False    
    
    cls_list = []
    for key, value in cls_json.items():
        cls_list.append(key)  
        
    if 'ID_PERSONA' not in cls_list :
        cls_list.append('ID_PERSONA')
        
    print(' '.join(cls_list)) 
    


    ID_PERSONA_SERIES = df['ID_PERSONA']
    

    num = anio_df-anio_h
    list_df_m_tras = []

    
    kpi_final_dic = {}
    print()
    for anio in range(anio_h,ultimo_anio,-1):
        if(anio<=2013):
            break

        
        df_m_t = pd.merge(ID_PERSONA_SERIES, hadb.get_siagie_por_anio(anio,modalidad=modalidad,columns_n=cls_list),left_on="ID_PERSONA",
                          right_on="ID_PERSONA", how='left')
        
        df_m_t = hc.trim_category_cls(df_m_t)
        
        for key, values in cls_json.items():
            if  isinstance(values, list):
                print("category")   
                for val in values:
                    key_val = key+"_"+val
                    if num ==0:
                        cl_pf = key_val+"_T"               
                    else:
                        cl_pf = key_val+"_T_MENOS_{}".format(num)                        
                    df_m_t[cl_pf] = np.where((df_m_t[key]==val),1,0)
                    print(key," - ",cl_pf)
                    if  (key_val in kpi_final_dic) ==False:
                        kpi_final_dic[key_val]=[]                    
                    kpi_final_dic[key_val].append(cl_pf)
                df_m_t.drop([key], axis = 1,inplace=True) 
            elif values=="dummy":      
                print("dummy")
                if num ==0:
                    cl_pf = key+"_T"              
                else:
                    cl_pf = key+"_T_MENOS_{}".format(num)                
                df_m_t[cl_pf] = np.where((df_m_t[key]==1),1,0)
                print(key," - ",cl_pf)
                
                if  (key in kpi_final_dic) ==False:
                    kpi_final_dic[key]=[]                    
                kpi_final_dic[key].append(cl_pf)
                df_m_t.drop([key], axis = 1,inplace=True) 
                
            elif values=="numero":    
                print("numero")                
                if num ==0:
                    cl_pf = key+"_T"              
                else:
                    cl_pf = key+"_T_MENOS_{}".format(num)                
                df_m_t[cl_pf] = df_m_t[key]  
                
                if  (key in kpi_final_dic) ==False:
                    kpi_final_dic[key]=[]                    
                kpi_final_dic[key].append(cl_pf)
                df_m_t.drop([key], axis = 1,inplace=True) 

        list_df_m_tras.append(df_m_t)
        num+=1

    df_final = reduce(lambda left,right: pd.merge(left,right,on='ID_PERSONA'), list_df_m_tras)


    kpi_list = []
    for key, cls_anios in kpi_final_dic.items():
        kpi_list.append(key)   
        df_final = set_generic_kpis(df_final,key,cls_anios)
        #df_final.drop(cls_anios, axis = 1,inplace=True) 
        
    print(' '.join(kpi_list))   

    return df_final


def set_generic_kpis(df,cl_name=None,cl_list=[],set_nan=False):

    if(set_nan==False):
        df['TOTAL_'+cl_name] = df[cl_list].sum(axis=1)
        df['MEAN_'+cl_name] = df[cl_list].mean(axis=1)
        if(len(cl_list)>2):
            df['STD_'+cl_name] = df[cl_list].std(axis=1)
        df['MIN_'+cl_name] = df[cl_list].min(axis=1)
        df['MAX_'+cl_name] = df[cl_list].max(axis=1)
    else:
        df['TOTAL_'+cl_name] = np.nan
        df['MEAN_'+cl_name] = np.nan
        df['STD_'+cl_name] = np.nan
    return df



def agregar_notas(df,anio_df=None,anio_notas=None,df_notas=None,min_alumn_zscore=20):

    if df is None:
        print("ERROR: Debe proporcionar el DF de alumnos")
        return
    
    if 'ID_PERSONA' not in df.columns:
        print("ERROR: El dataframe df no tiene la columna ID_PERSONA")
        return
    
    if anio_df is None:
        print("ERROR: Debe especificar el año del df de alumnos")
        return
    
    if anio_notas is None:
        print("ERROR: Debe especificar el año de las notas")
        return
    
    if anio_notas>anio_df:
        print("ERROR: El anio de notas no puede ser mayor al anio del df de alumnos")
        return
    
    if df_notas is None:
        df_notas = hadb.get_df_notas(anio_notas)
    
    postfix = ""    
    if anio_df== anio_notas:
        postfix ="T"  
    else:
        resta = anio_df - anio_notas
        postfix ="T_MENOS_{}".format(resta)  
    print("postfix : ",postfix)
    print("---------df_notas------------")
    #print(df_notas.dtypes)
    print(df_notas.shape)

    #df_notas = get_df_notas(anio)
    
    #notas del anio n_menos_1 de los alumnos del anio n
    df_notas_f = pd.merge(df_notas , df['ID_PERSONA'], left_on='ID_PERSONA', 
                          right_on='ID_PERSONA', how='inner')
    
    print("---------df_notas_f------------")
    #print(df_notas_f.dtypes)
    print(df_notas_f.shape)
    
    print("Total notas inicial : ",df_notas_f.shape)
    df_ser=df_notas_f.groupby(['COD_MOD', 'ANEXO']).size().reset_index()[['COD_MOD', 'ANEXO']]
    #hay que optener el listado total de alumnos del anio pasado para hacer los group_by respectivos con la data total de n-1.
    #estos alumnos deben pertenecer a los mismos servicios que los alumnos del anio n
    df_notas_alum_n_mes_1 = pd.merge(df_notas , df_ser, left_on=['COD_MOD','ANEXO'], 
                          right_on=['COD_MOD','ANEXO'], how='inner')
    
    df_notas_alum_n_mes_1 = hdf.reduce_mem_usage(df_notas_alum_n_mes_1)
    df_notas_f = hdf.reduce_mem_usage(df_notas_f)
    
    print("---------df_notas_f------------")
    #print(df_notas_f.dtypes)
    print(df_notas_f.shape)
    
    print("---------df_notas_alum_n_mes_1------------")
    #print(df_notas_alum_n_mes_1.dtypes)
    print(df_notas_alum_n_mes_1.shape)
    

    df_alum_nota = get_df_final_notas_alumn(df_notas_f,df_notas_alum_n_mes_1,postfix,min_alumn_zscore)
    print("---------df_alum_nota------------")
    #print(df_alum_nota.dtypes)
    print(df_alum_nota.shape)
    df_alum_nota = hdf.reduce_mem_usage(df_alum_nota)
    #print(df_alum_nota.dtypes)
    print(df_alum_nota.shape)
    
    #column_j_alum_not = ['COD_MOD','ANEXO','ID_PERSONA']  
    column_j_alum_not = ['ID_PERSONA']   
    
    list_area_letter = get_list_area_letter()
    for a_l in list_area_letter:       
        df_alum_nota.rename(columns={get_NC(a_l): get_NC(a_l,postfix)}, inplace=True)
        df_alum_nota.rename(columns={get_MN(a_l): get_MN(a_l,postfix)}, inplace=True)
        df_alum_nota.rename(columns={get_SN(a_l): get_SN(a_l,postfix)}, inplace=True)
        
    df_alum_nota.rename(columns={'TOTAL_CURSOS_X_ALUMNO': 'TOTAL_CURSOS_X_ALUMNO_'+postfix}, inplace=True)                  
    df_alum_nota.rename(columns={'TOTAL_CURSOS_VALIDOS_X_ALUMNO': 'TOTAL_CURSOS_VALIDOS_X_ALUMNO_'+postfix}, inplace=True)                  
    df_alum_nota.rename(columns={'TOTAL_CURSOS_APROBADOS_X_ALUMNO': 'TOTAL_CURSOS_APROBADOS_X_ALUMNO_'+postfix}, inplace=True)                  
    df_alum_nota.rename(columns={'MEAN_CURSOS_X_ALUMNO': 'MEAN_CURSOS_X_ALUMNO_'+postfix}, inplace=True)                  
    df_alum_nota.rename(columns={'STD_CURSOS_X_ALUMNO': 'STD_CURSOS_X_ALUMNO_'+postfix}, inplace=True)                  
          
    del df_alum_nota['TOTAL_ALUMNOS_X_CODMOD_NVL_GR']
    print("---------------------")
    #print(df.dtypes)
    print("---------------------")
    print(df_alum_nota.dtypes)
    print("---------------------")
    
    #df_join_model = pd.merge(df , df_alum_nota, left_on=['COD_MOD_T_MENOS_1','ANEXO_T_MENOS_1','ID_PERSONA'], 
    #                         right_on=column_j_alum_not, how='left',suffixes=('','_x'))
    
    df_join_model = pd.merge(df , df_alum_nota, left_on=['ID_PERSONA'], 
                             right_on=column_j_alum_not, how='left',suffixes=('','_x'))
    
    del df_join_model['COD_MOD_x']
    del df_join_model['ANEXO_x']
    df_join_model = hdf.reduce_mem_usage(df_join_model)
    
    #creando dummy que indica si el zscore esta nullo o no
    list_area_letter = get_list_area_letter()
    for a_l in list_area_letter:
        hc.agregar_na_cls(df_join_model,get_ZN(a_l,postfix))
        

    #df_join_model.fillna(0,inplace=True)
    return df_join_model


def get_df_final_notas_alumn(df_notas_f,df_notas_alum_n_mes_1,postfix,min_alumn):
    #print(df_notas_f.dtypes)
    df_a = get_df_por_alum(df_notas_f)
    df_a.reset_index(inplace=True)
    df_a['COD_MOD']=df_a['COD_MOD'].apply(lambda x: '{0:0>7}'.format(x))
    df_a['ANEXO']=df_a['ANEXO'].astype('int')

    #dataSet_por_alumno.head()

    dataSet_por_nivel_grado_serv, dataSet_por_nivel_grado = get_df_por_grado_serv(df_notas_alum_n_mes_1)
    
    #print(dataSet_por_nivel_grado)
    
    dataSet_por_nivel_grado_serv.reset_index(inplace=True)
    dataSet_por_nivel_grado_serv['COD_MOD']=dataSet_por_nivel_grado_serv['COD_MOD'].apply(lambda x: '{0:0>7}'.format(x))
    dataSet_por_nivel_grado_serv['ANEXO']=dataSet_por_nivel_grado_serv['ANEXO'].astype('int')
    #dataSet_por_nivel_grado.head()
    #print(df_a.dtypes)
    print("**********************************")
    #print(dataSet_por_nivel_grado_serv.dtypes)

    #print("df_a 1>",df_a.shape)
    df_a = pd.merge(df_a, dataSet_por_nivel_grado_serv, left_on=["COD_MOD","ANEXO"],  right_on=["COD_MOD","ANEXO"],  how='inner')
    #print("df_a 2>",df_a.shape)
    
    list_area_letter = get_list_area_letter()

    #calculamos el z score por alumno a nivel de grado servicio
    for a_l in list_area_letter:
        df_a[get_ZN(a_l,postfix)] = (df_a[get_NC(a_l)] - df_a[get_MN(a_l)])/df_a[get_SN(a_l)]
    
    #si el zscore no se puede calcular por el numero de alumnos a nivel de grado servicio, 
    #entonces se calculara a nivel de grado region
    #adicionalmente se crea una columna que indica para que alumnos se imputo con el z score a nivel grado region
    if len(dataSet_por_nivel_grado) > 0:
        for a_l in list_area_letter:        

            mean = dataSet_por_nivel_grado.iloc[0][get_MN(a_l)]
            std = dataSet_por_nivel_grado.iloc[0][get_SN(a_l)]

            #df_a[get_ZN_I(a_l,postfix)] = np.where((df_a[get_ZN(a_l,postfix)].isna()) & (df_a[get_NC(a_l)].isna()==False), 1,0)
            #df_a.loc[(df_a[get_ZN(a_l,postfix)].isna()) & (df_a[get_NC(a_l)].isna()==False), get_ZN(a_l,postfix)] = (df_a[get_NC(a_l)]-mean)/std    
            df_a[get_ZN_I(a_l,postfix)] = np.where( (df_a[get_NC(a_l)].isna()==False) & (df_a['TOTAL_ALUMNOS_X_CODMOD_NVL_GR']<= min_alumn) , 1,0)
            df_a.loc[ (df_a[get_NC(a_l)].isna()==False) & (df_a['TOTAL_ALUMNOS_X_CODMOD_NVL_GR']<= min_alumn), get_ZN(a_l,postfix)] = (df_a[get_NC(a_l)]-mean)/std    

            df_a[get_ZN_I(a_l,postfix)] = np.where( (df_a[get_NC(a_l)].isna()==False) & (df_a[get_SN(a_l)]== 0) , 1,0)
            df_a.loc[ (df_a[get_NC(a_l)].isna()==False) & (df_a[get_SN(a_l)]== 0), get_ZN(a_l,postfix)] = (df_a[get_NC(a_l)]-mean)/std    


    #nos quedamos con las notas en el ultimo servicio cursado
    df_a.drop_duplicates(subset ="ID_PERSONA", keep = "last", inplace = True)
    
    return df_a


def get_df_por_grado_serv(df_notas_f):
    df_notas_por_grado_serv =  get_df_notas_por_groupby(df_notas_f)
    df_notas_f['dummy']=1
    df_notas_por_grado =  get_df_notas_por_groupby(df_notas_f,groupby=['dummy'],agg_label='CODMOD_NVL_GR')
    
    return df_notas_por_grado_serv, df_notas_por_grado


def get_df_notas_por_groupby(df_notas_f,groupby=['COD_MOD','ANEXO'],agg_label='CODMOD_NVL_GR'):
    #print(df_notas_f.columns)
    dataSet_por_nivel_grado = df_notas_f.assign(   

    ############## mean ##############   
     #A3 A2 A5  B0 F0
     MEAN_NOTA_M_X_CODMOD_NVL_GR =  np.where(df_notas_f['DA']=='M', 
                                             df_notas_f['NOTA_AREA_REGULAR'],np.NaN),  
        
     MEAN_NOTA_C_X_CODMOD_NVL_GR = np.where(df_notas_f['DA']=='C',
                                            df_notas_f['NOTA_AREA_REGULAR'],np.NaN),
        
     MEAN_NOTA_V_X_CODMOD_NVL_GR = np.where(df_notas_f['DA']=='V',
                                            df_notas_f['NOTA_AREA_REGULAR'],np.NaN), 

     MEAN_NOTA_G_X_CODMOD_NVL_GR = np.where(df_notas_f['DA']=='G',
                                               df_notas_f['NOTA_AREA_REGULAR'],np.NaN), 
        
     MEAN_NOTA_F_X_CODMOD_NVL_GR = np.where(df_notas_f['DA']=='F',
                                               df_notas_f['NOTA_AREA_REGULAR'],np.NaN), 

     MEAN_NOTA_T_X_CODMOD_NVL_GR = np.where(df_notas_f['DA']=='T',
                                               df_notas_f['NOTA_AREA_REGULAR'],np.NaN), 
           
     MEAN_NOTA_A_X_CODMOD_NVL_GR = np.where(df_notas_f['DA']=='A',
                                           df_notas_f['NOTA_AREA_REGULAR'],np.NaN), 
        
     MEAN_NOTA_J_X_CODMOD_NVL_GR = np.where(df_notas_f['DA']=='J',
                                           df_notas_f['NOTA_AREA_REGULAR'],np.NaN), 
        
     MEAN_NOTA_O_X_CODMOD_NVL_GR =   np.where((df_notas_f['DA']=='O') &                                                  
                                              (df_notas_f['NOTA_AREA_REGULAR']>=0),
                                               df_notas_f['NOTA_AREA_REGULAR'],np.NaN), 

     ############## std ##############   
     #A3 A2 A5  B0 F0
     STD_NOTA_M_X_CODMOD_NVL_GR =   np.where(df_notas_f['DA']=='M', 
                                             df_notas_f['NOTA_AREA_REGULAR'],np.NaN), 
        
     STD_NOTA_C_X_CODMOD_NVL_GR =   np.where(df_notas_f['DA']=='C',
                                             df_notas_f['NOTA_AREA_REGULAR'],np.NaN), 
        
     STD_NOTA_V_X_CODMOD_NVL_GR =   np.where(df_notas_f['DA']=='V',
                                             df_notas_f['NOTA_AREA_REGULAR'],np.NaN), 

        
     STD_NOTA_G_X_CODMOD_NVL_GR =   np.where(df_notas_f['DA']=='G',
                                             df_notas_f['NOTA_AREA_REGULAR'],np.NaN), 
        
     STD_NOTA_F_X_CODMOD_NVL_GR =   np.where(df_notas_f['DA']=='F',
                                             df_notas_f['NOTA_AREA_REGULAR'],np.NaN), 
        

     STD_NOTA_T_X_CODMOD_NVL_GR =   np.where(df_notas_f['DA']=='T',
                                             df_notas_f['NOTA_AREA_REGULAR'],np.NaN), 
        
     STD_NOTA_A_X_CODMOD_NVL_GR =   np.where(df_notas_f['DA']=='A',
                                             df_notas_f['NOTA_AREA_REGULAR'],np.NaN), 
        
     STD_NOTA_J_X_CODMOD_NVL_GR =   np.where(df_notas_f['DA']=='J',
                                             df_notas_f['NOTA_AREA_REGULAR'],np.NaN), 
        
     STD_NOTA_O_X_CODMOD_NVL_GR =   np.where((df_notas_f['DA']=='O') &                                              
                                                 (df_notas_f['NOTA_AREA_REGULAR']>=0),
                                                  df_notas_f['NOTA_AREA_REGULAR'],np.NaN), 
     
     TOTAL_ALUMNOS_X_CODMOD_NVL_GR = df_notas_f['ID_PERSONA']

    ).groupby(groupby).agg({
                                        'MEAN_NOTA_M_X_{}'.format(agg_label):'mean',
                                        'MEAN_NOTA_C_X_{}'.format(agg_label):'mean',  
                                        'MEAN_NOTA_V_X_{}'.format(agg_label):'mean', 
                                        'MEAN_NOTA_G_X_{}'.format(agg_label):'mean',
                                        'MEAN_NOTA_F_X_{}'.format(agg_label):'mean',
                                        'MEAN_NOTA_T_X_{}'.format(agg_label):'mean',
                                        'MEAN_NOTA_A_X_{}'.format(agg_label):'mean',
                                        'MEAN_NOTA_J_X_{}'.format(agg_label):'mean',
                                        'MEAN_NOTA_O_X_{}'.format(agg_label):'mean',
        
                                        'STD_NOTA_M_X_{}'.format(agg_label):'std',
                                        'STD_NOTA_C_X_{}'.format(agg_label):'std',
                                        'STD_NOTA_V_X_{}'.format(agg_label):'std',
                                        'STD_NOTA_G_X_{}'.format(agg_label):'std',
                                        'STD_NOTA_F_X_{}'.format(agg_label):'std',
                                        'STD_NOTA_T_X_{}'.format(agg_label):'std',
                                        'STD_NOTA_A_X_{}'.format(agg_label):'std',
                                        'STD_NOTA_J_X_{}'.format(agg_label):'std',
                                        'STD_NOTA_O_X_{}'.format(agg_label):'std',      
                                        
                                        'TOTAL_ALUMNOS_X_{}'.format(agg_label):'nunique', 
                                       })
    
    #dataSet_por_nivel_grado['COD_MOD']=dataSet_por_nivel_grado['COD_MOD'].apply(lambda x: '{0:0>7}'.format(x))
    #dataSet_por_nivel_grado['ANEXO']=dataSet_por_nivel_grado['ANEXO'].astype('int')

    return dataSet_por_nivel_grado


def get_df_por_alum(df_notas_f):

    dataSet_por_alumno = df_notas_f.assign(

     NOTA_M_X_ALUMNO =  np.where(df_notas_f['DA']=='M', 
                                 df_notas_f['NOTA_AREA_REGULAR'],np.NaN),  
        
     NOTA_C_X_ALUMNO = np.where(df_notas_f['DA']=='C',
                                df_notas_f['NOTA_AREA_REGULAR'],np.NaN),
        
     NOTA_V_X_ALUMNO = np.where(df_notas_f['DA']=='V',
                                df_notas_f['NOTA_AREA_REGULAR'],np.NaN), 

     NOTA_G_X_ALUMNO = np.where(df_notas_f['DA']=='G',
                                df_notas_f['NOTA_AREA_REGULAR'],np.NaN), 
        
     NOTA_F_X_ALUMNO = np.where(df_notas_f['DA']=='F',
                                df_notas_f['NOTA_AREA_REGULAR'],np.NaN), 

     NOTA_T_X_ALUMNO = np.where(df_notas_f['DA']=='T',
                                df_notas_f['NOTA_AREA_REGULAR'],np.NaN), 
           
     NOTA_A_X_ALUMNO = np.where(df_notas_f['DA']=='A',
                                df_notas_f['NOTA_AREA_REGULAR'],np.NaN), 
        
     NOTA_J_X_ALUMNO = np.where(df_notas_f['DA']=='J',
                                df_notas_f['NOTA_AREA_REGULAR'],np.NaN), 
        
     NOTA_O_X_ALUMNO = np.where((df_notas_f['DA']=='O') &                                                  
                                (df_notas_f['NOTA_AREA_REGULAR']>=0),
                                 df_notas_f['NOTA_AREA_REGULAR'],np.NaN), 

     TOTAL_CURSOS_X_ALUMNO =   1, 
     TOTAL_CURSOS_VALIDOS_X_ALUMNO =   np.where((df_notas_f['NOTA_AREA_REGULAR']>=0),1,0),      
     TOTAL_CURSOS_APROBADOS_X_ALUMNO =   np.where((df_notas_f['NOTA_AREA_REGULAR']>=11),1,0), 
     MEAN_CURSOS_X_ALUMNO =   np.where((df_notas_f['NOTA_AREA_REGULAR']>=0),df_notas_f['NOTA_AREA_REGULAR'],0), 
     STD_CURSOS_X_ALUMNO =   np.where((df_notas_f['NOTA_AREA_REGULAR']>=0),df_notas_f['NOTA_AREA_REGULAR'],0),   
        
    ).groupby(['COD_MOD','ANEXO','ID_PERSONA']).agg({
                                                    'NOTA_M_X_ALUMNO':'mean',
                                                    'NOTA_C_X_ALUMNO':'mean',  
                                                    'NOTA_V_X_ALUMNO':'mean', 
                                                    'NOTA_G_X_ALUMNO':'mean',
                                                    'NOTA_F_X_ALUMNO':'mean',
                                                    'NOTA_T_X_ALUMNO':'mean',
                                                    'NOTA_A_X_ALUMNO':'mean',
                                                    'NOTA_J_X_ALUMNO':'mean',
                                                    'NOTA_O_X_ALUMNO':'mean',
                                                    
                                                    'TOTAL_CURSOS_X_ALUMNO':'sum',
                                                    'TOTAL_CURSOS_VALIDOS_X_ALUMNO':'sum',
                                                    'TOTAL_CURSOS_APROBADOS_X_ALUMNO':'sum',
                                                    
                                                    'MEAN_CURSOS_X_ALUMNO':'mean',
                                                    'STD_CURSOS_X_ALUMNO':'std',
                                                   })
    

    return dataSet_por_alumno



def get_list_area_letter():
    return ['M','C','V','G','F','T','A','J','O']

def get_NC(area,postfix=None):
    if postfix is None :
        return 'NOTA_{}_X_ALUMNO'.format(area)
    else:
        return 'NOTA_{}_X_ALUMNO_{}'.format(area,postfix)

def get_ZN_I(area,postfix=None):
    return 'IMP_Z_NOTA_{}_{}'.format(area,postfix)

def get_ZN(area,postfix=None):
    return 'Z_NOTA_{}_{}'.format(area,postfix)

def get_MN(area,postfix=None):
    if postfix is None :
        return 'MEAN_NOTA_{}_X_CODMOD_NVL_GR'.format(area)
    else:
        return 'MEAN_NOTA_{}_X_CODMOD_NVL_GR_{}'.format(area,postfix)

def get_SN(area,postfix=None):
    if postfix is None :
        return 'STD_NOTA_{}_X_CODMOD_NVL_GR'.format(area)
    else:
        return 'STD_NOTA_{}_X_CODMOD_NVL_GR_{}'.format(area,postfix)


df = hadb.get_siagie_por_anio(anio=2017,id_grado=9)

#cls_json = {}
#cls_json['SITUACION_FINAL']=["APROBADO","DESAPROBADO"]
#cls_json['JUNTOS']="dummy"
#df_h = generar_kpis_historicos(df,anio_df=2017,anio_h=2016,cls_json=cls_json,t_anios=2 )

