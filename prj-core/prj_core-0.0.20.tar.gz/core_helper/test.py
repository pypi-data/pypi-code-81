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



#import core_helper.helper_transformers as ht
import src.Prj_Core.core_helper.helper_transformers as ht

import src.Prj_Core.core_helper.helper_clean as hc
import src.Prj_Core.core_helper.helper_classification_model as hcm

import src.Prj_Core.core_helper.helper_dataframe as hd
import src.Prj_Core.core_helper.helper_siagie_kpi as hsk

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

df_servicios = hadb.get_df_servicios(macro_region='oriente')

def get_df_procesado(anio,col_name_y,grupo_grados):

    list_pd = []
    #5,6,7,8
    for ID_GRADO in grupo_grados:
        url = hg.get_base_path()+"\\src\\Prj_Interrupcion_Estudios\\Prj_Desercion\\_02_Preparacion_Datos\\_02_Estructura_Base\\_data_\\nominal\\estructura_base_EBR_{}_{}_delta_1.csv"
        url = url.format(ID_GRADO,anio)
        df =pd.read_csv(url, dtype=dtypes_columns ,encoding="utf-8")
        #df['ID_GRADO'] = ID_GRADO
        df = pd.merge(df,df_servicios, left_on=["COD_MOD","ANEXO"], right_on = ["COD_MOD","ANEXO"] ,how="inner")
        list_pd.append(df)
        
    df_reg = pd.concat(list_pd)
    
    anio_notas = anio-2
    print("antes : ",df_reg.shape)
    df_reg = hsk.agregar_notas(df_reg,anio,anio_notas)
    #print(df_reg.ID_GRADO.value_counts())
    print("despues : ",df_reg.shape)
    
    df_reg = hc.fill_nan_with_nan_category_in_cls(df_reg , ["SITUACION_MATRICULA_T_MENOS_1",
                                                            "SF_RECUPERACION_T_MENOS_1",
                                                            "PARENTESCO","DSC_DISCAPACIDAD",
                                                            "SEXO_APOD",
                                                            "SITUACION_FINAL_T_MENOS_1",
                                                            "SITUACION_MATRICULA_T"])
    
    df_reg = hc.trim_category_cls(df_reg)
    
    
    df_reg['EDAD_EN_DIAS_T']  = df_reg['EDAD_EN_DIAS_T'].round()
    
    column_y = col_name_y
    
    columns_too_much_nan_and_categories = ["JUSTIFICACION_RETIRO_T_MENOS_1","DSC_PAIS","DSC_LENGUA"]
    columns_to_drop  = ['ID_PERSONA','COD_MOD','ANEXO','COD_MOD_T_MENOS_1','ANEXO_T_MENOS_1','ID_GRADO_T_MENOS_1',
                        'NUMERO_DOCUMENTO_APOD','N_DOC','NIVEL_INSTRUCCION_APOD'] 
    #cat_muy_largas = ['D_REGION']
    
    columns_to_drop_all = columns_too_much_nan_and_categories+columns_to_drop + [column_y]
    
    
    y = df_reg[column_y]
    X = df_reg.drop(columns = columns_to_drop_all) 
    
    ct = ht.CatTransformer(pp = "lb",console=True) #lb le
    ct.fit(X)
    return ct.transform(X) , y


X_t , y = get_df_procesado(2018,'DESERCION_2018_2019',[5])

#grupo_grado_list = [[5,6,7,8]]
#grupo_grado_list = [[5],[6],[7],[8]]
grupo_grado_list = [[5]]
y_test2_total = []
y_pred2_total = []

for grupo_grado in grupo_grado_list:
    
    X_t , y = get_df_procesado(2017,'DESERCION_2017_2018',grupo_grado)
    
    X_train, X_test, y_train, y_test= train_test_split(X_t, y, test_size=0.20,stratify=y,random_state=42)
    model , predicted_probas  , kpis = hcm.modelar_clasificacion_binaria("neg_bagging_fraction__lgb_model", X_train,y_train,X_test,y_test,url="prueba")
    
    X_test2 , y_test2 = get_df_procesado(2018,'DESERCION_2018_2019',grupo_grado)
    y_test2_total.append(y_test2)
    
    X_test2 = hd.igualar_columnas(X_t,X_test2)
    y_pred2 ,y_prob2,  predicted_probas2 = hcm.predecir_clasificacion_binaria(model,X_test2)
    y_pred2_total.append(y_pred2)
    

y_test2_flat = hg.flat_list(y_test2_total)
y_pred2_flat = hg.flat_list(y_pred2_total)

print(classification_report(y_test2_flat, y_pred2_flat))
print("average_precision", average_precision_score(y_test2_flat, y_pred2_flat))


