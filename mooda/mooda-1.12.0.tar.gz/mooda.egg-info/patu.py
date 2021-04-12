import pandas as pd
import plotly.express as px
import mooda as md

path = r'C:\Users\rbard\Documents\datos\pati-cientific\2021-02-05\raw-measurements.CSV'
path_kml = r'C:\Users\rbard\Documents\datos\pati-cientific\2021-02-05\20210205015930-38132-data.txt'

df = pd.read_csv(path)
# df_sensors = df[['TIME', 'AS_TEMP', 'TEMP']]
df_sensors = df[['TIME', 'AS_TEMP']]

df_sensors['TIME'] = pd.to_datetime(df_sensors['TIME'], utc=True)
df_sensors.set_index('TIME', inplace=True)

df_geo = pd.read_csv(path_kml, sep='\t')
df_geo = df_geo[['time', 'latitude', 'longitude']]
df_geo['time'] = pd.to_datetime(df_geo['time'], utc=True)
df_geo.set_index('time', inplace=True)

df_sensors_reindex = df_sensors.reindex(df_geo.index, method='nearest')
df_total = pd.merge(df_sensors_reindex, df_geo, on=['time'], how='inner')
df_total.reset_index(inplace=True)
df_total['time'] = df_total['time'].dt.round('1s')

# Plots

px.set_mapbox_access_token("pk.eyJ1IjoiYmFyZGFqaSIsImEiOiJjank0Z283NjkxMWtxM2NxOGJqaHp5Njh0In0.KAdUAjLEHxqPgFzv4w0-ew")

# fig = px.scatter_mapbox(df_total, lat="latitude", lon="longitude", color="AS_TEMP", size_max=15,
#                         zoom=14.5, animation_frame=df_total['time'].astype(str),
#                         range_color=[min(df_total['AS_TEMP']), max(df_total['AS_TEMP'])],
#                         title='Patí Científic 2021-02-04', labels={'AS_TEMP': "Temperatura de l'aigua"})
# fig.show()

fig2 = px.scatter_mapbox(df_total, lat="latitude", lon="longitude", color="AS_TEMP", size_max=15,
                        zoom=14.5,
                        range_color=[min(df_total['AS_TEMP']), max(df_total['AS_TEMP'])],
                        title='Patí Científic 2021-02-04', labels={'AS_TEMP': "Temperatura de l'aigua"})
fig2.show()

# fig.write_html("sortida-pati.html")
# fig2.write_html("sortida-pati-play.html")

# df_total.rename(
#     columns={'time': 'TIME', 'TEMP': 'DRYT', 'AS_TEMP': 'SSTI', 'latitude': 'LATITUDE', 'longitude': 'LONGITUDE'},
#     inplace=True)
df_total.rename(
    columns={'time': 'TIME', 'AS_TEMP': 'SSTI', 'latitude': 'LATITUDE', 'longitude': 'LONGITUDE'},
    inplace=True)

df_total['DEPTH'] = 1
# df_total['DRYT_QC'] = 1
df_total['DEPTH_QC'] = 1
df_total['SSTI_QC'] = 1
df_total['LATITUDE_QC'] = 1
df_total['LONGITUDE_QC'] = 1

df_total.set_index(['DEPTH', 'TIME'], inplace=True)

