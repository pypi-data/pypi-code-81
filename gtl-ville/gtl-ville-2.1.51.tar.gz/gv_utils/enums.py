#!/usr/bin/env python3


class AttId:
    att = 'att'
    centerxy = 'centerxy'
    datapointeid = 'datapointeid'
    datapointseids = 'datapointseids'
    datatypeeid = 'datatypeeid'
    eid = 'eid'
    ffspeed = 'ffspeed'
    fow = 'fow'
    frc = 'frc'
    fromno = 'fromno'
    geom = 'geom'
    geomxy = 'geomxy'
    id = 'id'
    length = 'length'
    mainroad = 'mainroad'
    maxspeed = 'maxspeed'
    name = 'name'
    nlanes = 'nlanes'
    no = 'no'
    roadeid = 'roadeid'
    roads = 'roads'
    tono = 'tono'
    sample = 'sample'
    validfrom = 'validfrom'
    validto = 'validto'
    webatt = 'webatt'
    zoneeid = 'zoneeid'


class CsvData:
    samples = 'samples'
    timestamp = 'timestamp'

    confidence = 'confidence'
    density = 'density'
    flow = 'flow'
    fluidity = 'fluidity'
    occupancy = 'occupancy'
    speed = 'speed'
    status = 'status'
    traveltime = 'traveltime'
    vehicle = 'vehicle'


class DataTypeId:
    karrusrd = 'karrusrd'
    metropme = 'metropme'
    tomtomfcd = 'tomtomfcd'
    density = 'density'
    vehicles = 'vehicles'
    fluidity = 'fluidity'
    partitions = 'partitions'
    partitionstraveltime = 'partitionstraveltime'

    dataquality = 'dataquality'
    datapoints = 'datapoints'
    roads = 'roads'
    mappingroadsdatapoints = 'mappingroadsdatapoints'
    zonespoints = 'zonespoints'

    imputedprefixe = 'imputed'


INDICATORS_DATA_TYPES = (DataTypeId.karrusrd, DataTypeId.metropme, DataTypeId.tomtomfcd, DataTypeId.density,
                         DataTypeId.fluidity, DataTypeId.partitions)

IMPUTED_INDICATORS_DATA_TYPES = tuple(('-'.join((DataTypeId.imputedprefixe, dt)) for dt in INDICATORS_DATA_TYPES))

MISSING_VALUE = -1
NO_VALUE = ''
