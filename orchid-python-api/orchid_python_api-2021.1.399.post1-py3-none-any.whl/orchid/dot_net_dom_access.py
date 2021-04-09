#  Copyright 2017-2021 Reveal Energy Services, Inc 
#
#  Licensed under the Apache License, Version 2.0 (the "License"); 
#  you may not use this file except in compliance with the License. 
#  You may obtain a copy of the License at 
#
#      http://www.apache.org/licenses/LICENSE-2.0 
#
#  Unless required by applicable law or agreed to in writing, software 
#  distributed under the License is distributed on an "AS IS" BASIS, 
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. 
#  See the License for the specific language governing permissions and 
#  limitations under the License. 
#
# This file is part of Orchid and related technologies.
#

import uuid
from typing import Callable, Union

import deal
import toolz.curried as toolz

from orchid import (
    unit_system as units,
)

# noinspection PyUnresolvedReferences
from System import Guid

# These methods in this module are based on the StackOverflow post:
# https://stackoverflow.com/questions/36580931/python-property-factory-or-descriptor-class-for-wrapping-an-external-library
#
# Additionally, it resolves an issue I was experiencing with PyCharm: when I used `property` directly
# in the class definition, PyCharm reported "Property 'xyz' could not be read. I think it might have been
# than I needed to apply `curry` to the "getter method" I also defined in the class in order to pass he
# attribute name at definition time (because `self` was only available at run-time).


def constantly(x):
    """
    Creates a function that always returns the value, `x`.
    Args:
        x: The value to return

    Returns:
        Returns a function takes any arguments yet always returns `x`.
    """

    # noinspection PyUnusedLocal
    def make_constantly(*args, **kwargs):
        return toolz.identity(x)

    return make_constantly


def get_dot_net_property_value(attribute_name, dom_object):
    """
    Return the value of the DOM property whose name corresponds to `attribute_name`.
    :param attribute_name: The Python `attribute_name`.
    :param dom_object: The DOM object whose property is sought.
    :return: The value of the DOM property.
    """
    @toolz.curry
    def python_name_to_words(python_name):
        return python_name.split('_')

    def capitalize_words(words):
        return toolz.map(str.capitalize, words)

    def words_to_dot_net_property_name(words):
        return ''.join(words)

    @toolz.curry
    def get_value_from_dom(dom, property_name):
        return getattr(dom, property_name)

    # The function, `thread_last`, from `toolz.curried`, "splices" threads a value (the first argument)
    # through each of the remaining functions as the *last* argument to each of these functions.
    result = toolz.thread_last(attribute_name,
                               python_name_to_words,
                               capitalize_words,
                               words_to_dot_net_property_name,
                               get_value_from_dom(dom_object))
    return result


def dom_property(attribute_name, docstring):
    """
    Return the property of the DOM corresponding to `attribute_name` with doc string.
    :param attribute_name: The name of the Python attribute.
    :param docstring: The doc string to be attached to the resulting property.
    :return: The Python property wrapping the value of the DOM property.
    """
    def getter(self):
        result = get_dot_net_property_value(attribute_name, self._adaptee)
        return result

    # Ensure no setter for the DOM properties
    return property(fget=getter, doc=docstring, fset=None)


def transformed_dom_property(attribute_name, docstring, transformer):
    """
    Return the transformed property of the DOM corresponding to `attribute_name`.
    :param attribute_name: The name of the Python attribute.
    :param docstring: The doc string to be attached to the resulting property.
    :param transformer: A callable to transform the value returned by the .NET DOM property.
    :return: The Python property wrapping the transformed value of the DOM property.
    """
    def getter(self):
        raw_result = get_dot_net_property_value(attribute_name, self._adaptee)
        result = transformer(raw_result)
        return result

    # Ensure no setter for the DOM properties
    return property(fget=getter, doc=docstring, fset=None)


def transformed_dom_property_iterator(attribute_name, docstring, transformer):
    """
    Return transformed collection property of the DOM corresponding to `attribute_name` with doc string, `docstring`.
    :param attribute_name: The name of the original attribute.
    :param docstring: The doc string to be attached to the resultant property.
    :param transformer: A callable invoked on each value in the list returned by the .NET DOM property.
    :return: The Python property wrapping a Python iterator mapping values from the DOM property (collection) items.
    """
    def getter(self):
        container = get_dot_net_property_value(attribute_name, self._adaptee)
        result = toolz.map(transformer, container.Items)
        return result

    # Ensure no setter for the DOM properties
    return property(fget=getter, doc=docstring, fset=None)


def as_uuid(guid: Guid):
    return uuid.UUID(str(guid))


class DotNetAdapter:
    @deal.pre(lambda _self, adaptee, _net_project_callable=None: adaptee is not None)
    def __init__(self, adaptee, net_project_callable: Callable = None):
        """
        Construct an instance adapting `adaptee` with access to the .NET `IProject` provided by `net_project_callable`.
        Args:
            adaptee: The .NET DOM object to adapt.
            net_project_callable: A callable returning the .NET `IProject` instance.
        """
        self._adaptee = adaptee
        self._net_project_callable = net_project_callable

    object_id = transformed_dom_property('object_id', 'The object ID of the adapted .NET DOM object.', as_uuid)

    @property
    def dom_object(self):
        """
        (PROTECTED) Determine the DOM object being adapted.

        This method is only intended to be used **INSIDE** the orchid package. It is **NOT** intended for
        external use.

        Returns:
            The .NET DOM object being adapted.
        """
        return self._adaptee

    @property
    def maybe_project_units(self) -> Union[units.UsOilfield, units.Metric]:
        """
        (PROTECTED) Return the `UnitSystem` appropriate the .NET `IProject` of this instance.

        Although by naming convention, this property is "public," the author intends it to be "protected";
        that is, only called by classes derived from `DotNetAdapter` (and not necessarily all of those).

        Returns:
            The unit system, `units.UsOilfield` or `units.Metric`, for this instance. For some derived
            classes, such as `BaseCurveAdapter`, the `IProject` cannot be determined. In those cases, I
            return `None`.
        """
        return (units.as_unit_system(self._net_project_callable().ProjectUnits)
                if self._net_project_callable
                else None)
