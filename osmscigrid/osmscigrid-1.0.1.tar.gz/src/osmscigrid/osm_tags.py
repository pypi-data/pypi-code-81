from quantulum3 import parser

def extract_values(tag_dict_list, parameter,verbose=False):

    counterlist = []
    valuelist = []
    unitylist = []

    for i, tag_dict in enumerate(tag_dict_list):
        if parameter in tag_dict:
            if parameter in ['operator','start_operator']:
                value=tag_dict[parameter]
                valuelist.append(value)
            else:    
                value = parser.parse(tag_dict[parameter])
                print(tag_dict[parameter])
                if value != []:
                    if verbose==True:
                        print(i, tag_dict[parameter], value[0].unit.name)
                    unitylist.append(value[0].unit.uri)
                    valuelist.append(value[0].value)
            if value != []:
                counterlist.append(i)
               
                
    return counterlist, valuelist, unitylist

def values_to_pipeline(
    elements, pipe_numbers, values, value_name):
    for i, value in zip(pipe_numbers, 
                           values):
        elements[i].param.update({value_name: value})
        elements[i].uncertainty.update({value_name: 0})
        elements[i].method.update({value_name: "OSM"})
    pass

def values_to_pipeline_diameters(
    elements, pipe_numbers, diameter_values, diameter_unities
):
   

    for i, diameter, unit in zip(pipe_numbers, 
                                 diameter_values, 
                                 diameter_unities):

        if unit == "Centimeter":
            diameter = diameter * 10
        if unit == "Meter":
            diameter = diameter * 100
        if unit == "Inch":
            diameter = diameter * 25.4
        if unit == "Dimensionless_quantity" and diameter < 2:
            diameter = diameter * 1000

        elements[i].param.update({"diameter_mm": int(diameter)})
        elements[i].uncertainty.update({"diameter_mm": 0})
        elements[i].method.update({"diameter_mm": "OSM"})
    pass

def values_to_pipeline_pressures(
    elements, pipe_numbers, pressure_values, pressure_unities):
    for i, pressure, unit in zip(pipe_numbers, 
                                 pressure_values, 
                                 pressure_unities):

        if unit == "MPa":
            pressure = pressure * 10

        if pressure > 1000:
            pressure = None
                                             
        elements[i].param.update({"max_pressure_bar": pressure})
        elements[i].uncertainty.update({"max_pressure_bar": 0})
        elements[i].method.update({"max_pressure_bar": "OSM"})
    pass
        
def extract_tags(NET,verbose=False):
    tags_pipelines = NET.all("PipeLines", "tags", verbose=False)
    
    tags_pipesegments = NET.all("PipeSegments", "tags", verbose=False)

    component_names=['PipeSegments','PipeLines']
    components=[NET.PipeSegments,NET.PipeLines]
    tags_components=[tags_pipesegments,tags_pipelines]
  
    for tags_component,component,component_name in zip(tags_components,components,component_names):
    # Export Values to PipeSegments
        diameter_lines, diameter_values, diameter_unities = extract_values(
            tags_component, "diameter")
            
        values_to_pipeline_diameters(
            component, diameter_lines, diameter_values, diameter_unities)
            
        pressure_lines, pressure_values, pressure_unities = extract_values(
            tags_component, "pressure")
            
        values_to_pipeline_pressures(
            component, pressure_lines, pressure_values, pressure_unities)

        operator_lines, operator_values, operater_unities = extract_values(
            tags_component, "operator")

        values_to_pipeline(
            component, operator_lines, operator_values,"operator")

        operator_lines, operator_values, operater_unities = extract_values(
            tags_component, "start_date")

        values_to_pipeline(
            component, operator_lines, operator_values,"start_date")

            
        num_pipe = len(component)
        if verbose==True:    

            print(len(diameter_lines), " diameter values for ", 
                  num_pipe, component_name)
            print(len(pressure_lines), " pressure values for ", 
                  num_pipe, component_name)
    # Export Values to PipeSegments
    return NET
