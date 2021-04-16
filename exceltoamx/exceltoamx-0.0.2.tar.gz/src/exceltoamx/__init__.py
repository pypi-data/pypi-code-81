from logging import error


def _name_systems(*args):
    import re
    result = []

    for system in args:
        # leading zeroes
        system['room_number'] = str(system['room_number']).zfill(3)
        system['full_name'] = system['building_name'] + system['room_number']

        try:
            system['system_number'] = str(system['system_number'])
        except KeyError:
            pass

        try:
            system['space_use_code'] = str(system['space_use_code'])
        except KeyError:
            pass

        # Model-Number(G4) else Massio
        try:
            tp_match = r'(?<=[(])(\w+)'  # find text inside parenthesis
            if re.search(tp_match, system['tp_model']) is not None:
                system['tp_generation'] = re.search(tp_match, system['tp_model']).group(0)
            # catches keypads
            else: system['tp_generation'] = system['tp_model']
        except KeyError:
            pass

        result.append(system)
    return result


def xlsx_to_dict_list(path):
    import json
    from tablib import Dataset
# also requires xlrd, may get incorrect error about openpyxl
    """
    Dictionary keys are populated from the top row of data in the
	.xlsx file. Each additional row is turned into a dictionary
	with the values from that row.
    Then all of the rows/dictionaries are put into a list and
    returned. We could also return the xlsx dataset, but there's
    no current use for it so I left that commented out.
    :param path: path to .xlsx file
    :return: list of dictionaries
    """
    try:
        data = Dataset()
        with open(path, 'rb') as file:
            data.load(file, 'xlsx')
        #  json and back is the cleanest way to get to dict list
        systems = json.loads(data.json)  # , data
        result = _name_systems(*systems)
        return result
    except Exception as e:
        error(f"exceltoamx.py xlsx_to_dict_list() {e}")
        return
