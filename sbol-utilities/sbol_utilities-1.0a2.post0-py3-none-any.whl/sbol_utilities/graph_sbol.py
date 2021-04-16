import sbol3
import graphviz
import rdflib
import argparse


def graph_sbol(doc, outfile='out'):
    g = doc.graph()
    dot_master = graphviz.Digraph()
    #dot_master.graph_attr['ratio'] = '%f' %(4./3.)

    dot = graphviz.Digraph(name='cluster_toplevels')
    for obj in doc.objects:
        dot.graph_attr['style'] = 'invis'

        # Graph TopLevel
        obj_label = _get_node_label(obj)
        dot.node('Document', **node_format)
        dot.node(_strip_scheme(obj), **node_format)
        dot.edge('Document', _strip_scheme(obj), **composition_format)
    dot_master.subgraph(dot)

    for obj in doc.objects:
        dot = graphviz.Digraph(name='cluster_%s' %_strip_scheme(obj))
        dot.graph_attr['style'] = 'invis'

        # Graph owned objects
        t = _visit_children(obj, [])
        for start_node, edge, end_node in t:
            start_label = _get_node_label(start_node)
            end_label = _get_node_label(end_node)
            dot.node(_strip_scheme(start_node), label=start_label, **node_format)
            dot.node(_strip_scheme(end_node), label=end_label, **node_format)
            dot.edge(_strip_scheme(start_node), _strip_scheme(end_node), label=edge, **composition_format)
        dot_master.subgraph(dot)

    for obj in doc.objects:
        # Graph associations
        t = _visit_associations(obj, [])
        for triple in t:
            start_node, edge, end_node = triple
            start_label = _get_node_label(start_node)
            end_label = _get_node_label(end_node)
            dot_master.node(_strip_scheme(start_node), label=start_label, **node_format)
            dot_master.node(_strip_scheme(end_node), label=end_label, **node_format)
            # See https://stackoverflow.com/questions/2499032/subgraph-cluster-ranking-in-dot
            # constraint=false commonly gives unnecessarily convoluted edges.
            # It seems that weight=0 gives better results:
            dot_master.edge(_strip_scheme(start_node), _strip_scheme(end_node), label=edge, weight='0', **association_format)
        
    #print(dot_master.source)
    source = graphviz.Source(dot_master.source.replace('\\\\', '\\'))
    source.render(outfile, view=True)
 

def _get_node_label(obj):
    if obj.name:
        node_label = obj.name
    elif obj.display_id:
        node_label = obj.display_id
    else:
        node_label = obj.identity.split('//')[-1]

    properties_label = ''
    for attr_name, sbol_property in obj.__dict__.items():
        datatype = ''
        if not isinstance(sbol_property, sbol3.property_base.Property):
            continue
        if isinstance(sbol_property, sbol3.ownedobject.OwnedObjectPropertyMixin):
            continue
        if isinstance(sbol_property, sbol3.refobj_property.ReferencedObjectMixin):
            continue
        if isinstance(sbol_property, sbol3.property_base.ListProperty):
            val = str(sbol_property)
        else:
            val = sbol_property.get()
        properties_label += f'{attr_name}: {val}\\l'

    label = f'{node_label}|{properties_label}'
    label = '{' + label + '}'

    return label


def _strip_scheme(obj):
    return obj.identity.split('//')[-1]


def _visit_children(obj, triples=[]):
    for property_name, sbol_property in obj.__dict__.items():
        if isinstance(sbol_property, sbol3.ownedobject.OwnedObjectSingletonProperty):
            child = sbol_property.get()
            if child is not None:
                _visit_children(child, triples)
                triples.append((obj, 
                                property_name,
                                child))
        elif isinstance(sbol_property, sbol3.ownedobject.OwnedObjectListProperty):
            for child in sbol_property:
                _visit_children(child, triples)
                triples.append((obj, 
                                property_name, 
                                child))
    return triples


def _visit_associations(obj, triples=[]):
    for property_name, sbol_property in obj.__dict__.items():
        if isinstance(sbol_property, sbol3.refobj_property.ReferencedObjectSingleton):
            referenced_object = sbol_property.get().lookup()
            if referenced_object is not None:
                triples.append((obj, 
                                property_name, 
                                referenced_object))
        elif isinstance(sbol_property, sbol3.refobj_property.ReferencedObjectList):
            for reference in sbol_property:
                referenced_object = reference.lookup()
                triples.append((obj, 
                                property_name, 
                                referenced_object))
        elif isinstance(sbol_property, sbol3.ownedobject.OwnedObjectSingletonProperty):
            child = sbol_property.get()
            if child is not None:
                _visit_associations(child, triples)
        elif isinstance(sbol_property, sbol3.ownedobject.OwnedObjectListProperty):
            for child in sbol_property:
                _visit_associations(child, triples)
    return triples


association_format = {
        'arrowtail' : 'odiamond',
        'arrowhead' : 'vee',
        'fontname' : 'Bitstream Vera Sans',
        'fontsize' : '8',
        'dir' : 'both'
    } 


composition_format = {
        'arrowtail' : 'diamond',
        'arrowhead' : 'vee',
        'fontname' : 'Bitstream Vera Sans',
        'fontsize' : '8',
        'dir' : 'both'
    } 


node_format = {
    'fontname' : 'Bitstream Vera Sans',
    'fontsize' : '8',
    'shape': 'record'
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i",
        "--input",
        dest="in_file",
        help="Input PAML file",
    )
    args_dict = vars(parser.parse_args())

    doc = sbol3.Document()
    doc.read(args_dict['in_file'])
    graph_sbol(doc, args_dict['in_file'].split('.')[0])
