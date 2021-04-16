import json
from enrichwrap import get_contents


def get_steps(step_string=None):
    """
    args: The list of arguments as would be passed in from the command line or the IDE's run.
            This list starts after the 0th element (the python file name)

    returns: dictionary, describing the steps aka how the enrichment tools will be called, and failovers and percentages
    """
    json_dictionary = {}
    if step_string is not None:
        print('Parse input of %s' % step_string)
        json_dictionary = parse_incoming_string(step_string)

    # If the string is not specified, or cannot be parsed, then use the file as a backup
    if len(json_dictionary.keys()) == 0:
        with open(get_contents('samples', 'sample_steps.json')) as json_file:
            step_dictionary = json.load(json_file)
    else:
        step_dictionary = json_dictionary

    return step_dictionary


def parse_incoming_string(incoming_string):
    json_dictionary = {}
    sample_list = []
    split_str = incoming_string.split(',')
    step_string = ''
    astr = ''
    for astr in split_str:
        if astr.find(':') > 0:
            if len(step_string) > 0:
                step_string += ','
            step_string += astr
        elif step_string != '':
            sample_list.append(get_step_definition(step_string))
            step_string = astr
        else:
            step_string = astr
    sample_list.append(get_step_definition(astr))

    json_dictionary["steps"] = sample_list
    #print(json.dumps(json_dictionary))
    return json_dictionary


def get_failover(step_string):
    if step_string.find(';') < 0 and step_string.find('|') < 0:
        return step_string
    steps = {}
    main_step_str = step_string
    failover_step_str = ''
    if step_string.find('|') > 0:
        main_step_str = step_string[0: step_string.find('|')]
        failover_step_str = step_string[step_string.find('|')+1:]
    steps['what'] = main_step_str
    steps['failoverWhat'] = failover_step_str
    my_list = []
    for astr in main_step_str.split(';'):
        my_list.append(astr)
    steps['serialsteps'] = my_list
    failover_list = []
    for astr in failover_step_str.split(';'):
        failover_list.append(astr)
    steps['failoversteps'] = failover_list
    return steps


def get_step_definition(step_string):
    step_dictionary = {'what': step_string}
    step_list = []
    # If step_string contains a comma, then there are more than one steps to create, with the bounds as defined
    for astr in step_string.split(','):
        if astr.find(':') > 0:
            enrich_str = astr[0:astr.find(':')]
            percentage_bit = astr[astr.find(':')+1:]
            lower_bound = percentage_bit[0: percentage_bit.find('-')]
            upper_bound = percentage_bit[percentage_bit.find('-')+1:]
            this_step = {'stepBoundsLower': int(lower_bound), 'stepBoundsUpper': int(upper_bound), 'what': enrich_str}
            if enrich_str.find('|') > 0 or enrich_str.find(';') > 0:
                this_step['steps'] = get_failover(enrich_str)
            step_list.append(this_step)
        else:
            this_step = {'what': astr}
            if astr.find('|') > 0 or astr.find(';') > 0:
                this_step['steps'] = get_failover(astr)
            step_list.append(this_step)
    step_dictionary['steps'] = step_list
    return step_dictionary

