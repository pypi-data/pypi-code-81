"""
Functions helping to build filtering functions to use
in graph search
"""
class NodesFiltering:
    def all_nodes():
        """
        Return a function that filter nothing
        """
        return lambda e: True

    def positive_filter_nodes(positive):
        """
        Return a function filtering nodes not belonging to positive
        """
        return lambda e: e in positive

    def negative_filter_nodes(negative):
        """
        Return a function filtering nodes belonging to negative
        """
        return lambda e: not(e in negative)

    def filter_nodes_and(get_node_data, document):
        """
        Return function filtering nodes whose data values match the document with
        "and" semantic:
        document: {"type": ["actor","author"], "age":12} match all nodes whose type
        is either actor or author AND of age 12.
        """
        for key,value in document.items():
            if type(value) != list:
                document[key] = [value]
        _fltr = lambda e: all(map(lambda e: get_node_data(e,key) in documents[key],document))
        return _fltr
