import xml.etree.ElementTree as ET
import shortuuid

bpmn_schema_url = 'http://www.omg.org/spec/BPMN/20100524/MODEL'
camunda_schema_url = 'http://camunda.org/schema/1.0/bpmn'
simod_schema_url = 'http://www.qbp-simulator.com/Schema201212'
bpmn_element_ns = {'xmlns': bpmn_schema_url}
camunda_element_ns = {'xmlns': camunda_schema_url}
simod_ns = {'qbp': simod_schema_url}

elements = {
    'exclusive_gateway': 'exclusiveGateway',
    'task': 'task',
}


def retrieve_incoming_flows(process_root, task_id):
    incoming_sequence_flows = []

    for sequence_flow in process_root.findall("xmlns:sequenceFlow", bpmn_element_ns):
        if sequence_flow.attrib['targetRef'] == task_id:
            incoming_sequence_flows.append(sequence_flow)

    return incoming_sequence_flows


def retrieve_outgoing_flows(process_root, task_id):
    outgoing_sequence_flows = [];

    for sequence_flow in process_root.findall("xmlns:sequenceFlow", bpmn_element_ns):
        if sequence_flow.attrib['sourceRef'] == task_id:
            outgoing_sequence_flows.append(sequence_flow)

    return outgoing_sequence_flows


def generate_exclusive_gateway(gateway_id):
    exclusive_gateway = ET.Element("bpmn:exclusiveGateway")
    exclusive_gateway.set('id', gateway_id)

    return exclusive_gateway


def generate_incoming_flow(id):
    incoming_flow = ET.Element("bpmn:incoming")
    incoming_flow.text = id

    return incoming_flow


def generate_outgoing_flow(id):
    outgoing_flow = ET.Element("bpmn:outgoing")
    outgoing_flow.text = id

    return outgoing_flow


def add_incoming_flows_to_gateway(gateway, incoming_flows):
    new_gateway = gateway

    for incoming_flow in incoming_flows:
        incoming = generate_incoming_flow(incoming_flow.attrib['id'])
        new_gateway.append(incoming)

    return new_gateway


def add_outgoing_flows_to_gateway(gateway, outgoing_flows):
    new_gateway = gateway

    for outgoing_flow in outgoing_flows:
        outgoing = generate_outgoing_flow(outgoing_flow.attrib['id'])
        new_gateway.append(outgoing)

    return new_gateway


def generate_sequence_flow(id, source_ref, target_ref):
    new_sequence_flow = ET.Element("bpmn:sequenceFlow")
    new_sequence_flow.set('id', id)
    new_sequence_flow.set('sourceRef', source_ref)
    new_sequence_flow.set('targetRef', target_ref)

    return new_sequence_flow


def add_sequence_flow_to_process(process_root, sequence_flow):
    new_process_root = process_root
    new_process_root.append(sequence_flow)

    return new_process_root


def remove_duplicate_incoming(process_root):
    new_process_root = process_root
    prev = None

    for child in new_process_root.getchildren():
        for incoming in child.findall('xmlns:incoming', bpmn_element_ns):
            if type(incoming) == type(prev) and incoming.text == prev.text:
                child.remove(incoming)
            prev = incoming

    return new_process_root


def remove_duplicate_outgoing(process_root):
    new_process_root = process_root
    prev = None

    for child in new_process_root.getchildren():
        for outgoing in child.findall('xmlns:outgoing', bpmn_element_ns):
            if type(outgoing) == type(prev) and outgoing.text == prev.text:
                child.remove(outgoing)
            prev = outgoing

    return new_process_root


def update_sequence_flow_targets(process_root, sequence_flow_ids, target_ref):
    new_process_root = process_root

    for sequence_flow in new_process_root.findall("xmlns:sequenceFlow", bpmn_element_ns):
        if sequence_flow.attrib['id'] in sequence_flow_ids:
            sequence_flow.set('targetRef', target_ref)

    return new_process_root


