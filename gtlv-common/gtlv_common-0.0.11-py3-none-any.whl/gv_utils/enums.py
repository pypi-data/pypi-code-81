#!/usr/bin/env python3


class DbColumn:
    separator = '.'

    att = 'att'
    classification = 'classification'
    confidence = 'confidence'
    datapoint = 'data_point'
    datatype = 'data_type'
    dataquality = 'data_quality'
    day = 'day'
    density = 'density'
    eid = 'eid'
    flow = 'flow'
    fluidity = 'fluidity'
    fromtraveltime = 'from_travel_time'
    fromroad = 'from_road'
    fromturnratio = 'from_turn_ratio'
    fromzonepoint = 'from_zone_point'
    geom = 'geom'
    id = 'id'
    imputedindicator = 'imputed_indicator'
    indicator = 'indicator'
    networkdataquality = 'network_data_quality'
    networkindicator = 'network_indicator'
    occupancy = 'occupancy'
    ratio = 'ratio'
    road = 'road'
    roadcenter = 'road_center'
    samples = 'samples'
    sampletime = 'sample_time'
    timestamp = 'timestamp'
    speed = 'speed'
    totraveltime = 'to_travel_time'
    toroad = 'to_road'
    toturnratio = 'to_turn_ratio'
    tozonepoint = 'to_zone_point'
    traveltime = 'travel_time'
    validfrom = 'valid_from'
    validto = 'valid_to'
    vehicle = 'vehicle'
    webatt = 'web_att'


class DbTable:
    datapoint = 'data_point'
    datapointdataquality = 'data_point_data_quality'
    datapointimputedindicator = 'data_point_imputed_indicator'
    datapointindicator = 'data_point_indicator'
    datatype = 'data_type'
    networkdataquality = 'network_data_quality'
    networkindicator = 'network_indicator'
    road = 'road'
    roadcenter = 'road_center'
    roaddatapoint = 'road_data_point'
    roaddataquality = 'road_data_quality'
    roadindicator = 'road_indicator'
    turnratio = 'turn_ratio'
    zonepoint = 'zone_point'
    zonepointtraveltime = 'zone_point_travel_time'


class Message:
    data = 'data'
    format = 'format'
    timestamp = 'timestamp'
    kind = 'kind'


class MessageData(DbColumn):
    csvseparator = ';'
    encoding = 'utf-8'
    separator = '_'

    status = 'status'

    late = -2
    nan = -1

    hendday = 21
    hstartday = 6

    max = 'max'
    mean = 'mean'
    min = 'min'


class AttId(DbColumn):
    centerxy = 'centerxy'
    datapointseids = 'datapoints'
    datatypeeid = 'datatypeeid'
    ffspeed = 'ffspeed'
    fow = 'fow'
    frc = 'frc'
    fromno = 'fromno'
    geomxy = 'geomxy'
    length = 'length'
    mainroad = 'mainroad'
    maxspeed = 'maxspeed'
    name = 'name'
    nlanes = 'nlanes'
    no = 'no'
    roads = 'roads'
    tono = 'tono'
    zone = 'zone'


class MessageFormat:
    json = 'json'
    csv = 'csv'


class MessageKind:
    separator = '-'

    mainprefix = 'gtlv'

    past = 'past'

    imputed = 'imputed'

    dataquality = 'dataquality'
    datapoint = 'datapoint'
    datatype = 'datatype'
    indicator = 'indicator'
    mappingroadsdatapoints = 'mappingroadsdatapoints'
    network = 'network'
    partitions = 'partitions'
    partitionstraveltime = 'partitionstraveltime'
    traveltime = 'traveltime'
    turnratio = 'turnratio'
    vehicles = 'vehicles'

    density = 'density'
    fluidity = 'fluidity'
    karrusrd = 'karrusrd'
    metropme = 'metropme'
    road = 'road'
    roadcenter = 'roadcenter'
    tomtomfcd = 'tomtomfcd'
    zonepoint = 'zonepoint'


class RequestParam(MessageKind):
    separator = ','

    internalflag = 'internal'

    eid = 'eid'
    fields = 'fields'
    fromdatetime = 'fromdatetime'
    frompoint = 'frompoint'
    fromroad = 'fromroad'
    period = 'period'
    sampling = 'sampling'
    todatetime = 'todatetime'
    topoint = 'topoint'
    toroad = 'toroad'
    window = 'window'
    within = 'within'

    day = 'day'
    month = 'month'
    week = 'week'


class RequestPath(MessageKind):
    separator = '/'


class NetworkObjId:
    datapointsroadsmap = 'datapointsroadsmap'
    frcroadsmap = 'frcroadsmap'
    lonlatnodesmatrix = 'lonlatnodesmatrix'
    mainclustersgeom = 'mainclustersgeom'
    newdpmappings = 'newdpmappings'
    newzonemappings = 'newzonemappings'
    omiteddatapoints = 'omiteddatapoints'
    roadclustermap = 'roadclustermap'
    roadsdatamap = 'roadsdatamap'
    roadsffspeedmap = 'roadsffspeedmap'
    roadszonesmap = 'roadszonesmap'
    voronoiroadmap = 'voronoiroadmap'
    zonesdatamap = 'zonesdatamap'
