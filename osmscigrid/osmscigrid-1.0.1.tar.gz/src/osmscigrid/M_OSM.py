"""Read funktion: OSM Data (pipelines) into K_Net Class"""

#######################################################################
#All functions are called from the makefile                           #
#######################################################################

#from Code.OSM.M_OSM_CreateElements import M_OSM_CreateElements
#from unidecode                     import unidecode
#import Code.OSM.C_colors              as CC
import esy.osmfilter as EO
from . import M_OSM_convert
from . import OSMpath
from esy.osmfilter import Node,Way,Relation
from esy.osmfilter import osm_colors as CC


def read(PBF_inputfile,
         JSON_outputfile,
         TM_World_Borders_file='../TM_World_Borders/TM_WORLD_BORDERS-0.3.shp',
         countrycode='EU',
         NewPreFilterData=True, 
         CreateElements=True, 
         LoadElements=True,
         CreateCountryCodeForLines=True, 
         LoadCountryCodeForLines=True,
         length=100,
         min_length=0,
         multiprocess=True,
         verbose=False):
    """ Reads the OSM PipelineNetwork into K_Net Class
    \n.. comments: 
    Call: 
        
         OSM_Netz=M_OSM.read(Info=InfoOSM1)
         CreateElements = True (If the countrydata are used for the first time)
         NewPreFilterData = True (If the countrydata are used for the first time) 
         
    Return Data:
         element
         
         if elements are ways and than you can finde the referenced nodes in Data
         
         eg. to access lon lat for the node '6037838916' 
         Data['Node']['6037838916']['lonlat']"""
    
 
    

    prefilter = {
        Node: {"substance"    : ["gas","cng"],
                      "pipeline"     : ["substation","marker","valve",
                                        "pressure_control_station",True],
                      "product"      : ["gas","cng"],
                      "substation"   : ["valve","measurement", "inspection_gauge",
                                        "compression","valve_group"],
                      "man_made"     : ["pipeline","pipeline_marker","pumping_station"],
                      "gas"          : ["station",True],
                      "content"      : ["gas","cng"],
                      "storage"      : ["gas","cng"],
                      "industrial"   : ["gas","terminal","wellsite","cng"]
                      },

        Way: {"substance"     : ["gas","cng"],
                     "man_made"      : ["gasometer","pipeline","petroleum_well",
                                        "pumping_station", "pipeline_marker",
                                        "pipeline_station","storage_tank",
                                        "gas_cavern"],
                     "industrial"    : ["gas","terminal","cng"],
                     "gas"           : ["station"],
                     "content"       : ["gas","cng"],
                     "pipeline"      : ["substation","marker","valve",
                                        "pressure_control_station",True],
                     "storage"       : ["gas","cng"],
                     "seamark:type"  : ["pipeline_submarine"],
                     "land_use"      : ["industrial:gas"]
                      },

        Relation: {"substance"    : ["gas","cng"],
                      "man_made"     : ["gasometer","pipeline","petroleum_well",
                                        "pumping_station",
                                       "pipeline_marker","pipeline_station",
                                       "storage_tank","gas_cavern"],
                      "industrial"   : ["gas","terminal","cng"],
                      "gas"          : ["station"],
                      "content"      : ["gas","cng"],
                      "pipeline"     : ["substation","marker","valve",
                                        "pressure_control_station",True],
                      "storage"      : ["gas","cng"],
                      "seamark:type" : ["pipeline_submarine"],
                      "land_use"     : ["industrial:gas"]
                      }
        }

    whitefilter=[(("man_made","pipeline"),("substance","gas")),
                (("man_made","pipeline"),("substance","cng")),
                (("man_made","pipeline"),("substance","natural_gas")),
                (("man_made","pipeline"),("pipeline,type","natural_gas")),
                (("man_made","pipeline"),("type","gas")),
                (("man_made","pipeline"),("type","natural_gas")),  
                (("man_made","pipeline"),("type","cng")), 
                (("man_made","pipeline"),("industrial","gas")), 
                (("man_made","pipeline"),("industrial","cng")), 
                (("man_made","pipeline"),("industrial","natural_gas")),]
    
    blackfilter     =[("pipeline","substation"),
                    ("substation","distribution"),
                    ('usage', 'distribution'),
                    ('pipeline:type','water'),
                    ('pipeline:type', 'sewer'),
                    ("pumping_station","water"),
                    ("pumping_station","sewage"),
                    ('pumping_station','wastewater'),
                    ("type","wastewater"),
                    ("type","fuel"),
                    ("type","sewage"),
                    ("type","oil"),
                    ("type","water"),
                    ("substance","sewage"),
                    ("substance","water"),
                    ("substance","hot_water"),
                    ("substance","fuel"),
                    ("substance","wastewater"),
                    ("substance","rainwater"),
                    ("substance", "drain"),
                    ("substance", "heat"),
                    ("substance", "gas,heat"),
                    ("substance", "heat,gas"),
                    ("substance", "ammonia"),
                    ("substance", "ethylen"),
                    ("substance","oil")]
