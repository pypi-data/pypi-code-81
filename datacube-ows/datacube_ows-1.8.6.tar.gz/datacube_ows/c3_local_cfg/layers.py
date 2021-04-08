from .bands import *
from .styles import *
from .resource_limits import reslim_c3_ls 

dea_c3_ls8_ard = {
                            "title": "DEA C3 Landsat 8 ARD",
                            "abstract": """
This product takes Landsat 8 imagery captured over the Australian continent and corrects for inconsistencies across land and coastal fringes. The result is accurate and standardised surface reflectance data, which is instrumental in identifying and quantifying environmental change.
The imagery is captured using the Operational Land Imager (OLI) and Thermal Infra-Red Scanner (TIRS) sensors aboard Landsat 8.
This product is a single, cohesive Analysis Ready Data (ARD) package, which allows you to analyse surface reflectance data as is, without the need to apply additional corrections.
It contains three sub-products that provide corrections or attribution information:
Surface Reflectance NBAR 3 (Landsat 8 OLI-TIRS)
Surface Reflectance NBART 3 (Landsat 8 OLI-TIRS)
Surface Reflectance OA 3 (Landsat 8 OLI-TIRS)
The resolution is a 30 m grid based on the USGS Landsat Collection 1 archive.""",
                            # The WMS name for the layer
                            "name": "ga_ls8c_ard_3",
                            # The Datacube name for the associated data product
                            "product_name": "ga_ls8c_ard_3",
                            "bands": bands_c3_ls_8,
                            "resource_limits": reslim_c3_ls,
                            "image_processing": {
                                "extent_mask_func": "datacube_ows.ogc_utils.mask_by_val",
                                "always_fetch_bands": [],
                                "manual_merge": False,
                            },
                            "flags": [
                                {
                                    "band": "oa_nbart_contiguity",
                                    "product": "ga_ls8c_ard_3",
                                    "ignore_time": False,
                                    "ignore_info_flags": [],
                                },
                                {
                                    "band": "oa_fmask",
                                    "product": "ga_ls8c_ard_3",
                                    "ignore_time": False,
                                    "ignore_info_flags": [],
                                },
                            ],
                            "wcs": {
                                "native_crs": "EPSG:3577",
                                "native_resolution": [25, -25],
                                "default_bands": ["nbart_red", "nbart_green", "nbart_blue"],
                            },
                            "styling": {
                                "default_style": "simple_rgb",
                                "styles": styles_c3_ls_8
                            },
                        }
dea_c3_ls7_ard =        {
                            "title": "DEA C3 Landsat 7 ARD",
                            "abstract": """
The United States Geological Survey's (USGS) Landsat satellite program has been capturing images of the Australian continent for more than 30 years. This data is highly useful for land and coastal mapping studies.
In particular, the light reflected from the Earth’s surface (surface reflectance) is important for monitoring environmental resources – such as agricultural production and mining activities – over time.
We need to make accurate comparisons of imagery acquired at different times, seasons and geographic locations. However, inconsistencies can arise due to variations in atmospheric conditions, sun position, sensor view angle, surface slope and surface aspect. These need to be reduced or removed to ensure the data is consistent and can be compared over time.
For service status information, see https://status.dea.ga.gov.au""",
                            # The WMS name for the layer
                            "name": "ga_ls7e_ard_3",
                            # The Datacube name for the associated data product
                            "product_name": "ga_ls7e_ard_3",
                            "bands": bands_c3_ls_7,
                            "resource_limits": reslim_c3_ls,
                            "image_processing": {
                                "extent_mask_func": "datacube_ows.ogc_utils.mask_by_val",
                                "always_fetch_bands": [],
                                "manual_merge": False,
                            },
                            "wcs": {
                                "native_crs": "EPSG:3577",
                                "native_resolution": [25, -25],
                                "default_bands": ["nbart_red", "nbart_green", "nbart_blue"],
                            },
                            "styling": {
                                "default_style": "simple_rgb",
                                "styles": styles_c3_ls_7
                            },
                        }
dea_c3_ls5_ard =        {
                            "title": "DEA C3 Landsat 5 ARD",
                            "abstract": """
The United States Geological Survey's (USGS) Landsat satellite program has been capturing images of the Australian continent for more than 30 years. This data is highly useful for land and coastal mapping studies.
In particular, the light reflected from the Earth’s surface (surface reflectance) is important for monitoring environmental resources – such as agricultural production and mining activities – over time.
We need to make accurate comparisons of imagery acquired at different times, seasons and geographic locations. However, inconsistencies can arise due to variations in atmospheric conditions, sun position, sensor view angle, surface slope and surface aspect. These need to be reduced or removed to ensure the data is consistent and can be compared over time.
For service status information, see https://status.dea.ga.gov.au""",
                            # The WMS name for the layer
                            "name": "ga_ls5t_ard_3",
                            # The Datacube name for the associated data product
                            "product_name": "ga_ls5t_ard_3",
                            "bands": bands_c3_ls_common,
                            "resource_limits": reslim_c3_ls,
                            "image_processing": {
                                "extent_mask_func": "datacube_ows.ogc_utils.mask_by_val",
                                "always_fetch_bands": [],
                                "manual_merge": False,
                            },
                            "wcs": {
                                "native_crs": "EPSG:3577",
                                "native_resolution": [25, -25],
                                "default_bands": ["nbart_red", "nbart_green", "nbart_blue"],
                            },
                            "styling": {
                                "default_style": "simple_rgb",
                                "styles": styles_c3_ls_common
                            },
                        }