def add_gateway_before_task(root, task_id, prev_gateway_id):
    process_root = root.find("xmlns:process", bpmn_element_ns);

    # GET ALL INCOMING FLOWS TO THE TASK THAT IS TO BE MODIFIED
    incoming_flows = retrieve_incoming_flows(process_root, task_id)
    incoming_flow_ids = list(map(lambda in_flow: in_flow.attrib['id'], incoming_flows))

    # CREATE A NEW EXCLUSIVE GATEWAY
    previous_gateway = generate_exclusive_gateway(prev_gateway_id)

    # FOR EACH INCOMING FLOW, ADD A <bpmn:incoming>FLOW_ID</bpmn:incoming> IN THE EXCLUSIVE GATEWAY
    previous_gateway = add_incoming_flows_to_gateway(previous_gateway, incoming_flows)

    # CREATE A NEW SEQUENCE FLOW (SOURCE: NEW GATEWAY, TARGET: TASK)
    previous_sequence_flow = generate_sequence_flow(f"Flow_{shortuuid.uuid()}", previous_gateway.attrib['id'], task_id)

    # ADD A <bpmn:outgoing>NEW_FLOW_ID</bpmn:outgoing> IN THE NEW EXCLUSIVE GATEWAY
    outgoing = generate_outgoing_flow(previous_sequence_flow.attrib['id'])
    previous_gateway.append(outgoing)

    # ADD THE NEW GATEWAY(INCOMING, NEW_OUTGOING[PREV_SEQUENCE_FLOW]) and PREV_SEQUENCE_FLOW TO THE PROCESS
    process_root.append(previous_sequence_flow)
    process_root.append(previous_gateway)

    # UPDATE INCOMING SEQUENCE FLOWS TO HAVE TARGET REF OF THE PRECEDING GATEWAY INSTEAD OF THE TASK
    process_root = update_sequence_flow_targets(process_root, incoming_flow_ids, previous_gateway.attrib['id'])

    # UPDATE INCOMING AND OUTGOING WITHIN TASKS AND OTHER EVENTS TO REFLECT CHANGES IN FLOW
    for child in process_root.getchildren():
        if child.attrib['id'] == task_id:
            for incoming in child.findall("xmlns:incoming", bpmn_element_ns):
                if incoming.text in incoming_flow_ids:
                    child.remove(incoming)

            new_incoming = generate_incoming_flow(previous_sequence_flow.attrib['id'])
            child.append(new_incoming)

    # for child in process_root.getchildren():
    #     for outgoing in child.findall("xmlns:outgoing", bpmn_element_ns):
    #         if outgoing.text in incoming_flow_ids:
    #             outgoing.text = previous_sequence_flow.attrib['id']

    return root


def add_gateway_after_task(root, task_id, next_gateway_id):
    process_root = root.find("xmlns:process", bpmn_element_ns);

    # GET ALL SEQUENCE FLOWS OUTGOING FROM THE TASK
    outgoing_flows = retrieve_outgoing_flows(process_root, task_id)
    outgoing_flow_ids = list(map(lambda in_flow: in_flow.attrib['id'], outgoing_flows))

    # CREATE A NEW EXCLUSIVE GATEWAY
    next_gateway = generate_exclusive_gateway(next_gateway_id)

    # FOR EACH OUTGOING FLOW, ADD A <bpmn:incoming>FLOW_ID</bpmn:incoming> IN THE EXCLUSIVE GATEWAY
    next_gateway = add_incoming_flows_to_gateway(next_gateway, outgoing_flows)

    # FOR EACH OUTGOING FLOW:
    # GENERATE NEW OUTGOING SEQUENCE FLOWS, (SOURCE: NextGateway, TARGET: OutgoingFlow.target)
    # LINK THE NEW OUTGOING SEQUENCE FLOW TO OUTGOING OF THE EXCLUSIVE GATEWAY (<bpmn:outgoing>NEW FLOW</bpmn:outgoing>)
    # LINK THE NEW OUTGOING SEQUENCE FLOW TO INCOMING OF THE TASK
    # WHICH WAS THE TARGET OF ORIGINAL OUTGOING FLOW (<bpmn:incoming>NEW FLOW</bpmn:incoming>)

    for index, outgoing_flow in enumerate(outgoing_flows):
        new_outgoing_sequence_flow = generate_sequence_flow(f"Flow_{shortuuid.uuid()}",
                                                            next_gateway.attrib['id'],
                                                            outgoing_flow.attrib['targetRef'])
        next_gateway = add_outgoing_flows_to_gateway(next_gateway, [new_outgoing_sequence_flow])

        for child in process_root.getchildren():
            for incoming in child.findall("xmlns:incoming", bpmn_element_ns):
                if incoming.text in outgoing_flow_ids:
                    incoming.text = new_outgoing_sequence_flow.attrib['id']

        process_root.append(new_outgoing_sequence_flow)

    # UPDATE THE TARGET OF THE PREVIOUSLY EXISTING OUTGOING SEQUENCE FLOW TO THE NEXT GATEWAY
    process_root = update_sequence_flow_targets(process_root, outgoing_flow_ids, next_gateway.attrib['id'])

    # APPEND THE GATEWAY TO PROCESS ROOT
    process_root.append(next_gateway)

    return root


