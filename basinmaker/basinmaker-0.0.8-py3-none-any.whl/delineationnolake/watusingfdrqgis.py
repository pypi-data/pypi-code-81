from basinmaker.func.grassgis import *
from basinmaker.func.qgis import *
from basinmaker.func.pdtable import *
from basinmaker.func.rarray import *
from basinmaker.utilities.utilities import *


def delineate_watershed_no_lake_using_fdr(
    grassdb,
    grass_location,
    qgis_prefix_path,
    input_geo_names,
    fdr_path,
    acc_thresold,
    fdr_arcgis,
    fdr_grass,
    str_r,
    str_v,
    acc,
    cat_no_lake,
    max_memroy,
):
    mask = input_geo_names["mask"]
    dem = input_geo_names["dem"]
    
    import grass.script as grass
    import grass.script.setup as gsetup
    from grass.pygrass.modules import Module
    from grass.pygrass.modules.shortcuts import general as g
    from grass.pygrass.modules.shortcuts import raster as r
    from grass.script import array as garray
    from grass.script import core as gcore
    from grass_session import Session

    os.environ.update(
        dict(GRASS_COMPRESS_NULLS="1", GRASS_COMPRESSOR="ZSTD", GRASS_VERBOSE="1")
    )
    PERMANENT = Session()
    PERMANENT.open(gisdb=grassdb, location=grass_location, create_opts="")

    write_grass_and_arcgis_fdr_rules(grassdb)
    print("using fder dataset     ")
    grass_raster_r_in_gdal(grass, raster_path=fdr_path, output_nm="fdr_arcgis_temp")
    # reclassify it into grass flow direction data
    grass_raster_r_reclass(
        grass,
        input="fdr_arcgis_temp",
        output="fdr_grass_temp",
        rules=os.path.join(grassdb, "Arcgis2GrassDIR.txt"),
    )
    # calcuate flow accumulation from provided dir
    grass_raster_r_accumulate(
        grass, direction="fdr_grass_temp", accumulation=acc
    )

    grass_raster_r_stream_extract(
        grass,
        elevation=dem,
        accumulation=acc,
        threshold=int(acc_thresold),
        stream_raster=str_r,
        stream_vector=str_v,
        direction=fdr_grass,
        memory=max_memroy,
    )
    # create a arcgis flow direction
    grass_raster_r_reclass(
        grass,
        input=fdr_grass,
        output=fdr_arcgis,
        rules=os.path.join(grassdb, "Grass2ArcgisDIR.txt"),
    )

    grass_raster_r_stream_basins(
        grass,
        direction=fdr_grass,
        stream=str_r,
        basins=cat_no_lake,
        memory=max_memroy,
    )

    PERMANENT.close()
    return
