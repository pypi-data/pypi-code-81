# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
'''
from core_helper import helper_classification_model as hcm
from core_helper import helper_imputacion as hi
from core_helper import helper_transformers as ht 
from core_helper import helper_dataframe as hd 
from core_helper import helper_acces_db as hadb
from sklearn.model_selection import train_test_split
'''

#import core_helper.helper_general as hg
import src.Prj_Core.core_helper.helper_general as hg
hg.set_base_path()

#import core_helper.helper_acces_db as hadb
import src.Prj_Core.core_helper.helper_acces_db as hadb

import src.Prj_Core.core_helper.helper_feature_selection as hfs

#import core_helper.helper_transformers as ht
import src.Prj_Core.core_helper.helper_transformers as ht

import src.Prj_Core.core_helper.helper_clean as hc
import src.Prj_Core.core_helper.helper_classification_model as hcm

import src.Prj_Core.core_helper.helper_dataframe as hd
import src.Prj_Core.core_helper.helper_siagie_kpi as hsk
import src.Prj_Core.core_helper.helper_terceros_kpi as htk

from sklearn.metrics import classification_report,average_precision_score
   
#df_notas_2016 = hadb.get_df_notas(2016)
#df_notas_2017 = hadb.get_df_notas(2017)

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



def get_df_procesado(anio,col_name_y,grupo_grados,macro_region, feature_selection=False):

    df_servicios = hadb.get_df_servicios(macro_region=macro_region)    

    list_pd = []
    #5,6,7,8
    for ID_GRADO in grupo_grados:
        url = hg.get_base_path()+"\\src\\Prj_Interrupcion_Estudios\\Prj_Desercion\\_02_Preparacion_Datos\\_02_Estructura_Base\\_data_\\nominal\\estructura_base_EBR_{}_{}_delta_1.csv"
        url = url.format(ID_GRADO,anio)
        df =pd.read_csv(url, dtype=dtypes_columns ,encoding="utf-8")
        df['STR_ID_GRADO'] = "GRADO_" + str(ID_GRADO)      
        df = pd.merge(df,df_servicios, left_on=["COD_MOD","ANEXO"], right_on = ["COD_MOD","ANEXO"] ,how="inner")
        list_pd.append(df)
        
    df_reg = pd.concat(list_pd)

    anio_notas = anio-1   
      
   
    cls_json = {}
    cls_json['SITUACION_FINAL']=["APROBADO","DESAPROBADO"]
    cls_json['SF_RECUPERACION']=["APROBADO","DESAPROBADO"]
    cls_json['SITUACION_MATRICULA']=["PROMOVIDO","REPITE","INGRESANTE","REENTRANTE"]
    cls_json['JUNTOS']="dummy"
    df_reg = hsk.generar_kpis_historicos(df_reg,anio_df=anio,anio_h=anio-2,cls_json=cls_json,t_anios=4)  
    df_reg = hsk.agregar_notas(df_reg,anio,anio_notas, cls_group=["ZSCORE"])    
    df_reg = htk.agregar_sisfoh(df_reg)       
    df_reg = hsk.generar_kpis_desercion(df_reg,anio_df=anio, anio_h=anio-2 ,t_anios=4)        
    df_reg =  htk.agregar_shock_economico(df_reg,anio=anio)    
    df_reg = hsk.generar_kpis_traslado(df_reg,anio_df=anio,anio_h=anio-1,t_anios=5)
    df_reg = hsk.generar_kpis_traslado_a_publico(df_reg,anio_df=anio,anio_h=anio-1,t_anios=5)

    df_reg = hc.fill_nan_with_nan_category_in_cls(df_reg , ["SITUACION_MATRICULA_T_MENOS_1",
                                                            "SF_RECUPERACION_T_MENOS_1",
                                                            "PARENTESCO","DSC_DISCAPACIDAD",
                                                            "SEXO_APOD",
                                                            "SITUACION_FINAL_T_MENOS_1",
                                                            "SITUACION_MATRICULA_T",
                                                            "TIENE_CERTIFICADO_DISCAPACIDAD",
                                                            "PADRE_VIVE","MADRE_VIVE"])
    
    df_reg = hc.trim_category_cls(df_reg)
    
    df_reg = hsk.formatear_columnas_siaguie(df_reg)
    
    #df_reg['EDAD_EN_DIAS_T']  = df_reg['EDAD_EN_DIAS_T'].round()
   
   
    columns_too_much_nan_and_categories = ["JUSTIFICACION_RETIRO_T_MENOS_1","DSC_PAIS","DSC_LENGUA"]
    columns_to_drop  = ['ID_PERSONA','COD_MOD','ANEXO','COD_MOD_T_MENOS_1','ANEXO_T_MENOS_1','ID_GRADO_T_MENOS_1',
                        'NUMERO_DOCUMENTO_APOD','N_DOC','NIVEL_INSTRUCCION_APOD'] 
    #cat_muy_largas = ['D_REGION']
    
    columns_to_drop_all = columns_too_much_nan_and_categories+columns_to_drop 
    
    ID_P_T = df_reg['ID_PERSONA']
    
    if col_name_y is not None:
        y = df_reg[col_name_y]
        columns_to_drop_all.append(col_name_y)
    else:    
        y = None
        
        
    X = df_reg.drop(columns = columns_to_drop_all) 

    ct = ht.CatTransformer(pp = "lb",console=True) #lb le
    ct.fit(X)
    X_t = ct.transform(X)
    
    if feature_selection:
        X_t = hfs.drop_cls_unique_value(X_t)
        X_t = hfs.drop_corr_columns(X_t)
        X_t = hfs.drop_nan_columns(X_t)
        
    return ID_P_T, X_t , y





