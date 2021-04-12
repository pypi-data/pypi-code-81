"""
Find native and alien observations of marine species.

It finds species data from OBIS and connect to distribution of the species
using WoRMS, GISD and NatCon data sources. It uses geo-spatial regions
based on MEOW ECOS merged with MRGID (used by WoRMS source) from different
shape-files.

More about data processing can be found at README.md
"""


import logging
import warnings
from functools import lru_cache
from typing import List, Union

import matplotlib.pyplot as plt
import pandas as pd
import shapely.geometry as sh_geo
from matplotlib.patches import Polygon

import geopandas as gpd
import numpy as np
from marinvaders.api_calls import request_obis
from marinvaders.observation import observations
from marinvaders.readers import ShapeFiles, read_shapefile, read_taxonomy

# ignoring UserWarnings when using str.contains in Species.gisd() method
warnings.filterwarnings("ignore", "This pattern has match groups")
warnings.filterwarnings("ignore", "Geometry column does not contain geometry")

log_filename = "marinvaders.log"
handlers = [logging.FileHandler(log_filename)]

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)-8s " "[%(filename)s:%(lineno)d]  %(message)s",
    handlers=handlers,
)


@lru_cache(None)
def marine_ecoregions(**kwargs) -> gpd.GeoDataFrame:
    """
    Filter meow eco-regions using keywords arguments selectors.

    Note
    ----
    The values of selectors are processed as regexp.

    Parameters
    ----------
    kwargs:
        Selectors to filter using regexp.
        The selectors as a kwargs keys are:

            - ECO_CODE int or list if ints
            - ECOREGION
            - PROVINCE
            - REALM

    Returns
    -------
    geoPandas
        Information on all selected eco-regions

    """

    meow_gpd = read_shapefile(ShapeFiles.MEOW_ECOS)

    for param in kwargs.items():
        # remove null
        colname = param[0].upper()
        if colname == "ECO_CODE":
            eco_codes = param[1]
            if isinstance(eco_codes, int):
                eco_codes = (eco_codes,)
            meow_gpd = meow_gpd[meow_gpd[colname].isin(eco_codes)]
        else:
            meow_gpd = meow_gpd[meow_gpd[colname].notnull()]
            meow_gpd = meow_gpd[meow_gpd[colname].str.contains(
                param[1], regex=True)]
        meow_gpd = meow_gpd.reset_index(drop=True)

    return meow_gpd[
        ["ECO_CODE", "ECO_CODE_X", "ECOREGION", "PROVINCE", "REALM", "geometry"]
    ]


@lru_cache(None)
def get_obis(eco_code: int = None, aphia_id: int = None) -> pd.DataFrame:
    """
    Get OBIS species either for the selected eco-code from MEOW  or Aphia ID.
    Using both is currently not implemented.

    Parameters
    ----------
    eco_code: int
        Eco code of MEOW eco-region
    aphia_id: int
        Aphia ID of species

    Returns
    -------
    pandas.DataFrame
        Species information from the obis database

    Raises
    ------
    NotImplementedError
        When both arguments eco_code and aphia_id are used
    ValueError
        when both arguments are none

    """
    if eco_code and aphia_id:
        raise NotImplementedError(
            "Currently either geometry or aphiaID can " "be specified. Not both"
        )

    if eco_code:
        df_obis = request_obis(eco_code=eco_code)
    elif aphia_id:
        df_obis = request_obis(aphia_id=aphia_id)
    else:
        raise ValueError("Either eco_code or aphiaID must be specified")

    df_obis["ECO_CODE"] = eco_code

    return df_obis