def link_gateways(root, prev_gateway_id, next_gateway_id):
    process_root = root.find("xmlns:process", bpmn_element_ns);

    # GENERATE NEW SEQUENCE FLOW (Source: prev id, Target: next id)
    new_sequence_flow = generate_sequence_flow(f"Flow_{shortuuid.uuid()}", prev_gateway_id, next_gateway_id)
    process_root = add_sequence_flow_to_process(process_root, new_sequence_flow)

    # ADD NEW OUTGOING TO PREV GATEWAY WITH NEW SEQUENCE FLOW ID <bpmn:outgoing>
    # ADD NEW INCOMING TO NEXT GATEWAY WITH NEW SEQUENCE FLOW ID <bpmn:incoming>

    for gateway in process_root.getchildren():
        if gateway.attrib['id'] == prev_gateway_id:
            add_outgoing_flows_to_gateway(gateway, [new_sequence_flow])

        if gateway.attrib['id'] == next_gateway_id:
            add_incoming_flows_to_gateway(gateway, [new_sequence_flow])

    return new_sequence_flow


def reset_incoming_outgoing_tags(root):
    new_process_root = root.find("xmlns:process", bpmn_element_ns);

    for child in new_process_root.getchildren():
        for incoming in child.findall("xmlns:incoming", bpmn_element_ns):
            child.remove(incoming)

    for child in new_process_root.getchildren():
        for outgoing in child.findall("xmlns:outgoing", bpmn_element_ns):
            child.remove(outgoing)

    for sequenceFlow in new_process_root.findall("xmlns:sequenceFlow", bpmn_element_ns):
        source_node = sequenceFlow.attrib['sourceRef']
        target_node = sequenceFlow.attrib['targetRef']
        flow_id = sequenceFlow.attrib['id']

        for process_child in new_process_root.getchildren():
            if process_child.attrib['id'] == source_node:
                outgoing_tag = generate_outgoing_flow(flow_id)
                process_child.append(outgoing_tag)

            if process_child.attrib['id'] == target_node:
                incoming_tag = generate_incoming_flow(flow_id)
                process_child.append(incoming_tag)

    return root


def parse_camunda_attributes(root):
    # FOR EACH TASK IN BPMN, ADD ENTRY IN DICTIONARY e.g. { task_id: { isEssential: "1" } }
    # RETURN DICTIONARY
    attributes = dict()

    for process in root.findall('xmlns:process', bpmn_element_ns):
        for index, task in enumerate(process.findall('xmlns:task', bpmn_element_ns)):
            task_id = task.attrib["id"]
            attributes[task_id] = dict()

            for extensionElements in task.findall('xmlns:extensionElements', bpmn_element_ns):
                for properties in extensionElements.findall('xmlns:properties', camunda_element_ns):
                    for camundaProperty in properties.findall('xmlns:property', camunda_element_ns):
                        property_name = camundaProperty.attrib['name']
                        property_value = camundaProperty.attrib['value']

                        attributes[task_id][property_name] = property_value

    return attributes


def should_add_exclusive_gateways(task_id, task_attributes):
    # FOR NOW; WE WILL ONLY CHECK IF THE DICTIONARY ENTRY FOR TASK ID HAS isEssential EQUAL TO 0
    task_attribute = task_attributes[task_id]

    if task_attribute['isEssential'] and task_attribute['isEssential'] == "0":
        return True
    else:
        return False


def is_camunda_model(root):
    if root.attrib['exporter'] and root.attrib['exporter'] == 'Camunda Modeler':
        return True
    else:
        return False


def add_conditional_gateways(temp_bpmn_file):
    root = parse_bpmn_from(temp_bpmn_file);

    if is_camunda_model(root):
        task_attributes = parse_camunda_attributes(root)
    else:
        print('is not a camunda model')
        return

    for process in root.findall('xmlns:process', bpmn_element_ns):
        for index, task in enumerate(process.findall('xmlns:task', bpmn_element_ns)):
            task_id = task.attrib["id"]
            if should_add_exclusive_gateways(task_id, task_attributes):
                # add_exclusive_gateways_for(task_id, f"PrevGateway_{task_id}", f"NextGateway_{task_id}")
                print('update implementation')

    return root


