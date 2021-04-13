# -*- coding: utf-8 -*-

from pip_services3_commons.convert import StringConverter
from pip_services3_components.count import CounterType


class PrometheusCounterConverter:
    """
    Helper class that converts performance counter values into
    a response from Prometheus metrics service.
    """

    @staticmethod
    def to_string(counters, source, instance):
        """
        Converts the given counters to a string that is returned by Prometheus metrics service.

        :param counters: a list of counters to convert.
        :param source: a source (context) name.
        :param instance: a unique instance name (usually a host name).
        """
        if counters is None or len(counters) == 0: return ''

        builder = ''

        for counter in counters:
            counter_name = PrometheusCounterConverter.__parse_counter_name(counter)
            labels = PrometheusCounterConverter.__generate_counter_label(counter, source, instance)

            if counter.type == CounterType.Increment:
                builder += "# TYPE " + counter_name + " gauge\n"
                builder += counter_name + labels + ' ' + StringConverter.to_string(counter.count) + "\n"
            elif counter.type == CounterType.Interval:
                builder += "# TYPE " + counter_name + "_max gauge\n"
                builder += counter_name + "_max" + labels + " " + StringConverter.to_string(counter.max) + "\n"
                builder += "# TYPE " + counter_name + "_min gauge\n"
                builder += counter_name + "_min" + labels + " " + StringConverter.to_string(counter.min) + "\n"
                builder += "# TYPE " + counter_name + "_average gauge\n"
                builder += counter_name + "_average" + labels + " " + StringConverter.to_string(counter.average) + "\n"
                builder += "# TYPE " + counter_name + "_count gauge\n"
                builder += counter_name + "_count" + labels + " " + StringConverter.to_string(counter.count) + "\n"
            elif counter.type == CounterType.LastValue:
                builder += "# TYPE " + counter_name + " gauge\n"
                builder += counter_name + labels + " " + StringConverter.to_string(counter.last) + "\n"
            elif counter.type == CounterType.Statistics:
                builder += "# TYPE " + counter_name + "_max gauge\n"
                builder += counter_name + "_max" + labels + " " + StringConverter.to_string(counter.max) + "\n"
                builder += "# TYPE " + counter_name + "_min gauge\n"
                builder += counter_name + "_min" + labels + " " + StringConverter.to_string(counter.min) + "\n"
                builder += "# TYPE " + counter_name + "_average gauge\n"
                builder += counter_name + "_average" + labels + " " + StringConverter.to_string(counter.average) + "\n"
                builder += "# TYPE " + counter_name + "_count gauge\n"
                builder += counter_name + "_count" + labels + " " + StringConverter.to_string(counter.count) + "\n"

        return builder

    @staticmethod
    def __generate_counter_label(counter, source, instance):
        labels = {}

        if source and source != '': labels['source'] = source
        if instance and instance != '': labels['instance'] = instance

        name_parts = counter.name.split('.')

        # If there are other predictable names from which we can parse labels, we can add them below
        if (len(name_parts) >= 3 and name_parts[2] == 'exec_count') or (
                len(name_parts) >= 3 and name_parts[2] == 'exec_time') or (
                len(name_parts) >= 3 and name_parts[2] == 'exec_errors'):
            labels["service"] = name_parts[0]
            labels["command"] = name_parts[1]

        if (len(name_parts) >= 4 and name_parts[3] == 'call_count') or (
                len(name_parts) >= 4 and name_parts[3] == 'call_time') or (
                len(name_parts) >= 4 and name_parts[3] == 'call_errors'):
            labels["service"] = name_parts[1]
            labels["command"] = name_parts[2]
            labels["target"] = name_parts[0]

        if (len(name_parts) >= 3 and name_parts[2] == 'sent_messages') or (
                len(name_parts) >= 3 and name_parts[2] == 'received_messages') or (
                len(name_parts) >= 3 and name_parts[2] == 'dead_messages'):
            labels["queue"] = name_parts[1]

        if len(labels) < 1:
            return ''

        builder = '{'
        for key in labels:
            if len(builder) > 1: builder += ','
            builder += key + '="' + labels[key] + '"'
        builder += '}'

        return builder

    @staticmethod
    def __parse_counter_name(counter):
        if counter is None and (counter.name is None or counter.name == ''): return ''

        name_parts = counter.name.split('.')

        # If there are other predictable names from which we can parse labels, we can add them below
        # Rest Service Labels
        if len(name_parts) >= 3 and name_parts[2] == 'exec_count': return name_parts[2]
        if len(name_parts) >= 3 and name_parts[2] == 'exec_time': return name_parts[2]
        if len(name_parts) >= 3 and name_parts[2] == 'exec_errors': return name_parts[2]

        # Rest & Direct Client Labels
        if len(name_parts) >= 4 and name_parts[3] == 'call_count': return name_parts[3]
        if len(name_parts) >= 4 and name_parts[3] == 'call_time': return name_parts[3]
        if len(name_parts) >= 4 and name_parts[3] == 'call_errors': return name_parts[3]

        # Queue Labels
        if (len(name_parts) >= 3 and name_parts[2] == 'sent_messages') or (
                len(name_parts) >= 3 and name_parts[2] == 'received_messages') or (
                len(name_parts) >= 3 and name_parts[2] == 'dead_messages'):
            name = f'{name_parts[0]}.{name_parts[2]}'
            return name.lower().replace(".", "_").replace("/", "_")

        # TODO: are there other assumptions we can make?
        # Or just return as a single, valid name
        return counter.name.lower().replace(".", "_").replace("/", "_")

    @staticmethod
    def __parse_counter_labels(counter, source, instance):
        labels = {}

        if source and source != '': labels['source'] = source
        if instance and instance != '': labels['instance'] = instance

        name_parts = counter.name.split('.')

        # If there are other predictable names from which we can parse labels, we can add them below
        if len(name_parts) >= 3 and name_parts[2] == 'exec_time':
            labels["service"] = name_parts[0]
            labels["command"] = name_parts[1]

        return labels
