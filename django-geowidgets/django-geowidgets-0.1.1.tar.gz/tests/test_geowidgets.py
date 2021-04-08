from unittest import TestCase

from django.contrib.gis.geos import Point

from geowidgets import LatLonField, LatLonWidget


class LatLonWidgetTestCase(TestCase):
    def test_decompress_value(self):
        result = LatLonWidget().decompress(Point(12.34567891234567, -23.456789123456))
        self.assertAlmostEqual(result[0], 12.345679, places=13)
        self.assertAlmostEqual(result[1], -23.456789, places=13)

    def test_decompress_none(self):
        result = LatLonWidget().decompress(None)
        self.assertIsNone(result[0])
        self.assertIsNone(result[1])


class LatLonFieldTestCase(TestCase):
    def test_compress(self):
        self.assertEqual(
            LatLonField().compress([12.345678, -23.456789]),
            "SRID=4326;POINT(12.345678 -23.456789)",
        )
