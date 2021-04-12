import simplesum


def summation(elements: list):
    return simplesum.ssum(elements)


def productory(elements: list):
    p = 1
    for k in elements:
        p *= k
    return p


def source_version():
    return "Source: PyPI package index"