# PERTURBATOR CODE


def parse_bpmn_from(file_path):
    ET.register_namespace('bpmn', bpmn_schema_url)
    ET.register_namespace('camunda', camunda_schema_url)

    tree = ET.parse(file_path)
    return tree


def write_to_file(file_tree, file_path):
    file_tree.write(file_path, xml_declaration=True)


def find_flow_by_id(parsed_bpmn, flow_id):
    for sequenceFlow in parsed_bpmn.findall("xmlns:sequenceFlow", bpmn_element_ns):
        if sequenceFlow.attrib['id'] == flow_id:
            return sequenceFlow

    return False


def generate_element(element_tag, element_id):
    element = ET.Element(f"bpmn:{element_tag}")
    element.set('id', element_id)

    return element


def add_incoming_to_element(element, incoming_sequence_flows):
    new_element = element

    for incoming_flow in incoming_sequence_flows:
        incoming = generate_incoming_flow(incoming_flow.attrib['id'])
        new_element.append(incoming)

    return new_element


def add_outgoing_to_element(element, outgoing_sequence_flows):
    new_element = element

    for outgoing_flow in outgoing_sequence_flows:
        outgoing = generate_outgoing_flow(outgoing_flow.attrib['id'])
        new_element.append(outgoing)

    return new_element


def remove_element_by_id(root, element_id):
    new_root = root

    for process in new_root.getchildren():
        for element in process.getchildren():
            if element.attrib['id'] == element_id:
                process.remove(element)

    return new_root


def insert_element_to_flow(root, flow_id, element_tag, element_id):
    process_root = root.find("xmlns:process", bpmn_element_ns)
    new_element = generate_element(element_tag, element_id)
    target_sequence_flow = find_flow_by_id(process_root, flow_id)

    if target_sequence_flow is not False:
        outgoing_sequence_flow_id = f"Flow_{shortuuid.uuid()}"
        incoming_sequence_flow_id = target_sequence_flow.attrib['id']

        outgoing_target_ref = target_sequence_flow.attrib['targetRef']
        incoming_source_ref = target_sequence_flow.attrib['sourceRef']

        outgoing_sequence_flow = generate_sequence_flow(outgoing_sequence_flow_id, element_id, outgoing_target_ref)
        incoming_sequence_flow = generate_sequence_flow(incoming_sequence_flow_id, incoming_source_ref, element_id)

        new_element = add_incoming_to_element(new_element, [incoming_sequence_flow])
        new_element = add_outgoing_to_element(new_element, [outgoing_sequence_flow])

        root = remove_element_by_id(root, incoming_sequence_flow_id)
        process_root = root.find("xmlns:process", bpmn_element_ns)

        process_root = add_sequence_flow_to_process(process_root, incoming_sequence_flow)
        process_root = add_sequence_flow_to_process(process_root, outgoing_sequence_flow)

        process_root.append(new_element)

        for task in process_root.getchildren():
            if task.attrib['id'] == outgoing_target_ref:
                for incoming in task.findall("xmlns:incoming", bpmn_element_ns):
                    if incoming.text == flow_id:
                        task.remove(incoming)

                add_incoming_to_element(task, [outgoing_sequence_flow])

        return {'new_element': new_element,
                'incoming_sequence_flow': incoming_sequence_flow,
                'outgoing_sequence_flow': outgoing_sequence_flow}
    else:
        print('Flow ID not found')
        return False


def add_new_element_to_flow(file_path, element_type, flow_id, output_file):
    tree = parse_bpmn_from(file_path)
    root = tree.getroot()

    insert_element_to_flow(root, flow_id, element_type, f"{element_type}_{shortuuid.uuid()}")

    write_to_file(tree, output_file)


def skip_element(file_path, element_id, output_file):
    tree = parse_bpmn_from(file_path)
    root = tree.getroot()

    prev_gateway_id = f"gateway_{shortuuid.uuid()}"
    next_gateway_id = f"gateway_{shortuuid.uuid()}"

    add_gateway_before_task(root, element_id, prev_gateway_id)
    add_gateway_after_task(root, element_id, next_gateway_id)

    write_to_file(tree, output_file)

    tree = parse_bpmn_from(output_file)
    root = tree.getroot()

    link_gateways(root, prev_gateway_id, next_gateway_id)

    write_to_file(tree, output_file)


