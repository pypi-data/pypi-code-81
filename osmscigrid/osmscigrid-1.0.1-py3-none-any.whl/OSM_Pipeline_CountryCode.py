from . import M_GetCountry          as GC
#import Code.K_Component           as KC
from . import M_PCKL                as PCKL
from . import C_colors              as CC
import os, time

def Calc_OSM_Pipeline_CountryCodes(TM_World_Borders_file,
                                   PipeLine,countrycode):
    
    ''' Calulating lat/long for each pipeline point of a Pipeline '''
    
    countrypolydict=GC.CountryPolyDict(TM_World_Borders_file,
                                       predicted_countrycodes=countrycode)
    res=GC.GetCountry4List(TM_World_Borders_file,PipeLine.long,PipeLine.lat,countrypolydict=countrypolydict,predicted_countrycodes=countrycode)
    return res


def Calc_OSM_Pipelines_CountryCodes(TM_World_Borders_file,Pipelines,countrycode,verbose=False):
    '''
    Calculating lat/long for a list of pipelines
    '''
    pipelines_country_code_list=[]
    data_count=len(Pipelines)
    for i,pipeline in enumerate(Pipelines):
        countrycodes_of_line=Calc_OSM_Pipeline_CountryCodes(TM_World_Borders_file,
                                                             pipeline,countrycode)
        pipelines_country_code_list.append([pipeline.id,
                                            countrycodes_of_line])
        print(countrycodes_of_line)
        if verbose==True:
            print(f'{i+1}/{data_count}')
    return pipelines_country_code_list


def Create_Pipelines_CountryCodes(JSON_outputfile,TM_World_Borders_file,
                                  Netz,countrycode,verbose=False):
    '''
    Calculates pipeline countrycodes and stores it to file
    '''
    print(CC.Green+'Create countrycodes for pipelines:'+CC.End)
    pipeline_countrycodelist=Calc_OSM_Pipelines_CountryCodes(TM_World_Borders_file,
                                                             Netz.PipeLines,
                                                             countrycode,
                                                             verbose)
    print('\nPickle gas data to \n'+os.path.dirname(JSON_outputfile),'/pipeline_countrycode_list.pickle')
    PCKL.picklesavelist(pipeline_countrycodelist,
    'pipeline_countrycode_list.pickle',os.path.dirname(JSON_outputfile))
    pipesegment_countrycodelist=Calc_OSM_Pipelines_CountryCodes(TM_World_Borders_file,
                                                             Netz.PipeSegments,
                                                             countrycode,
                                                             verbose)
                                                             
    print('\nPickle gas data to \n'+os.path.dirname(JSON_outputfile),'/pipesegment_countrycode_list.pickle')
    PCKL.picklesavelist(pipesegment_countrycodelist,
    'pipesegment_countrycode_list.pickle',os.path.dirname(JSON_outputfile))
    pass
    
def load_pipeline_countrycode(JSON_outputfile):
    '''
    Loads Countrycodes from Json-File
    '''
    print("Load countrydata from ",JSON_outputfile)
    liste=PCKL.pickleloadlist(os.path.dirname(JSON_outputfile),
                              'pipeline_countrycode_list.pickle')
    
    return liste

def load_pipesegment_countrycode(JSON_outputfile):
    '''
    Loads Countrycodes from Json-File
    '''
    print("Load countrydata from ",JSON_outputfile)
    liste=PCKL.pickleloadlist(os.path.dirname(JSON_outputfile),
                              'pipesegment_countrycode_list.pickle')
    
    return liste

def Load_Pipelines_Countrycodes(JSON_outputfile,Netz,countrycode):
    '''
    loads countrycodes list for a Netz object and 
    
    '''
    pipe_count=len(Netz.PipeLines)
    countrycode_data=load_pipeline_countrycode(JSON_outputfile)
    data_count=len(countrycode_data)
    if pipe_count==data_count:
        for i in range(pipe_count):
            #print(i,':',countrycode_data[i][0],'vs',Netz.PipeLines[i].id )
            for j in range(data_count):
                if countrycode_data[j][0]==Netz.PipeLines[i].id:
                    Netz.PipeLines[i].country_code=countrycode_data[j][1]
                    for node_id,countrycode_value in zip(Netz.PipeLines[i].node_id,
                                                         Netz.PipeLines[i].country_code):
                        Netz.select('Nodes','id',node_id).country_code=countrycode_value
           
            
    else:
        print(CC.Warning+'2:Outdatet Countrypipeline file\n Please recreate countrycode with OSM_Pipelines_CountryCodes()'+CC.End)
        time.sleep(2)
    pass

def Load_Pipesegments_Countrycodes(JSON_outputfile,Netz,countrycode):
    '''
    loads countrycodes list for a Netz object and 
    
    '''
    pipe_count=len(Netz.PipeSegments)
    countrycode_data=load_pipesegment_countrycode(JSON_outputfile)
    data_count=len(countrycode_data)
    if pipe_count==data_count:
        for i in range(pipe_count):
            #print(i,':',countrycode_data[i][0],'vs',Netz.PipeSegments[i].id)
            for j in range(data_count):
                if countrycode_data[j][0]==Netz.PipeSegments[i].id:
                    Netz.PipeSegments[i].country_code=countrycode_data[j][1]
                    for node_id,countrycode_value in zip(Netz.PipeSegments[i].node_id,
                                                         Netz.PipeSegments[i].country_code):
                        Netz.select('Nodes','id',node_id).country_code=countrycode_value
        # else:
        # print(CC.Green+'Success: added countrycodes to ',data_count,' Pipelines'+CC.End)
        # time.sleep(2)
            
    else:
        print(CC.Warning+'2:Outdatet Countrysegment file\n Please recreate countrycode with OSM_Pipelines_CountryCodes()'+CC.End)
        time.sleep(2)
    pass


if __name__=='__main__':
    Create_Pipelines_CountryCodes(JSON_outputfile,OSM,'EU')
    Load_Pipelines_Countrycodes(JSON_outputfile,OSM,'EU')
    
    