@lru_cache(None)
class Species:
    """
    Class representing a single species.

    Attributes
    ----------
    aphia_id: int
        Aphia ID of species (using WoRMS classification).
    obis: pandas.DataFrame
        Result from OBIS API request for this species
    observations: pandas.DataFrame
        Observations of this species based on WoRMS, GISD and NatCon sources

    """

    def __init__(self, aphia_id: Union[int, str]):
        """
        Class init method

        Parameters
        ----------
        aphia_id: int or str
            Species AphiaID (from WoRMS or OBIS).
            This can either be the AphiaID integer or the whole URI string
            ('urn:lsid:marinespecies.org:taxname:XXXXXX'), in which case the
            integer XXXXXX will be extracted and used

        Raises
        ------
        RuntimeError
            When no record found in OBIS for the aphia ID of species
        """

        if type(aphia_id) == str:
            aphia_id = int(aphia_id.split(":")[-1])
        self.aphia_id: int = aphia_id
        self.obis: pd.DataFrame = get_obis(aphia_id=aphia_id)
        if self.obis.empty:
            raise RuntimeError(
                "No record found in OBIS for species with "
                "aphia ID: {}".format(aphia_id)
            )
        self.observations: pd.DataFrame = observations(self.obis.iloc[0:1],
                                                       species=True)

    @property
    def reported_as_alien(self) -> pd.DataFrame:
        """
        Get marine eco regions where the species is alien.

        The eco-region information is based on OBIS lat/log linked to
        eco-regions and only these obeservations are reported.
        (technically the intersection of obis observation and all alien
        observations for the species).

        Returns
        -------
        pd.DataFrame
            Table of aliens observations
        """
        if self.observations.empty:
            return pd.DataFrame()

        aliens = self.observations[
            self.observations["establishmentMeans"] == "Alien"
        ].reset_index(drop=True)
        aliens["ECO_CODE"] = aliens["ECO_CODE"].astype("int64")

        df_intersection = pd.merge(
            aliens, self.all_occurrences, on="ECO_CODE", how="inner"
        )
        df_intersection.drop(
            [
                "ECOREGION_y",
                "aphiaID_y",
                "geometry_y",
                "decimalLatitude_y",
                "decimalLongitude_y",
                "species_y",
            ],
            axis=1,
            inplace=True,
        )
        df_intersection.rename(
            index=str,
            columns={
                "ECOREGION_x": "ECOREGION",
                "aphiaID_x": "aphiaID",
                "decimalLatitude_x": "decimalLatitude",
                "decimalLongitude_x": "decimalLongitude",
                "geometry_x": "geometry",
                "species_x": "species",
                "MRGID_x": "MRGID",
                "dataset_x": "dataset",
                "establishmentMeans_x": "establishmentMeans",
            },
            inplace=True,
        )
        # Report as alien as soon as it is reported as alien in one of the
        # datasources. Column dataset reports all datasources which report a
        # species as alien.
        df_intersection = df_intersection.groupby(
            ["aphiaID", "ECO_CODE", "ECOREGION", "species", "MRGID"],
            as_index=False)["dataset"].agg(
            {"dataset": lambda x: ",".join(x)}
        )
        df_intersection = pd.merge(
            df_intersection,
            aliens[['geometry', 'ECO_CODE']],
            on="ECO_CODE", how="left")
        df_intersection.drop_duplicates(["ECO_CODE"], inplace=True)

        return df_intersection

    @property
    def all_occurrences(self) -> pd.DataFrame:
        """
        Reports all occurrences of a given species

        Data is based on the OBIS database with linking of latitude/longitude values to ecoregions.

        Returns
        -------
        pd.DataFrame
            table of observations
        """

        df = self.observations.copy()

        ecoregions = marine_ecoregions()

        # df["geometry"] = None
        # df["ECO_CODE"] = None

        def map_point_to_polygon(polygon, ecocode, ecoregion, lon, lat):
            """Check if a given point (lon, lat) within polygon"""
            p = sh_geo.Point(lon, lat)
            if p.within(polygon):
                return polygon, ecocode, ecoregion
            return None, None, None

        # Check for each ecoregion if a given observation is within that
        # ecoregion
        for _, row in ecoregions.iterrows():
            ra, rb, rc = zip(
                *df.apply(
                    lambda x: map_point_to_polygon(
                        row["geometry"],
                        row["ECO_CODE"],
                        row["ECOREGION"],
                        x["decimalLongitude"],
                        x["decimalLatitude"],
                    )
                    if not x["geometry"]
                    else (x["geometry"], x["ECO_CODE"], x["ECOREGION"]),
                    axis=1,
                )
            )
            # need to assign to object type to avoid deprecation warning
            df["geometry"], df["ECO_CODE"], df["ECOREGION"] = (
                np.array(ra, dtype=object),
                np.array(rb, dtype=object),
                np.array(rc, dtype=object),
            )
        df = df[df["ECO_CODE"].notna()]
        df.drop_duplicates("ECO_CODE", inplace=True)
        df["ECO_CODE"] = df["ECO_CODE"].astype("int64")

        return df

    def plot(self):
        """
        Plot species object.

        Returns
        -------
        matplotlib plot object
        """
        world = gpd.read_file(gpd.datasets.get_path("naturalearth_lowres"))
        fig, _ = plt.subplots(1, 1, sharey=True, figsize=(20, 30))
        fig.suptitle(
            "Observations of {}".format(self.obis.species.iloc[0]), fontsize=24
        )

        ax1 = plt.subplot(3, 1, 1)
        ax1.set_aspect("equal")
        world.plot(ax=ax1, color="white", edgecolor="black")
        polys = []
        for item in self.all_occurrences.iterrows():
            try:
                if type(item[1]["geometry"]) == sh_geo.MultiPolygon:
                    polys.extend(
                        list(sh_geo.MultiPolygon(item[1]["geometry"])))
                else:
                    polys.append(sh_geo.Polygon(item[1]["geometry"]))
            except Exception as e:
                logging.error(e)
        for poly in polys:
            coords = poly
            x, y = coords.exterior.coords.xy
            x = x.tolist()
            y = y.tolist()
            xym = list(zip(x, y))
            m_poly = Polygon(
                xym, facecolor="green", edgecolor="green", linewidth=1, alpha=0.3
            )
            plt.gca().add_patch(m_poly)
        ax1.set_title(
            "Distribution of {} (from OBIS database)".format(
                self.obis.species.iloc[0])
        )

        ax2 = plt.subplot(3, 1, 2)
        ax2.set_aspect("equal")
        world.plot(ax=ax2, color="white", edgecolor="black")
        polys = []
        for item in self.reported_as_alien.iterrows():
            try:
                if type(item[1]["geometry"]) == sh_geo.MultiPolygon:
                    polys.extend(
                        list(sh_geo.MultiPolygon(item[1]["geometry"])))
                else:
                    polys.append(sh_geo.Polygon(item[1]["geometry"]))
            except Exception as e:
                logging.error(e)
        for poly in polys:
            coords = poly
            x, y = coords.exterior.coords.xy
            x = x.tolist()
            y = y.tolist()
            xym = list(zip(x, y))
            m_poly = Polygon(
                xym, facecolor="red", edgecolor="red", linewidth=1, alpha=0.7
            )
            plt.gca().add_patch(m_poly)
        ax2.set_title("Alien distribution of {}".format(
            self.obis.species.iloc[0]))

        plt.show()


