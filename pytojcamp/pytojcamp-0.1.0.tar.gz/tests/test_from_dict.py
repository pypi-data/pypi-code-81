# -*- coding: utf-8 -*-
"""Test the ntuple conversion"""
from pytojcamp.from_dict import from_dict


def test_from_dict(make_data_dictionary):
    """Test the conversion based on a data dict"""
    jcamp_string = from_dict(make_data_dictionary)

    expected_string = """##TITLE=
##JCAMP-DX=6.00
##DATA TYPE=
##ORIGIN=
##OWNER=
##VAR_NAME=  x,y,z
##SYMBOL=    x,y,z
##VAR_TYPE=  INDEPENDENT,DEPENDENT,DEPENDENT
##VAR_DIM=   3,3,3
##UNITS=     cm,h,kg
##DATA TABLE= (xyz..xyz), PEAKS
1\t3\t3
2\t2\t2
3\t3\t3
##END"""
    print(jcamp_string)
    print(expected_string)
    assert jcamp_string == expected_string
