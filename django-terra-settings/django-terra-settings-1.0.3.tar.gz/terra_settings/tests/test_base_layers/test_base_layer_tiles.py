from django.core.management import call_command
from django.urls import reverse
from mapbox_baselayer.models import MapBaseLayer
from rest_framework import status
from rest_framework.test import APITestCase


class MapboxBaseLayerViewsSetTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        call_command('install_osm_baselayer')

    def test_create(self):
        data = {
            "name": "test",
            "base_layer_type": "mapbox",
            "map_box_url": "mapbox://test/",
            "order": 0,
            "min_zoom": 0,
            "max_zoom": 20,
            "tile_size": 256
        }
        response = self.client.post(reverse('baselayer-list'), data=data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, data)

        self.assertTrue(data['id'])
        self.assertEqual(data['tiles'], [])

    def test_full_update(self):
        data = {
            "name": "test2",
            "base_layer_type": "mapbox",
            "map_box_url": "mapbox://test/",
            "order": 0,
            "min_zoom": 0,
            "max_zoom": 20,
            "tile_size": 256
        }
        pk = MapBaseLayer.objects.first().pk
        response = self.client.patch(reverse('baselayer-detail', args=(pk, )), data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data['name'], "test2")