vocabulary = {
    'TIME': {
        'standard_name': 'time',
        'units': 'number of seconds that have elapsed since January 1, 1970 (midnight UTC/GMT)',
        'axis': 'T',
        'long_name': 'time of measurement',
        'valid_min': -9223372036854775808,
        'valid_max': 9223372036854775808,
        'QC_indicator': 'excellent',
        'processing_level': 'Ranges applied, bad data flagged',
        'uncertainty': 'nan',
        'comment': 'Time is going be visualized as YYYY/MM/DD hh:mm:ss'},
    'TIME_QC': {
        'long_name': 'quality flag for TIME',
        'flag_values': [0, 1, 2, 3, 4, 7, 8, 9],
        'flag_meanings': 'unknown good_data probably_good_data potentially_correctable_bad_data' \
            'bad_data nominal_value interpolated_value missing_value'},
    'DEPTH': {
        'standard_name': 'depth',
        'units': 'meters',
        'positive': 'down',
        'axis': 'Z',
        'reference': 'sea_level',
        'coordinate_reference_frame': 'urn:ogc:def:crs:EPSG::5831',
        'long_name': 'Depth of measurement',
        '_FillValue': 'nan',
        'valid_min': -10,
        'valid_max': 12000,
        'QC_indicator': 'excellent',
        'processing_level': 'Ranges applied, bad data flagged',
        'uncertainty': 'nan',
        'comment': 'Depth calculated from the sea surface'},
    'DEPTH_QC': {
        'long_name': 'quality flag for DEPTH',
        'flag_values': [0, 1, 2, 3, 4, 7, 8, 9],
        'flag_meanings': 'unknown good_data probably_good_data potentially_correctable_bad_data' \
            'bad_data nominal_value interpolated_value missing_value'},
    'SSTI': {
        'standard_name': 'sea_surface_temperature',
        'units': 'degree_C',
        '_FillValue': 'nan',
        'coordinates': 'DEPTH, TIME, LATITUDE, LONGITUDE',
        'long_name': 'Sea Surface Temperature',
        'QC_indicator': 'excelent',
        'processing_level': 'Ranges applied, bad data flagged',
        'valid_min': 0,
        'valid_max': 40,
        'comment': 'n/a',
        'ancillary_variables': 'TEMP_QC',
        'history': 'n/a',
        'uncertainty': 0.05,
        'accuracy': 0.35,
        'precision': 0.1,
        'resolution': 0.01,
        'cell_methods': 'TIME: point DEPTH: point LATITUDE: point LONGITUDE:' \
            ' point',
        'DM_indicator': 'D',
        'reference_scale': 'n/a',
        'sensor_model': 'PT-100, AtlasCIentific 100mm Temperature ' \
            'Thermowell, SmartCitizen board',
        'sensor_manufacturer': 'Fab Lab, Barcelona',
        'sensor_reference': 'https://docs.smartcitizen.me/Guides/deployment' \
            's/Soil%20and%20water%20sensors/',
        'sensor_serial_number': 'n/a',
        'sensor_mount': 'in_continuous_box',
        'sensor_orientation': 'downward'},
    'SSTI_QC': {
        'long_name': 'quality flag for SSTI',
        'flag_values': [0, 1, 2, 3, 4, 7, 8, 9],
        'flag_meanings': 'unknown good_data probably_good_data potentially_correctable_bad_data' \
            'bad_data nominal_value interpolated_value missing_value'},
    'LATITUDE': {
        'standard_name': 'latitude',
        'units': 'degrees_north',
        'axis': 'Y',
        'long_name': 'Latitude of measurement',
        'reference': 'WGS84',
        'coordinate_reference_frame': 'urn:ogc:def:crs:EPSG::4326',
        'valid_min': -90.0,
        'valid_max': 90.0,
        'QC_indicator': 'excellent',
        'processing_level': 'Ranges applied, bad data flagged',
        'uncertainty': 2,
        'accuracy': 10,
        'comment': 'Possition obtained with an Android phone'},
    'LATITUDE_QC': {
        'long_name': 'quality flag for LATITUDE',
        'flag_values': [0, 1, 2, 3, 4, 7, 8, 9],
        'flag_meanings': 'unknown good_data probably_good_data potentially_correctable_bad_data' \
            'bad_data nominal_value interpolated_value missing_value'},
    'LONGITUDE': {
        'standard_name': 'longitude',
        'units': 'degrees_east',
        'axis': 'X',
        'long_name': 'Longitude of measurement',
        'reference': 'WGS84',
        'coordinate_reference_frame': 'urn:ogc:def:crs:EPSG::4326',
        'valid_min': -180.0,
        'valid_max': 180.0,
        'QC_indicator': 'excellent',
        'processing_level': 'Ranges applied, bad data flagged',
        'uncertainty': 2,
        'accuracy': 10,
        'comment': 'Possition obtained with an Android phone'},
    'LONGITUDE_QC': {
        'long_name': 'quality flag for LATITUDE',
        'flag_values': [0, 1, 2, 3, 4, 7, 8, 9],
        'flag_meanings': 'unknown good_data probably_good_data potentially_correctable_bad_data' \
            'bad_data nominal_value interpolated_value missing_value'},
}

