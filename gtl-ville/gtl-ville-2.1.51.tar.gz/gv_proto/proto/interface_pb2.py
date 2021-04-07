# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: gv_proto/proto/interface.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import any_pb2 as google_dot_protobuf_dot_any__pb2
from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2
from gv_proto.proto import archivist_pb2 as gv__proto_dot_proto_dot_archivist__pb2
from gv_proto.proto import broadcaster_pb2 as gv__proto_dot_proto_dot_broadcaster__pb2
from gv_proto.proto import common_pb2 as gv__proto_dot_proto_dot_common__pb2
from gv_proto.proto import geographer_pb2 as gv__proto_dot_proto_dot_geographer__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='gv_proto/proto/interface.proto',
  package='gv_proto.proto',
  syntax='proto3',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x1egv_proto/proto/interface.proto\x12\x0egv_proto.proto\x1a\x19google/protobuf/any.proto\x1a\x1bgoogle/protobuf/empty.proto\x1a\x1egv_proto/proto/archivist.proto\x1a gv_proto/proto/broadcaster.proto\x1a\x1bgv_proto/proto/common.proto\x1a\x1fgv_proto/proto/geographer.proto2\x87\t\n\tInterface\x12<\n\x07publish\x12\x1a.gv_proto.proto.PubRequest\x1a\x13.gv_proto.proto.Ack\"\x00\x12\x41\n\tsubscribe\x12\x1a.gv_proto.proto.SubRequest\x1a\x14.google.protobuf.Any\"\x00\x30\x01\x12S\n\x0eget_indicators\x12!.gv_proto.proto.IndicatorsRequest\x1a\x1a.gv_proto.proto.Indicators\"\x00\x30\x01\x12U\n\x10get_data_quality\x12\".gv_proto.proto.DataQualityRequest\x1a\x1b.gv_proto.proto.DataQuality\"\x00\x12X\n\x11get_location_data\x12#.gv_proto.proto.LocationDataRequest\x1a\x1c.gv_proto.proto.LocationData\"\x00\x12q\n\x1aget_partitions_travel_time\x12+.gv_proto.proto.PartitionsTravelTimeRequest\x1a$.gv_proto.proto.PartitionsTravelTime\"\x00\x12O\n\x1d\x61\x64\x64_mapping_roads_data_points\x12\x17.gv_proto.proto.Mapping\x1a\x13.gv_proto.proto.Ack\"\x00\x12\x43\n\x0f\x61\x64\x64_data_points\x12\x19.gv_proto.proto.Locations\x1a\x13.gv_proto.proto.Ack\"\x00\x12G\n\x16import_shapefile_to_db\x12\x16.google.protobuf.Empty\x1a\x13.gv_proto.proto.Ack\"\x00\x12P\n\x0fget_data_points\x12 .gv_proto.proto.LocationsRequest\x1a\x19.gv_proto.proto.Locations\"\x00\x12J\n\tget_roads\x12 .gv_proto.proto.LocationsRequest\x1a\x19.gv_proto.proto.Locations\"\x00\x12Q\n\x10get_zones_points\x12 .gv_proto.proto.LocationsRequest\x1a\x19.gv_proto.proto.Locations\"\x00\x12Z\n\x1dget_mapping_roads_data_points\x12\x1e.gv_proto.proto.MappingRequest\x1a\x17.gv_proto.proto.Mapping\"\x00\x12T\n\x1bupdate_roads_freeflow_speed\x12\x1e.gv_proto.proto.FreeflowSpeeds\x1a\x13.gv_proto.proto.Ack\"\x00\x62\x06proto3'
  ,
  dependencies=[google_dot_protobuf_dot_any__pb2.DESCRIPTOR,google_dot_protobuf_dot_empty__pb2.DESCRIPTOR,gv__proto_dot_proto_dot_archivist__pb2.DESCRIPTOR,gv__proto_dot_proto_dot_broadcaster__pb2.DESCRIPTOR,gv__proto_dot_proto_dot_common__pb2.DESCRIPTOR,gv__proto_dot_proto_dot_geographer__pb2.DESCRIPTOR,])



_sym_db.RegisterFileDescriptor(DESCRIPTOR)