#    blackfilter = [("pipeline","substation"),]
#    whitefilter =[(("man_made","pipeline"),("waterway","drain")),]
    if verbose:
        print(CC.Caption+' Creating OSM net'+CC.End)
        print(f'Create:{CreateElements}')
    

    
    [Data,Elements]=EO.run_filter('pipelines',PBF_inputfile, JSON_outputfile, 
                                  prefilter, whitefilter, blackfilter, 
                                  NewPreFilterData=NewPreFilterData, 
                                  CreateElements=CreateElements, 
                                  LoadElements=LoadElements,verbose=verbose, 
                                  multiprocess=multiprocess)
#    print(Data)
     
#    [Data,Elements] = M_OSM_CreateElements('pipelines',countrycode,PBF_inputfile,
#                          JSON_outputfile, NewPreFilterData=NewPreFilterData, 
#                          CreateElements=CreateElements, LoadElements=LoadElements)
    ### Hier zwischenergebnisse speichern
    # min_length=min
    # length=length
    OSM=M_OSM_convert.RawData2ClassData(Data,Elements,JSON_outputfile,TM_World_Borders_file,
                                        countrycode=countrycode, 
                                        CreateCountryCodeForLines=CreateCountryCodeForLines,
                                        LoadCountryCodeForLines=LoadCountryCodeForLines,
                                        min_length=min_length,segment_length=length,verbose=verbose)


    OSM=OSMpath.pathcorrection(OSM)

    return OSM

#def createall():
#    import configparser
#    from  configparser import  ExtendedInterpolation
#    from  pathlib            import Path
#    import os
#    import time
#    CountryCodes=["AL","XK","AM","LV","AT","LI","AZ","LT","BY","LU","BE","MT","BA",
#          "MD","BG","ME","HR","NL","CY","NO","CZ","PL","PT","EE","RO","FI",
#          "RS","FR","SK","GE","SI","DE","ES","EL","SE","HU","CH","IS","TR",
#          "IE","UA","IT","GB","DK","RU","EU"]
#
#    InfoOSM     = configparser.ConfigParser(interpolation=ExtendedInterpolation())
#    Setup_OSM      = Path(os.getcwd() + '/Setup/Setup_OSM.ini')
#    InfoOSM.read(Setup_OSM)
#
#    for countrycode in CountryCodes:
#    #    print('OSM_'+entry+'_ES2050')
#        InfoOSM1        = InfoOSM['OSM_'+countrycode+'_local']
#        #InfoOsmosis = InfoOSM['OSMOSIS_ADAM']
#        PBF_inputfile   = InfoOSM1['PBF_inputfile']
#        JSON_outputfile = InfoOSM1['JSON_outputfile']
#
#        print("PBF_inputfile for "+countrycode+" exists : "+ str(os.path.isfile(PBF_inputfile)))
#        if (os.path.isfile(PBF_inputfile)):
#            print(time.strftime('%m/%d/%Y', time.gmtime(os.path.getmtime(PBF_inputfile))))
#            print('check')
#            read(InfoOSM1,countrycode = countrycode, NewPreFilterData = True, CreateElements  = True,LoadElements = True, CreateCountryCodeForLines = True, LoadCountryCodeForLines=True)
#        else:
#            print('pbf-file not found')
        
        
        