# Metadata definition
metadata = {
    # Discovery and identification
    'DOI': '10.5281/zenodo.4551588',
    'site_code': 'somorrostro',
    'platform_code': 'pati-cientific_2021-02-04',
    'data_mode': 'D',
    'title': 'Sea Surface Temperature',
    'summary': 'Sea surface temperature observations measure with the Pati ' \
        'Cientific at Somorrostro, Barcelona the afternoon of 2021-02-04.',
    'naming_authority': 'CSIC',
    'id': 'OS_pati-cientific_20210205_T',
    'wmo_platform_code': 'n/a',
    'source': 'ship',
    'principal_investigator': 'Josep Lluis Pelegri',
    'principal_investigator_email': 'pelegri@icm.csic.es',
    'principal_investigator_url': 'http://oce.icm.csic.es/ca/pelegri',
    'principal_investigator_id': 'https://orcid.org/0000-0003-0661-2190',
    'creator_name': 'Ignasi Valles',
    'creator_email': 'valles@icm.csic.es',
    'creator_url': 'https://www.icm.csic.es/en/staff/ignasi-berenguer-valles-casanova-365',
    'creator_id': 'https://orcid.org/0000-0003-2084-852X',
    'creator_type': 'group',
    'creator_institution': 'ICM-CSIC',
    'array': 'n/a',
    'network': 'pati-cientific',
    'keywords_vocabulary': 'CF',
    'keywords': 'sea surface temperature, Somorrostro, Barcelona, Pati Vela',
    'comment': 'Data collected by Ignasi Valles',
    # Geo-spatial-temporal
    'sea_area': 'Barcelona',
    'geospatial_lat_min': min(df_total['LATITUDE']),
    'geospatial_lat_max': max(df_total['LATITUDE']),
    'geospatial_lat_units': 'degree_north',
    'geospatial_lon_min': min(df_total['LONGITUDE']),
    'geospatial_lon_max': max(df_total['LONGITUDE']),
    'geospatial_lon_units': 'degree_east',
    'geospatial_vertical_min': 0,
    'geospatial_vertical_max': 0.5,
    'geospatial_vertical_positive': 'down',
    'geospatial_vertical_units': 'meter',
    'time_coverage_start': '2021-02-04T15:18:39Z',
    'time_coverage_end': '2021-02-04T16:35:39Z',
    'time_coverage_duration': 'PT1H17M',
    'time_coverage_resolution': 'PT1M',
    'cdm_data_type': 'trajectory',
    'featureType': 'timeSeries',
    'platform_deployment_date': '2021-02-04T15:18:39Z',
    'platform_deployment_ship_name': 'pati cientific',
    'platform_deployment_cruise_name': 'Clase 2021-02-04',
    'platform_deployment_ship_ICES_code': 'n/a',
    'platform_deployment_cruise_ExpoCode': 'n/a',
    'platform_recovery_date': '2021-02-04T17:30:00Z',
    'platform_recovery_ship_name': 'pati cientific',
    'platform_recovery_cruise_name': 'Clase 2021-02-04',
    'platform_recovery_ship_ICES_code': 'n/a',
    'platform_recovery_cruise_ExpoCode': 'n/a',
    'data_type': 'OceanSITES trajectory data',
    # Conventions used
    'format_version': '1.5',
    'Conventions': 'CF-1.6, OceanSITES-1.5',
    # Publication information
    'publisher_name': 'Raul Bardaji',
    'publisher_email': 'bardaji@utm.csic.es',
    'publisher_url': 'https://www.linkedin.com/in/raul-bardaji-benach/',
    'publisher_id': 'https://orcid.org/0000-0002-0803-3427',
    'references': 'http://www.oceansites.org, https://paticientific.org/',
    'data_assembly_center': 'UTM-CSIC',
    'update_interval': 'n/a',
    'license': 'Creative Commons: Attribution-ShareAlike 4.0 International',
    'citation': 'These data were collected and made freely available by the ' \
        'Pati Cientific project and the national programs that contribute to' \
        ' it.',
    'acknowledgement': 'EMSO - Laboratorios Submarinos Profundos',
    # Provinance
    'date_created': '2021-02-05T23:49:07Z',
    'date_modified': '2021-02-05T23:49:07Z',
    'history': '2021-02-04T17:30:00Z data collected, I. Valles. ' \
        '2021-02-05T23:49:07Z file with provisional data compiled and sent ' \
        'to Zenodo (DOI: 10.5281/zenodo.4522201), R. Bardaji. ' \
        '2021-02-17T10:00:00Z dataset revised, N. Hoareau, I. Valles, ' \
        'JL. Pelegri. 2021-02-19T15:30:00Z file with revised data compiled ' \
        'and sent to Zenodo (DOI: 10.5281/zenodo.4551588), R. Bardaji',
    'processing_level': 'Ranges applied, bad data flagged',
    'QC_indicator': 'excellent',
    'contributor_name': 'Josep Lluis Pelegri; Ignasi Valles; Raul Bardaji;' \
        ' Kintxo Salvador; Nina Hoareau; Carine Simon; Carlos Rodero; ' \
        'Jaume Piera; Inma Ortigosa; Jordi Mateu; Marcel.la Castells; ' \
        'Rafel Figuerola; Albert Carbonell; Victor Barberan; Oscar Gonzalez; ' \
        'Oriol Carrasco; Joan Puigdefabregas; Iphygenia Yannoukakou; Igor ' \
        'Carretero',
    'contributor_role': 'Oceanographer; Oceanographer; Engineer; Technician; ' \
        'Oceanographer; Oceanographer; Technician; Scientist; Resercher and ' \
        'teacher; Technician and teacher; Resercher and teacher; President of' \
        ' Club Pati Vela; Manager of Club Pati Vela, Sensor developer, ' \
        'Sensor developer, Sensor developer, Oceanographer, Web designer',
    'contributor_email': 'pelegri@icm.csic.es; valles@icm.csic.es; ' \
        'bardaji@utm.csic.es; jsalvador@icm.csic.es; nhoareau@icm.csic.es; ' \
        'carine.simon@csic.es; rodero@icm.csic.es; jpiera@icm.csic.es; ' \
        'iortigosa@cen.upc.edu; jordi.mateu@upc.edu; ' \
        'marcella.castells@upc.edu; info@pativelabarcelona.com; ' \
        'info@pativelabarcelona.com; victor@smartcitizen.me; ' \
        'oscar@smartcitizen.me; n/a; n/a; n/a; n/a'}

wf = md.WaterFrame()
wf.data = df_total.copy()
wf.metadata = metadata.copy()
wf.vocabulary = vocabulary.copy()

# wf.to_csv('OS_pati-cientific_20210205_T_v0.2.csv')
# wf.to_nc('OS_pati-cientific_20210205_T_v0.2.nc')
# wf.to_pkl('OS_pati-cientific_20210205_T_v0.2.pkl')

df = wf.data.copy()
df.reset_index(inplace=True)
del df['TIME']
del df['LATITUDE_QC']
del df['LONGITUDE_QC']
del df['SSTI_QC']
del df['DEPTH']
del df['DEPTH_QC']
df2 = df[['LONGITUDE', 'LATITUDE', 'SSTI']]
print(df2)
# df2.to_csv('test.csv', header=False, index=False)

