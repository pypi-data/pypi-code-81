"""Read funktion: OSM Data (pipelines) into K_Net Class"""

#######################################################################
#All functions are called from the makefile                           #
#######################################################################

from .M_PlotObjects import routelength

# from Code.OSM.M_OSM_CreateElements import M_OSM_CreateElements
from . import OSM_Pipeline_CountryCode as OP
from . M_OSM_PipeSegmenting import new_node_ID_nodes
from copy import deepcopy
from . import M_OSM_PipeSegmenting as PS

from unidecode import unidecode

# import configparser
# from  configparser import  ExtendedInterpolation
# from  pathlib            import Path
# import os
# import time
import sys
import json

# import Code.C_colors              as CC
from . import K_Netze as K_Netze
from . import K_Component as KC


def PipeSegments2Nodes(Pipelines):
    lat_list = []
    long_list = []
    id_list = []
    for pipe in Pipelines:
        for entry in zip(pipe.lat, pipe.long, pipe.node_id):
            lat_list.append(entry[0])
            long_list.append(entry[1])
            id_list.append(entry[2])
    return [lat_list, long_list, id_list]


def FindNodes4Pipelines(pipelines, nodes,new_nodes):
    for pipe in pipelines:
        for lat, long in zip(pipe.lat, pipe.long):
            for node in nodes:
                if lat == node.lat and long == node.long:
                    if node.id!=[]:
                        pipe.node_id.append(node.id)
                    #schaue in neu generierten punkten nach
                    else:
                        for new_node in new_nodes:
                            if lat == new_node.lat and long == new_node.long:
                                if new_node.id!=[]:
                                    pipe.node_id.append(new_node.id)
    pass


def PipeLine_length_error(pipelines, pipesegments):
    for pipe in pipelines:
        error = 0
        for segment in pipesegments:
            segment_id = segment.id.rpartition("_Seg_")[0]
            if pipe.id == segment_id:
                error += float(segment.uncertainty["length_km"])
        pipe.uncertainty["length_km"] = (round(error * 1000) / 1000)
    pass


def OSMways2net(elements, data, min_length=0):

    """ Convert OSMways to plotable lines """

    refs = []
    lines = []
    ids = []
    lengths = []
    tags = []
    tagdicts = []
    node_ids = []
    if "Way" in elements.keys():
        node_id_list = []
        for entry in elements["Way"]:
            refs = elements["Way"][entry]["refs"]
            lonlat_array = []
            node_id_list = []
            for ID in refs:
                lonlat_array.append(data["Node"][str(ID)]["lonlat"])
                node_id_list.append("OSM-" + str(ID))
            node_ids.append(node_id_list)
            long = []
            lat = []
            line = []

            for coords in lonlat_array:
                long.append(coords[0])
                lat.append(coords[1])
            linelength = float(routelength(long, lat))
            tag = (
                unidecode(
                    json.dumps(
                        elements["Way"][entry]["tags"], ensure_ascii=False, indent=2
                    )
                )
                .replace("{", "")
                .replace("}", "")
                .replace('\\"', "")
            )
            tagdict = elements["Way"][entry]["tags"]
            line = [long, lat]
            # only lines longer than min_length
            if linelength >= min_length:
                lines.append(line)
                lengths.append(float(linelength))
                ids.append("OSM-" + entry)
                tags.append(tag)
                tagdicts.append(tagdict)
    #                node_ids.append(refs)
    return lines, ids, lengths, tags, node_ids, tagdicts


def OSMnodes2net(elements):

    """ Convert OSMways to plotable lines """

    nodes = []
    ids = []
    tags = []
    node_ids = []
    tagdicts = []

    if "Node" in elements.keys():
        for entry in elements["Node"]:
            idd = elements["Node"][entry]["id"]
            node_ids.append(idd)
            long = elements["Node"][entry]["lonlat"][0]
            lat = elements["Node"][entry]["lonlat"][1]
            tag = (
                unidecode(
                    json.dumps(
                        elements["Node"][entry]["tags"], ensure_ascii=False, indent=2
                    )
                )
                .replace("{", "")
                .replace("}", "")
                .replace('\\"', "")
            )
            tagdict = elements["Node"][entry]["tags"]
            tagdicts.append(tagdict)
            node = [long, lat]
            nodes.append(node)
            ids.append(entry)
            tags.append(tag)

    return nodes, ids, tags, node_ids, tagdicts


def OSMways2nodes(elements, data, min_length=0):

    """Convert OSM Pipeline endpoints to Nodes"""

    refs = set()
    if "Way" in elements:
        refs = set(
            ref for way_id, entry in elements["Way"].items() for ref in entry["refs"]
        )

    refs = list(refs)
    new_ids = set("OSM-%s" % ref for ref in refs)
    points = {}

    for point in data["Node"]:
        point_id = "OSM-%s" % data["Node"][point]["id"]
        if point_id in new_ids:
            data["Node"][point]["id"] = point_id
            points[point_id] = data["Node"][point]

    return {"Node": points}


def extract_lat_longs(Component):
    lat_longs = []

    for pipe in Component:
        for pipelat, pipelong in zip(pipe.lat, pipe.long):
            lat_longs.append((pipelat, pipelong))
    return set(lat_longs)


