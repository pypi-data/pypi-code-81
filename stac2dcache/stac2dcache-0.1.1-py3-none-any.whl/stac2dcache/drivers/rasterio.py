import rasterio
import rioxarray
import tempfile

from .base import Driver


class RasterioDriver(Driver):
    """ Driver to read raster data """
    def get(self, load=True, gdal_config_options=None, **kwargs):
        """
        Load the raster data in a rasterio-xarray DataArray object

        :param load: (bool, optional) if True, load data
        :param gdal_config_options: (dict, optional) GDAL configuration options
            (see https://trac.osgeo.org/gdal/wiki/ConfigOptions)
        :param kwargs: (optional) arguments to be passed to open_rasterio
        :return :class:`~rioxarray.core.dataarray.DataArray`
        """
        gdal_config_options = gdal_config_options or {}

        client_kwargs = getattr(self.filesystem, "client_kwargs", None)
        auth = None if not client_kwargs else client_kwargs.get("auth")
        if auth is not None:
            gdal_config_options['GDAL_HTTP_AUTH'] = 'BASIC'
            gdal_config_options['GDAL_HTTP_USERPWD'] = '{}:{}'.format(
                auth.login,
                auth.password
            )

        f = None
        headers = None if not client_kwargs else client_kwargs.get("headers")
        if headers is not None:
            headers_text = '\n'.join([f'{key}: {value}'
                                      for key, value in headers.items()])
            f = tempfile.NamedTemporaryFile(mode='w', delete=load)
            f.write(headers_text)
            f.seek(0)
            gdal_config_options['GDAL_HTTP_HEADER_FILE'] = f.name

        with rasterio.Env(**gdal_config_options):
            data_array = rioxarray.open_rasterio(self.uri, **kwargs)
            if load:
                data_array.load()

        if f is not None:
            f.close()  # this cleans up if needed
            if not f.delete:
                print(f"GDAL headers saved to: {f.name}")
        return data_array