def get_starting_task_id(root):
    starting_event = root.find("xmlns:startEvent", bpmn_element_ns)

    for seqFlow in root.findall("xmlns:sequenceFlow", bpmn_element_ns):
        if seqFlow.attrib['sourceRef'] == starting_event.attrib['id']:
            return seqFlow.attrib['targetRef']


def get_ending_task_id(root):
    end_event = root.find("xmlns:endEvent", bpmn_element_ns)

    for seqFlow in root.findall("xmlns:sequenceFlow", bpmn_element_ns):
        if seqFlow.attrib['targetRef'] == end_event.attrib['id']:
            return seqFlow.attrib['sourceRef']


def remove_starting_event(process_root):
    new_process_root = process_root
    starting_event_id = None
    starting_event_flow_id = None

    starting_event = new_process_root.find("xmlns:startEvent", bpmn_element_ns)
    starting_event_id = starting_event.attrib['id']

    new_process_root.remove(starting_event)

    for seqFlow in new_process_root.findall("xmlns:sequenceFlow", bpmn_element_ns):
        if seqFlow.attrib['sourceRef'] == starting_event_id:
            starting_event_flow_id = seqFlow.attrib['id']
            new_process_root.remove(seqFlow)

    for child in process_root.getchildren():
        for incoming in child.findall("xmlns:incoming", bpmn_element_ns):
            if incoming.text == starting_event_flow_id:
                child.remove(incoming)

        for outgoing in new_process_root.findall("xmlns:outgoing", bpmn_element_ns):
            if outgoing.text == starting_event_flow_id:
                child.remove(outgoing)

    return new_process_root


def remove_ending_event(process_root):
    new_process_root = process_root
    end_event_id = None
    end_event_flow_id = None

    end_event = new_process_root.find("xmlns:endEvent", bpmn_element_ns)
    end_event_id = end_event.attrib['id']

    new_process_root.remove(end_event)

    for seqFlow in new_process_root.findall("xmlns:sequenceFlow", bpmn_element_ns):
        if seqFlow.attrib['targetRef'] == end_event_id:
            end_event_flow_id = seqFlow.attrib['id']
            new_process_root.remove(seqFlow)

    for child in process_root.getchildren():
        for outgoing in child.findall("xmlns:outgoing", bpmn_element_ns):
            if outgoing.text == end_event_flow_id:
                child.remove(outgoing)

        for incoming in child.findall("xmlns:incoming", bpmn_element_ns):
            if incoming.text == end_event_flow_id:
                child.remove(incoming)

    return new_process_root


def merge_process_fragment(source_process_root, target_process_root):
    # REMOVE STARTING AND ENDING EVENTS FROM TARGET PROCESS:
    target_process_root = remove_starting_event(target_process_root)
    target_process_root = remove_ending_event(target_process_root)

    # APPEND REMAINING PROCESS TO SOURCE PROCESS
    for child in target_process_root.getchildren():
        source_process_root.append(child)

    # RETURN THE UPDATED TREE
    return source_process_root


def serial_insert(path_id, source_process_root, starting_id, ending_id):
    flow = None

    # remove existing A -> B flow to A -> Process -> B
    for seqFlow in source_process_root.findall("xmlns:sequenceFlow", bpmn_element_ns):
        if seqFlow.attrib['id'] == path_id:
            flow = seqFlow
            source_process_root.remove(seqFlow)

    flow_source = flow.attrib['sourceRef']
    flow_target = flow.attrib['targetRef']

    flow_id = f"Flow_{shortuuid.uuid()}"

    incoming_seq_flow = generate_sequence_flow(path_id, flow_source, starting_id)
    outgoing_seq_flow = generate_sequence_flow(flow_id, ending_id, flow_target)

    source_process_root.append(incoming_seq_flow)
    source_process_root.append(outgoing_seq_flow)

    # update incoming outgoing tags
    for child in source_process_root.getchildren():
        if child.attrib['id'] == starting_id:
            incoming = generate_incoming_flow(path_id)
            child.append(incoming)

        if child.attrib['id'] == ending_id:
            outgoing = generate_outgoing_flow(flow_id)
            child.append(outgoing)

        if child.attrib['id'] == flow_target:
            for incoming in child.findall('xmlns:incoming', bpmn_element_ns):
                if incoming.text == path_id:
                    child.remove(incoming)

            incoming = generate_incoming_flow(flow_id)
            child.append(incoming)

    return source_process_root