#        [GasData,elements]=M_OSM_CreateElements(countrycode,PBF_inputfile,JSON_outputfile, CreateNewGasData=True, CreateElements=True,LoadElements=False,CreateCountryCodeForPipelines = True)
#    ########
#    #Markers
#    ########
#    [nodes,ids,tags,node_ids,tagdicts] = OSMnodes2net(elements["markers"],GasData)
#    for i,entry in enumerate(zip(nodes,ids,tags,node_ids)):
#        Marker=KC.OSMComponent(id = ids[i], name=ids[i], node_id=node_ids[i],source_id = ['OSM'], lat = nodes[i][1], 
#                              long = nodes[i][0], country_code = countrycode,tags = tagdicts[i])
#        Ret_Data.Markers.append(Marker)
#        
#    ########
#    #SeaMarkers
#    ########
#    [lines,ids,lengths,tags,node_ids,tagdicts]= OSMways2net(elements["seamarkers"],GasData,min_length=0)
#    for i,entry in enumerate(zip(lines,ids,lengths,tags)):
#        SeaMarker=KC.OSMComponent(id = ids[i], name=ids[i], node_id=node_ids[i],source_id = ['OSM'], lat = lines[i][1], 
#                              long = lines[i][0], country_code = countrycode, length=lengths[i],tags = tagdicts[i])
#        Ret_Data.SeaMarkers.append(SeaMarker)
            
        
#    ########
#    #Compressors_lines
#    ########
#    [lines,ids,lengths,tags,node_ids,tagdicts] = OSMways2net(elements["compressors_lines"],GasData,min_length=0)
##    maxlines=len(lines)
#    for i,entry in enumerate(zip(lines,ids,lengths,tags)):
#        Compressor_Lines=KC.OSMComponent(id = ids[i], name=ids[i], node_id=node_ids[i],source_id = ['OSM'], lat = lines[i][1], 
#                              long = lines[i][0], country_code = countrycode,tags = tagdicts[i], length=lengths[i])
#        Ret_Data.Compressors_Lines.append(Compressor_Lines)
#        
#    ########
#    #Compressors
#    ########
#    [nodes,ids,tags,node_ids,tagdicts] = OSMnodes2net(elements["compressors"],GasData)
#    for i,entry in enumerate(zip(nodes,ids,tags,node_ids)):
#        Compressor=KC.OSMComponent(id = ids[i], name=ids[i], node_id=node_ids[i],source_id = ['OSM'], lat = nodes[i][1], 
#                              long = nodes[i][0], country_code = countrycode,tags = tagdicts[i])
#        Ret_Data.Compressors.append(Compressor)
#
#    
#    
#    ########
#    #Pipeline3
#    ########
#    [lines,ids,lengths,tags,node_ids,tagdicts] = OSMways2net(elements["pipelines3"],GasData,min_length=0)
#    for i,entry in enumerate(zip(lines,ids,lengths,tags)):
#        PipeLine3=KC.OSMComponent(id = ids[i], name=ids[i], node_id=node_ids[i],source_id = ['OSM'], lat = lines[i][1], 
#                              long = lines[i][0], country_code = countrycode, length=lengths[i],tags = tagdicts[i])
#        Ret_Data.PipeLines3.append(PipeLine3)
#
#    
#    
#    ########
#    #Pipeline2
#    ########
#    [lines,ids,lengths,tags,node_ids,tagdicts] = OSMways2net(elements["pipelines2"],GasData,min_length=0)
#    for i,entry in enumerate(zip(lines,ids,lengths,tags)):
#        PipeLine2=KC.OSMComponent(id = ids[i], name=ids[i], node_id=node_ids[i],source_id = ['OSM'], lat = lines[i][1], 
#                              long = lines[i][0], country_code = countrycode, length=lengths[i],tags = tagdicts[i])
#        Ret_Data.PipeLines2.append(PipeLine2)
#

#        
#        
#        
