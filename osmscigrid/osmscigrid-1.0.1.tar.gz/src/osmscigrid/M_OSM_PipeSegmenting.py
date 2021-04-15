#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from . import K_Component    as KC
from . import C_colors       as CC
from . import M_DataAnalysis as MD
from   geopy.distance      import great_circle
from . import M_GetCountry as MG 
from . path_segmenter import path_segmenting

def pipeline_sequencing(lat_list,lon_list,max_length=10):
    '''

    '''
    lat_list2=[]
    lon_list2=[]

    for lat1,lat2,lon1,lon2 in zip(lat_list[:-1],lat_list[1:],lon_list[:-1],lon_list[1:]):
       length=great_circle((lat1,lon1),(lat2,lon2)).km
       if length>max_length:
           lon_avg,lat_avg=midpoint((lon1,lon2),(lat1,lat2))
           lat_tmp1,lon_tmp1=pipeline_sequencing([lat1,lat_avg],[lon1,lon_avg],max_length)
           lat_tmp2,lon_tmp2=pipeline_sequencing([lat_avg,lat2],[lon_avg,lon2],max_length)
           lat_list2.extend(lat_tmp1[:-1])
           lon_list2.extend(lon_tmp1[:-1])
           lat_list2.extend(lat_tmp2)
           lon_list2.extend(lon_tmp2)

       else:
           lat_list2.extend([lat1,lat2])
           lon_list2.extend([lon1,lon2])

       lat_list2=lat_list2[:-1]
       lon_list2=lon_list2[:-1]

    lat_list2.append(lat2)
    lon_list2.append(lon2)
    return lat_list2,lon_list2

def new_node_ID_nodes():
    for i in range(100000000):
        yield f'OSM_{i}'

def new_node_ID(x,y):
    for i in range(10000):
        yield x+'-'+y+'_'+str(i)

def old_node_IDs(id_list):
    for i in range(len(id_list)-1):
        yield id_list[i],id_list[i+1]

def create_segments_INET(pipelines,max_distance=10, verbose=True):
    "creates addition pipeline nodes and add them to the network"
    warning=False
    for pipeline in pipelines:
        if len(pipeline.lat) != len(pipeline.node_id):
            warning=True
    if warning:
        print(CC.Red+'Warning: length of id_nodes not equals length of coordinates per pipeline'+CC.End)
    countrydict=MG.CountryPolyDict()
 
    for pipe in pipelines:
        old_nodes = list(zip(pipe.lat,pipe.long))
        lat,long = pipeline_sequencing(pipe.lat,pipe.long,max_length=max_distance)
        new_nodes = list(zip(lat,long))
        old_ID_generator = old_node_IDs(pipe.node_id)
        new_node_ids = []
        first_id,second_id = next(old_ID_generator)
        new_ID_generator=new_node_ID(first_id,second_id)
        for i, new_node in enumerate(new_nodes[:-1]):
            if new_node in old_nodes:
                new_node_ids.append(first_id)
            else: new_node_ids.append(next(new_ID_generator))


            if new_nodes[i+1] in old_nodes:
                if i+1<(len(new_nodes)-1):
                    first_id,second_id = next(old_ID_generator)
                    new_ID_generator=new_node_ID(first_id,second_id)
        new_node_ids.append(second_id)
        pipe.node_id=new_node_ids
        pipe.lat=lat
        pipe.long=long
        old_countrycodes=pipe.country_code
        pipe.country_code=MG.GetCountry4List(long,lat,countrydict,old_countrycodes)
    if verbose==True:
        print('--Segmenting INET--')

    return pipelines


def create_segments(pipelines,max_distance=10):
    for pipe in pipelines:
        lat,long=pipeline_sequencing(pipe.lat,pipe.long,max_distance)
        pipe.lat=lat
        pipe.long=long
    return pipelines

def OSM_ShortSegmentRemove(Pipelines,maxlength):
    """
    Removes all pipelines with a length<maxlength[km]
    """
    for pipe in reversed(Pipelines):
#       if float(pipe.length) < maxlength:
       if float(pipe.param['length_km'])< maxlength:
           Pipelines.remove(pipe)
    pass

def OSM_Segmenting(line_long, line_lat, i, maxlength,verbose=False):
    """
    Divides a OSM Line into Segments with a length < maxlength [km] if possible
    """
    line_a_long = []
    line_b_long = []
    line_a_lat  = []
    line_b_lat  = []
    i = str(i)
    length = MD.routelength(line_long, line_lat)
    if verbose==True:
        print(f'Pipeline {i} -- Length:{length} km')

    if len(line_long) ==2:
        if float(length)>maxlength:
#            print(f'Pipeline {i} > {maxlength} km -> create interlines from interpol')
            line_lat,line_long=pipeline_sequencing(line_lat,line_long,5)
