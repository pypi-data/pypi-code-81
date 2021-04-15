import json
import os
import time


def get_param(param_name,elements,i):
    """
    returns values of param_name of the Netz.elements[i]
    """
    res=elements[i].__dict__.get(param_name)    
    return res

def get_coordinates(elements,i):
    """
    returns coordinates in geoJSON format
    """
    lats=elements[i].__dict__.get('lat')    
    longs=elements[i].__dict__.get('long')  
    coordinates=[]
    
    "for line elements"
    if isinstance(longs,list):
        for coords in zip(longs,lats):
            coordinates.append(list(coords))     
        "for point elements"        
    else:
        coordinates=[longs,lats]        
    return coordinates
            
def create_GeoJson_Lines(elements):    
    """
    create GeoJSON output if Netz.elements consists of lines
    """    
    feature=[]
    for i in range(len(elements)):
        
        feature.append(       {'type'        : 'Feature',
                               'geometry'    : 
                              {'type'        : 'LineString',
                               'coordinates' : get_coordinates(elements,i)},
                               'properties'  : 
                              {'name'        : get_param('name',elements,i), 
                               'id'          : get_param('id',elements,i),
                               'country_code': get_param('country_code',elements,i) ,
                               'tags'        : get_param('tags',elements,i),
                               'param'       : get_param('param',elements,i),
                               'method'      : get_param('method',elements,i)}
                              })   
    return feature
    
def create_GeoJson_Points(elements):
    """
    create GeoJSON output if elements consists of points
    """    
    feature=[]
    for i in range(len(elements)):
        feature.append(       {'type'         : 'Feature',
                               'geometry'     : 
                              {'type'         : 'Point',
                               'coordinates'  : get_coordinates(elements,i)},
                               'properties'   : 
                              {'name'         : get_param('name',elements,i), 
                               'id'           : get_param('id',elements,i),
                               'country_code' : get_param('country_code',elements,i) ,
                               'tags'         : get_param('tags',elements,i),
                               'param'        : get_param('param',elements,i),
                               'method'       : get_param('method',elements,i)}
                               })   
    return feature
    
def geojson_export_element(Netz,Elementtyp,verbose=False):
    """
    Export Netz.Element to a geoJSON file
    """
    elements=Netz.__dict__.get(Elementtyp)
    #if verbose:
     #   print(elements)
      #  print(Elementtyp)
    if Elementtyp in (['PipeLines','PipeSegments']):
        output=json.dumps({'type': 'FeatureCollection',
          'features': create_GeoJson_Lines(elements)},indent=4)
    else:    
        output=json.dumps({'type': 'FeatureCollection',
          'features': create_GeoJson_Points(elements)},indent=4)
        
    return output

def export_geojson(Netz,netname,filepath='Output/GeoJSON/',verbose=False):
    """
    Export Netz object to separate geojson files
    """
    
    for pipe in Netz.PipeSegments:
        pipe.country_code=list(pipe.country_code)
    if verbose:
        print(os.path.dirname(filepath))    
        print('Filepathexist=',os.path.exists(os.path.dirname(filepath)))   
    if not os.path.exists(os.path.dirname(filepath)):
        os.makedirs(os.path.dirname(filepath))
        if verbose:
            print('created the following path: ', filepath)
        time.sleep(10)
        if verbose:
            print(os.path.exists(os.path.dirname(filepath)))
        
    if os.path.exists(os.path.dirname(filepath)):
        for elementname in Netz.CompLabels():   
            if verbose: print(elementname)
            if len(Netz.__dict__[elementname])>0:
                a=geojson_export_element(Netz,elementname,verbose)
                filename=netname+'_'+elementname+'.geojson'
                filename=os.path.join(filepath,filename)
                open(filename,"w+").write(a)
            
if __name__== '__main__':
     import M_Internet
     INET2=M_Internet.read(RelDirName = '../Eingabe/InternetDaten/')
     export_geojson(INET2,'INET',path='../Ausgabe/GeoJSON')