_INTERFACE = _descriptor.ServiceDescriptor(
  name='Interface',
  full_name='gv_proto.proto.Interface',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_start=235,
  serialized_end=1394,
  methods=[
  _descriptor.MethodDescriptor(
    name='publish',
    full_name='gv_proto.proto.Interface.publish',
    index=0,
    containing_service=None,
    input_type=gv__proto_dot_proto_dot_broadcaster__pb2._PUBREQUEST,
    output_type=gv__proto_dot_proto_dot_common__pb2._ACK,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='subscribe',
    full_name='gv_proto.proto.Interface.subscribe',
    index=1,
    containing_service=None,
    input_type=gv__proto_dot_proto_dot_broadcaster__pb2._SUBREQUEST,
    output_type=google_dot_protobuf_dot_any__pb2._ANY,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='get_indicators',
    full_name='gv_proto.proto.Interface.get_indicators',
    index=2,
    containing_service=None,
    input_type=gv__proto_dot_proto_dot_archivist__pb2._INDICATORSREQUEST,
    output_type=gv__proto_dot_proto_dot_archivist__pb2._INDICATORS,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='get_data_quality',
    full_name='gv_proto.proto.Interface.get_data_quality',
    index=3,
    containing_service=None,
    input_type=gv__proto_dot_proto_dot_archivist__pb2._DATAQUALITYREQUEST,
    output_type=gv__proto_dot_proto_dot_archivist__pb2._DATAQUALITY,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='get_location_data',
    full_name='gv_proto.proto.Interface.get_location_data',
    index=4,
    containing_service=None,
    input_type=gv__proto_dot_proto_dot_archivist__pb2._LOCATIONDATAREQUEST,
    output_type=gv__proto_dot_proto_dot_archivist__pb2._LOCATIONDATA,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='get_partitions_travel_time',
    full_name='gv_proto.proto.Interface.get_partitions_travel_time',
    index=5,
    containing_service=None,
    input_type=gv__proto_dot_proto_dot_archivist__pb2._PARTITIONSTRAVELTIMEREQUEST,
    output_type=gv__proto_dot_proto_dot_archivist__pb2._PARTITIONSTRAVELTIME,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='add_mapping_roads_data_points',
    full_name='gv_proto.proto.Interface.add_mapping_roads_data_points',
    index=6,
    containing_service=None,
    input_type=gv__proto_dot_proto_dot_geographer__pb2._MAPPING,
    output_type=gv__proto_dot_proto_dot_common__pb2._ACK,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='add_data_points',
    full_name='gv_proto.proto.Interface.add_data_points',
    index=7,
    containing_service=None,
    input_type=gv__proto_dot_proto_dot_geographer__pb2._LOCATIONS,
    output_type=gv__proto_dot_proto_dot_common__pb2._ACK,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='import_shapefile_to_db',
    full_name='gv_proto.proto.Interface.import_shapefile_to_db',
    index=8,
    containing_service=None,
    input_type=google_dot_protobuf_dot_empty__pb2._EMPTY,
    output_type=gv__proto_dot_proto_dot_common__pb2._ACK,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='get_data_points',
    full_name='gv_proto.proto.Interface.get_data_points',
    index=9,
    containing_service=None,
    input_type=gv__proto_dot_proto_dot_geographer__pb2._LOCATIONSREQUEST,
    output_type=gv__proto_dot_proto_dot_geographer__pb2._LOCATIONS,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='get_roads',
    full_name='gv_proto.proto.Interface.get_roads',
    index=10,
    containing_service=None,
    input_type=gv__proto_dot_proto_dot_geographer__pb2._LOCATIONSREQUEST,
    output_type=gv__proto_dot_proto_dot_geographer__pb2._LOCATIONS,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='get_zones_points',
    full_name='gv_proto.proto.Interface.get_zones_points',
    index=11,
    containing_service=None,
    input_type=gv__proto_dot_proto_dot_geographer__pb2._LOCATIONSREQUEST,
    output_type=gv__proto_dot_proto_dot_geographer__pb2._LOCATIONS,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='get_mapping_roads_data_points',
    full_name='gv_proto.proto.Interface.get_mapping_roads_data_points',
    index=12,
    containing_service=None,
    input_type=gv__proto_dot_proto_dot_geographer__pb2._MAPPINGREQUEST,
    output_type=gv__proto_dot_proto_dot_geographer__pb2._MAPPING,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='update_roads_freeflow_speed',
    full_name='gv_proto.proto.Interface.update_roads_freeflow_speed',
    index=13,
    containing_service=None,
    input_type=gv__proto_dot_proto_dot_geographer__pb2._FREEFLOWSPEEDS,
    output_type=gv__proto_dot_proto_dot_common__pb2._ACK,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_INTERFACE)

DESCRIPTOR.services_by_name['Interface'] = _INTERFACE

# @@protoc_insertion_point(module_scope)