#print(X_t.columns)
#grupos_grados = {"1 prim": [4],"2 prim": [5], "3-5 prim": [6,7,8], "6 prim": [9], "1-4 sec": [10,11,12,13],"5 sec": [14]}
grupos_grados = {"1 prim": [4]}

y_test2_total = []
y_pred2_total = []

#lista_mr = ["centro","norte","sur","oriente","lima"]
lista_mr = ["oriente"]
PATH_RESULT = "resultado"

for key, grupo_grado  in grupos_grados.items():
    KPIs_list = []
    
    for macro_region in lista_mr:
        path = "{}/{}/{}".format(PATH_RESULT,key,macro_region)
        hg.validar_directorio(path) 
        
        ID_P_T, X_t , y = get_df_procesado(2019,'DESERCION_2019_2020',grupo_grado,macro_region,True)
        X_train, X_test, y_train, y_test= train_test_split(X_t, y, test_size=0.20,stratify=y,random_state=42)
        t_train = X_train.shape[0]
        t_test =  X_test.shape[0]
        
        ID_P_T2, X_test2 , y_test2 = get_df_procesado(2021,None,grupo_grado,macro_region,False)
        
        X_test2 = hd.igualar_columnas(X_t,X_test2)
        
        y_test2_total.append(y_test2)       
               
        print(X_train.columns)
        model_name = "neg_bagging_fraction__lgb_model"
        path_directory_model = path +"/"+model_name 
        model , predicted_probas  , KPIs = hcm.modelar_clasificacion_binaria(model_name, X_train,y_train,X_test,y_test,path_directory_model)
        KPIs_list.append([macro_region,model_name,t_train,t_test,KPIs])
        y_pred2 ,y_prob2_nbf,  predicted_probas2 = hcm.predecir_clasificacion_binaria(model,X_test2)
        
                
        model_name = "scale_pos_weight__lgb_model"
        path_directory_model = path +"/"+model_name 
        model , predicted_probas  , KPIs = hcm.modelar_clasificacion_binaria(model_name, X_train,y_train,X_test,y_test,path_directory_model)
        KPIs_list.append([macro_region,model_name,t_train,t_test,KPIs])
        y_pred2 ,y_prob2_spw,  predicted_probas2 = hcm.predecir_clasificacion_binaria(model,X_test2)
        
                
        model_name = "custom_bagging__lgb_model"
        path_directory_model = path +"/"+model_name 
        model , predicted_probas  , KPIs = hcm.modelar_clasificacion_binaria(model_name, X_train,y_train,X_test,y_test,path_directory_model)
        KPIs_list.append([macro_region,model_name,t_train,t_test,KPIs])
        y_pred2 ,y_prob2_cb,  predicted_probas2 = hcm.predecir_clasificacion_binaria(model,X_test2)
          
        
        X_test2["neg_bagging_fraction__lgb_model"] = y_prob2_nbf
        X_test2["scale_pos_weight__lgb_model"] = y_prob2_spw
        X_test2["custom_bagging__lgb_model"] = y_prob2_cb
        
        X_t['DESERCION'] = y    
        X_t['ID_PERSONA'] = ID_P_T
        
        #X_test2['DESERCION'] = y_test2    
        X_test2['ID_PERSONA'] = ID_P_T2
        
        X_t.to_csv(path+"/X_t.csv",index =False , encoding="utf-8")
        X_test2.to_csv(path+"/X_t_mas_1.csv",index =False , encoding="utf-8")
      
        y_pred2_total.append(y_pred2)

    path = "{}/{}".format(PATH_RESULT,key)
    hg.validar_directorio(path)    

    df_result = hcm.get_result_df(KPIs_list)
    df_result.to_excel(path+"/resultados.xlsx")  

#y_test2_flat = hg.flat_list(y_test2_total)
#y_pred2_flat = hg.flat_list(y_pred2_total)