def serial_insert_process(source_file, target_file, path_id, output_file):
    source_tree = parse_bpmn_from(source_file)
    target_tree = parse_bpmn_from(target_file)

    source_root = source_tree.getroot()
    target_root = target_tree.getroot()

    source_process_root = source_root.find("xmlns:process", bpmn_element_ns)
    target_process_root = target_root.find("xmlns:process", bpmn_element_ns)

    if not validate_flow_presence(source_process_root, path_id):
        print('Flow is not in process')
        return

    starting_id = get_starting_task_id(target_process_root)
    ending_id = get_ending_task_id(target_process_root)

    source_process_root = merge_process_fragment(source_process_root, target_process_root)
    source_process_root = serial_insert(path_id, source_process_root, starting_id, ending_id)

    write_to_file(source_tree, output_file)

    return source_process_root


def branch_insert_process(source_file, target_file, start_path, end_path, output_file, conditional=False):
    insertion_element = 'parallelGateway'

    if conditional:
        insertion_element = 'exclusiveGateway'

    source_tree = parse_bpmn_from(source_file)

    source_root = source_tree.getroot()

    source_process_root = source_root.find("xmlns:process", bpmn_element_ns);

    if not validate_flow_presence(source_process_root, start_path):
        print('Starting Flow is not in process')
        return

    if not validate_flow_presence(source_process_root, end_path):
        print('Ending Flow is not in process')
        return

    split_gateway_id = f"gateway_{shortuuid.uuid()}"
    join_gateway_id = f"gateway_{shortuuid.uuid()}"

    new_element_data = insert_element_to_flow(source_root, start_path, insertion_element, split_gateway_id)

    if start_path == end_path:
        outgoing_flow = new_element_data['outgoing_sequence_flow']
        end_path = outgoing_flow.attrib['id']
        write_to_file(source_tree, output_file)
        source_tree = parse_bpmn_from(output_file)
        source_root = source_tree.getroot()

    insert_element_to_flow(source_root, end_path, insertion_element, join_gateway_id)

    source_root = source_tree.getroot()
    alternate_flow = link_gateways(source_root, split_gateway_id, join_gateway_id)

    write_to_file(source_tree, output_file)
    serial_insert_process(output_file, target_file, alternate_flow.attrib['id'], output_file)

    target_tree = parse_bpmn_from(output_file)
    target_root = target_tree.getroot()
    reset_incoming_outgoing_tags(target_root)
    write_to_file(target_tree, output_file)


def skip_process_fragment(source_file, output_file, start_path, end_path):
    insertion_element = 'exclusiveGateway'

    source_tree = parse_bpmn_from(source_file)

    source_root = source_tree.getroot()

    source_process_root = source_root.find("xmlns:process", bpmn_element_ns);

    if not validate_flow_presence(source_process_root, start_path):
        print('Starting Flow is not in process')
        return

    if not validate_flow_presence(source_process_root, end_path):
        print('Ending Flow is not in process')
        return

    split_gateway_id = f"gateway_{shortuuid.uuid()}"
    join_gateway_id = f"gateway_{shortuuid.uuid()}"

    new_element_data = insert_element_to_flow(source_root, start_path, insertion_element, split_gateway_id)

    if start_path == end_path:
        outgoing_flow = new_element_data['outgoing_sequence_flow']
        end_path = outgoing_flow.attrib['id']
        write_to_file(source_tree, output_file)
        source_tree = parse_bpmn_from(output_file)
        source_root = source_tree.getroot()

    insert_element_to_flow(source_root, end_path, insertion_element, join_gateway_id)

    source_root = source_tree.getroot()
    alternate_flow = link_gateways(source_root, split_gateway_id, join_gateway_id)

    write_to_file(source_tree, output_file)


def validate_flow_presence(process_root, flow_id):
    for sequence_flow in process_root.findall("xmlns:sequenceFlow", bpmn_element_ns):
        if sequence_flow.attrib['id'] == flow_id:
            return True

    return False


def validate_flow_presence_in_file(file, flow_id):
    tree = parse_bpmn_from(file)
    root = tree.getroot()

    process_root = root.find("xmlns:process", bpmn_element_ns);

    return validate_flow_presence(process_root, flow_id);