def RawData2ClassData(
    Data,
    elements,
    JSON_outputfile,
    TM_World_Borders_file,
    countrycode,
    CreateCountryCodeForLines=False,
    LoadCountryCodeForLines=False,
    min_length=1,
    segment_length=100,
    verbose=False,
):

    Ret_Data = K_Netze.NetComp_OSM()

    ########
    # Pipeline
    ########
    print("---Load Pipelines---")
    [lines, ids, lengths, tags, node_ids, tagdicts] = OSMways2net(
        elements["pipelines"], Data, min_length=min_length
    )
    # pipenodes_dict=OSMways2nodes(elements["pipelines"],Data,min_length=0)
    i = 0
    length_uncertainty_factor = 0.3
    if segment_length == 0:
        length_uncertainty_factor = 0
    for i, entry in enumerate(zip(lines, ids, lengths, tags)):
        PipeLine = KC.OSMComponent(
            id=ids[i],
            name=ids[i],
            node_id=[],  # node_ids[i],
            source_id=["OSM"],
            lat=lines[i][1],
            long=lines[i][0],
            country_code=countrycode,
            tags=tagdicts[i],
            param={"length_km": float(lengths[i]),"path_lat":lines[i][1],"path_long":lines[i][0]},
            method={"length_km": "SciGRID_gas"},
            uncertainty={},
        )
        # ,                                 length=lengths[i])

        Ret_Data.PipeLines.append(PipeLine)


    # here wieder rein
    deepcopy(Ret_Data.PipeLines)
    Ret_Data.PipeSegments = PS.OSM_PipelineSegmenting(
        deepcopy(Ret_Data.PipeLines), length=segment_length, minlength=min_length
    )
    Ret_Data.PipeLines = PS.OSM_PipelineSegmenting(
        Ret_Data.PipeLines, length=segment_length, minlength=min_length, composed=True
    )
    # for pipe in Ret_Data.PipeLines:
        # print(pipe.param)
        # print(pipe.lat)
    for pipe in Ret_Data.PipeLines:
        pipe.param["length_km"] = pipe.getPipeLength()
    node_coords = extract_lat_longs(Ret_Data.PipeSegments)
    new_ID_generator = new_node_ID_nodes()
    node_list_ids = [next(new_ID_generator) for node in node_coords]
    nodes_id_dict = {}
    for coord, node_id in zip(node_coords, node_list_ids):
        nodes_id_dict.update({coord: node_id})

    for pipe in Ret_Data.PipeSegments:
        first_node = (pipe.lat[0], pipe.long[0])
        second_node = (pipe.lat[1], pipe.long[1])
        node_id = [nodes_id_dict[first_node], nodes_id_dict[second_node]]
        pipe.node_id = node_id

    for pipe in Ret_Data.PipeSegments:
        length = pipe.param["length_km"]
        pipe.uncertainty["length_km"] =  length_uncertainty_factor * float(length)

    print("---Load Nodes---")
    pipenodes = OSMways2nodes(elements["pipelines"], Data, min_length=min_length)
    # print(len(pipenodes['Node']))
    # print(pipenodes['Node'])
    [nodes, ids, tags, node_ids, tagdicts] = OSMnodes2net(pipenodes)

    for i, entry in enumerate(zip(nodes, ids, tags, node_ids, tagdicts)):
        Node = KC.OSMComponent(
            id=ids[i],
            name=ids[i],
            node_id=[node_ids[i]],
            source_id=["OSM"],
            lat=nodes[i][1],
            long=nodes[i][0],
            country_code=countrycode,
            param={},
            uncertainty={},
            method={},
            tags=tagdicts[i],
        )

        Ret_Data.Nodes.append(Node)


    pipelist = PipeSegments2Nodes(Ret_Data.PipeSegments)

    # transpose
    pipelist = list(map(list, zip(*pipelist)))

    # unique
    pipelist = [tuple(row) for row in pipelist]
    pipelist = set(pipelist)
    # pipelist=[list(row) for row in pipelist]
    # transpose back
    pipelist = list(map(list, zip(*pipelist)))
    if len(pipelist)==0:
        print("No pipelines found")
        sys.exit()
    lats, longs, ids = pipelist

    for i, entry in enumerate(zip(lats, longs, ids)):
        PipePoint = KC.OSMComponent(
            id=ids[i],
            name=ids[i],
            node_id=[],
            source_id=["OSM_Seq"],
            lat=lats[i],
            long=longs[i],
            country_code=countrycode,
            param={},
            uncertainty={},
            method={},
            tags={},
        )
        Ret_Data.PipePoints.append(PipePoint)

    #PipePoints are only newly created points
    Ret_Data.PipePoints = sorted(
        Ret_Data.PipePoints, key=lambda PipePoints: int(PipePoints.id[4:])
    )
    
    FindNodes4Pipelines(Ret_Data.PipeLines, Ret_Data.Nodes,Ret_Data.PipePoints)
    #Merging new generated points to point table
    Ret_Data.Nodes=Ret_Data.Nodes+Ret_Data.PipePoints
    PipeLine_length_error(Ret_Data.PipeLines, Ret_Data.PipeSegments)
    if CreateCountryCodeForLines == True:

        OP.Create_Pipelines_CountryCodes(
            JSON_outputfile, TM_World_Borders_file, Ret_Data, 
            countrycode, verbose=False)

    if LoadCountryCodeForLines == True:
        print("---Load Line Countrycodes--")
        OP.Load_Pipelines_Countrycodes(JSON_outputfile, Ret_Data, 
                                       countrycode)
        OP.Load_Pipesegments_Countrycodes(JSON_outputfile, Ret_Data, 
                                                countrycode)
                  
    return Ret_Data

