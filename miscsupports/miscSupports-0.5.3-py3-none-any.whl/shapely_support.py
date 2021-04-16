import numpy as np


def meters_to_km_miles(area):
    """
    Meters are recorded as Cartesian Square Miles within shapely and this method will return both the square km and
    square Miles as a list

    :param area: Cartesian Square Miles area
    :return: list of [km_sq, Miles_sq]
    :rtype: list[float, float]
    """
    kmsq = area / 1000000
    return [kmsq, kmsq / 2.59]


def shapely_points_to_array(points_list):
    """Convert Shapely cords to a ContourObject readable numpy array"""
    return np.array([[cord] for cord in points_list])


def multi_to_poly(polygon_to_be_typed):
    """
    Recasts all geometry to be Shapely Polygons

    Some methods, like shapely split, do not work well on MultiPolygons and can lead to errors. This method recasts all
    polygons to be a list of polygons.

    :param polygon_to_be_typed: A polygonal structure, be a MultiPolygon or Polygon
    :type polygon_to_be_typed: Polygon | MultiPolygon

    :return: A list of polygons
    :rtype: list[Polygon]
    """
    if polygon_to_be_typed.geom_type == "MultiPolygon":
        return [poly for poly in polygon_to_be_typed]
    else:
        return [polygon_to_be_typed]