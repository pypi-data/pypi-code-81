def pathcorrection(OSM):
    line_components=[OSM.__dict__['PipeLines'],OSM.__dict__['PipeSegments']]
    for line_component in line_components:
        for line in line_component:
            line.__dict__["param"]["path_lat"]=\
                line.__dict__["param"]["path_lat"][1:-1]
            line.__dict__["param"]["path_long"]=\
                line.__dict__["param"]["path_long"][1:-1]
           
    return OSM