#            print(f'linelong {line_long}')
            line_long,line_lat=OSM_Segmenting(line_long,line_lat,i,maxlength)
            middle=int(round(len(line_long)//2))
            line_a_long, line_a_lat = OSM_Segmenting(line_long[0:middle],line_lat[0:middle],str(i)+'.1',maxlength)
            line_b_long, line_b_lat = OSM_Segmenting(line_long[middle:],line_lat[middle:],str(i)+'.2',maxlength)
            line_long = []
            line_lat  = []
            line_long.extend(line_a_long)
            line_long.extend(line_b_long)
            line_lat.extend(line_a_lat)
            line_lat.extend(line_b_lat)
            return line_long, line_lat

        else:
            xline_long = [line_long[0],line_long[-1]]
            xline_lat  = [line_lat[0],line_lat[-1]]
            return line_long, line_lat
    # Split lines (recursively) if they have more than 2 points and are longer then maxlength
    elif len(line_long) > 2:
        if float(length) > maxlength:
#            print(f'Pipeline {i} > {maxlength} km -> split this line')
            middle=int(round(len(line_long)//2))


            line_a_long, line_a_lat = OSM_Segmenting(
                                      line_long[0:middle+1],
                                      line_lat[0:middle+1],
                                      str(i)+'.1',maxlength)
            line_b_long, line_b_lat = OSM_Segmenting(
                                      line_long[middle:],
                                      line_lat[middle:],
                                      str(i)+'.2',maxlength)
            line_long = []
            line_lat  = []
            line_long.extend(line_a_long)
            line_long.extend(line_b_long)
            line_lat.extend(line_a_lat)
            line_lat.extend(line_b_lat)
            return line_long, line_lat
        else:
            xline_long = [line_long[0], line_long[-1]]
            xline_lat  = [line_lat[0], line_lat[-1]]
            return xline_long, xline_lat
    pass

def OSM_Pipe2Segment(pipe, i,length,verbose=False,compose=False):
    """
    Creates PipeSegments from a OSM-Pipeline
    """
    res_long, res_lat = OSM_Segmenting(pipe.long,pipe.lat,i,length,verbose=verbose)
    if verbose==True:
        print(f'res_lat: {res_lat}')
        print(f'res_long: {res_long}')

    # (int i = 0; i < list.length(); i+=2)
    pipesegments = []


    path_coords=list(zip(pipe.param['path_lat'],
                         pipe.param['path_long']))
    
    for i in range(0,len(res_long)-1,2):

        id   = pipe.id+'_Seg_'+str(int(i/2+1))
        lat  = [res_lat[i],res_lat[i+1]]
        long = [res_long[i],res_long[i+1]]
        name = pipe.id+'_Seg_'+str(int(i/2+1))

        source_id = pipe.source_id
        # try:
        #     node_id  = [pipe.node_id[i],pipe.node_id[i+1]]
        # except:
        #     node_id = 'no IDs created by pipelinesequencing'
        

        # if first_node not in current_nodes[0]
        # if current_nodes==[]:    

           # node_id=[next(new_id_generator),next(new_id_generator)]
        node_id=[]
        pipe_coords=list(zip(lat,long))
        #print('pipe_coords: ',pipe_coords)
        #print('path_coords: ',path_coords)
        if type(pipe.country_code)==str:
            pipe.country_code=[pipe.country_code]
#          self, id, name, source_id, node_id, lat, long, country_code, tags,**param
        new_path_coords=path_segmenting(pipe_coords,path_coords)
        #print('new_path:',new_path_coords)
        
        path_lat=[coord[0] for coord in new_path_coords]
        #print('pathlat:',path_lat)
        path_long=[coord[1] for coord in new_path_coords]
        
        new_param=dict(pipe.param)
        new_param['path_lat']=path_lat
        new_param['path_long']=path_long  
        country_code     = list(set(pipe.country_code))
        tags             = pipe.tags
        pipesegment      = KC.OSMComponent(id,
                                           name,
                                           source_id,
                                           node_id,
                                           lat,
                                           long,
                                           country_code,
                                           tags,
                                           param = new_param,
                                           uncertainty=pipe.uncertainty,
                                           method=pipe.method)
#        pipesegment.lat  = lat
#        pipesegment.long = long
        pipesegments.append(pipesegment)

    return pipesegments

def OSM_Pipe2Pipe(pipe, i,length,verbose=False):
    """
    Creates PipeSegments from a OSM-Pipeline
    """
    res_long, res_lat = OSM_Segmenting(pipe.long,pipe.lat,i,length,verbose=verbose)
    if verbose==True:
        print(f'res_lat: {res_lat}')
        print(f'res_long: {res_long}')

    # (int i = 0; i < list.length(); i+=2)

    
    new_long=[]
    for i in range(0,len(res_long)-1,2):
        a,b = res_long[i:i+2]
        save=b
        new_long.append(a)
    new_long.append(save)

    new_lat=[]
    for i in range(0,len(res_long)-1,2):
        a,b = res_lat[i:i+2]
        save=b
        new_lat.append(a)
    new_lat.append(save)

    id   = pipe.id
    lat  = new_lat
    long = new_long
    name = pipe.id

    source_id = pipe.source_id
        # try:
        #     node_id  = [pipe.node_id[i],pipe.node_id[i+1]]
        # except:
        #     node_id = 'no IDs created by pipelinesequencing'
        

        # if first_node not in current_nodes[0]
        # if current_nodes==[]:    

           # node_id=[next(new_id_generator),next(new_id_generator)]
    node_id=[]

    if type(pipe.country_code)==str:
        pipe.country_code=[pipe.country_code]
        
#          self, id, name, source_id, node_id, lat, long, country_code, tags,**param


    country_code     = list(set(pipe.country_code))
    tags             = pipe.tags
    pipeline     = KC.OSMComponent(id,
                                       name,
                                       source_id,
                                       node_id,
                                       lat,
                                       long,
                                       country_code,
                                       tags,
                                       param = pipe.param,
                                       uncertainty=pipe.uncertainty,
                                       method=pipe.method)
#        pipesegment.lat  = lat
#        pipesegment.long = long
    # pipelines.append(pipeline)

    return pipeline


def OSM_Pipelines2Segments(Component,length,verbose=False):
    """
    Creates PipeSegments from a list of OSM-Pipelines
    """
    linelist=[]
               
        
                 
    for i,pipe in enumerate(Component):
        lines=OSM_Pipe2Segment(pipe,i,length,verbose=verbose)
#        print(lines)
        for line in lines:
            linelist.append(line)

    # Component.clear()
    # Component.extend(linelist)
    return linelist

def OSM_Pipelines2Pipelines(Component,length,verbose=False):
    """
    Creates PipeSegments from a list of OSM-Pipelines
    """
    linelist=[]
               
    for i,pipe in enumerate(Component):
        line=OSM_Pipe2Pipe(pipe,i,length,verbose=verbose)
        linelist.append(line)
#        print(lines)


    # Component.clear()
    # Component.extend(lines)
    return linelist


def OSM_PipelineSegmenting(Component,length=40,minlength=3.0,verbose=False,composed=False):
    """
    Segmenting of OSM-PipeLines to PipeSegments with a length < maxlength
    Removing Segments < minlength
    length in deg^2
    """
    if verbose==True:
        print(CC.Cyan + 'Start Pipesegmenting:'+ CC.End)
    if composed==False:
        NewComponent=OSM_Pipelines2Segments(Component,length,verbose=verbose)
        if verbose==True:
            print(CC.Cyan + 'Recalculate lengths for all Segments' + CC.End)
        MD.set_lengths(NewComponent)
        if verbose==True:
            print(CC.Cyan + 'Remove all short Segments '+ str(minlength) + CC.End)
        OSM_ShortSegmentRemove(NewComponent,minlength)
    else:
        NewComponent=OSM_Pipelines2Pipelines(Component,length,verbose=verbose)
        


    return NewComponent


def average(a,b):
    res_a = (a[0]+a[1])/2
    res_b = (b[0]+b[1])/2
    return res_a,res_b


def midpoint(a,b):
    from math import pi,cos,sin,atan2,sqrt

    lon1 = a[0]/180*pi
    lon2 = a[1]/180*pi
    lat1 = b[0]/180*pi
    lat2 = b[1]/180*pi

    Bx     = cos(lat2) * cos(lon2-lon1)
    By     = cos(lat2) * sin(lon2-lon1)
    latMid = atan2(sin(lat1) + sin(lat2), sqrt( (cos(lat1)+Bx)*(cos(lat1)+Bx) + By*By ) )
    lonMid = lon1 + atan2(By, cos(lat1) + Bx)
    return round(lonMid/pi*180,5),round(latMid/pi*180,5)

#%%
if __name__=="__main__":
    import os
    os.chdir('..')

    pipes=create_segments_INET(INET.PipeSegments)


    # a=[40,53.939785, 54.801878, 54.80609]
    # b=[10,9.784432, 9.289041, 9.29094]

    # print(pipeline_sequencing(b,a,200))
    # print('ada')

#     lat: [56.962682700000244, 56.96265560000024, 56.96261540000024, 56.962586600000236]
# long: [24.03559059999993, 24.03558749999993, 24.03675789999993, 24.03675569999993]