@lru_cache(None)
class MarineLife(object):
    """
    Class representing Marine Life in selected MEOW Eco region.

    It finds which species are aliens, affected by aliens and find all
    observations of the alien species in other eco regions based on
    OBIS source.

    Attributes
    ----------
    eco_code: int
        MEOW eco code of the selected region
    obis: pandas.DataFrame
        all species for the selected region based on OBIS
    observations: pandas.DataFrame
        Observations of all species in this eco region based on WoRMS,
        GISD and NatCon sources

    """

    def __init__(self, eco_code: int):
        """
        Class init method.

        Parameters
        ----------
        eco_code: int
            Eco code of MEOW eco region.
        """
        self.eco_code: int = eco_code
        # All species from obis which are present in the selected eco-region
        self.obis: pd.DataFrame = get_obis(eco_code=eco_code)
        # All species in other db (WoRMs, GISD, NatCon)
        self.observations: pd.DataFrame = observations(self.obis)

    @property
    def aliens(self) -> pd.DataFrame:
        """
        Return aliens species in currently selected eco-region.

        Returns
        -------
        pd.DataFrame
            aliens species
        """
        aliens = self.observations[
            (self.observations["establishmentMeans"] == "Alien")
            & (self.observations["ECO_CODE"] == self.eco_code)
        ].reset_index(drop=True)
        # Report as alien as soon as it is reported as alien in one of the
        # datasources. Column dataset reports all datasources which report a
        # species as alien.
        df = aliens.groupby(["aphiaID", "ECO_CODE_X"], as_index=False)["dataset"].agg(
            {"dataset": lambda x: ",".join(x)}
        )
        df.drop(["ECO_CODE_X"], axis=1, inplace=True)
        aliens = aliens.merge(df, on=["aphiaID"], how="inner")
        aliens["dataset"] = aliens["dataset_y"]
        aliens.drop(["dataset_x", "dataset_y"], axis=1, inplace=True)
        return aliens

    @property
    def all_species(self) -> List[str]:
        """
        List all unique species reported by obis.

        Returns
        -------
        list
            species names
        """
        df = self.observations[
            self.observations["ECO_CODE"] == self.eco_code
        ].reset_index(drop=True)

        return df["species"].unique().tolist()

    @property
    def affected_by_invasive(self) -> List[str]:
        """
        List all species which are affected by invasive species.

        Returns
        -------
        list
            species names
        """
        affected = read_taxonomy()
        ret = pd.merge(self.obis, affected, on="species", how="inner")

        return ret[["species", "aphiaID"]].drop_duplicates()


def plot(eco_code):
    """
    Plot world map with selected MEOW eco region

    Parameters
    ----------
    eco_code: int or Species obj
        If int is set as eco_code the plot will try to get eco region from
        MEOW and plot it. If no eco region is found for the int eco_code
        the function will raise ValueError.

    Returns
    ---------
    matplotlib plot

    Raises:
    -------
    Value Error
        When eco-region for the eco_code was not found.
    """

    world = gpd.read_file(gpd.datasets.get_path("naturalearth_lowres"))
    fig, ax = plt.subplots(figsize=(20, 30))
    ax.set_aspect("equal")
    world.plot(ax=ax, color="white", edgecolor="black")

    gdf = marine_ecoregions(eco_code=eco_code)
    if gdf.empty:
        raise ValueError(
            "Seems like the eco region should be plotted but "
            "no eco region found for eco code: {}.".format(eco_code)
        )
    coords = gdf.iloc[0]["geometry"]
    if coords.geom_type == "MultiPolygon":
        for polygon in coords:
            x, y = polygon.exterior.coords.xy
            x = x.tolist()
            y = y.tolist()
            xym = list(zip(x, y))
            poly = Polygon(xym, facecolor="blue",
                           edgecolor="blue", linewidth=2)
            plt.gca().add_patch(poly)
    else:
        x, y = coords.exterior.coords.xy
        x = x.tolist()
        y = y.tolist()
        xym = list(zip(x, y))
        poly = Polygon(xym, facecolor="blue", edgecolor="blue", linewidth=2)
        plt.gca().add_patch(poly)
    plt.title("{} / {}".format(gdf.iloc[0]["ECOREGION"], gdf.iloc[0]["REALM"]))
    plt.show()
