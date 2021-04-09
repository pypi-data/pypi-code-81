import numpy as np
from .auth import get_access_token
import json
import requests
import logging
import base64
import math
from .api_urls import get_storage_index_files_api_url,  \
    get_storage_index_request_permission_token_api_url,\
    get_asset_file_entry_api_url

logger = logging.Logger(__name__)


class AnnotationDto(object):
    '''
    The slide annotation struct.

    Args:
        tags (list(str)): a lot of tag strings.

        comments (str): a comment string to annotation.

        bounds (list[int]): a area with location and size.

        vertices (list[list[int]]): vertices of annotation shape.
    '''

    def __init__(self,
                 tags,
                 comments,
                 bounds,
                 vertices) -> None:
        self.Tags = tags
        self.Comments = comments
        self.Bounds = bounds
        self.Vertices = vertices

    def __repr__(self) -> str:
        return f"AnnotationDto(Tags={self.Tags},"\
            f"Comments={self.Comments},"\
            f"Bounds = {self.Bounds}, "\
            f"Vertices = {self.Vertices})"


class SlideEntryDto:
    '''
    The slide entry of slide in the storage. it contains slide entry informations.

    Args:
        name (str): the name of slide entry.

        pathName (str): the path of slide in the Coriander explorer.

        scheme (str): fixed with 'slide'

        storageId (str): Important it represent identity of slide. We can open slide with it.

        creatorId (str): creator of slide entry.

        creationTime (date): creation time of slide entry.

        lastModifierId (str): last modifier of slide entry.

        lastModificationTime (date): last modification time of slide entry.
    '''

    def __init__(self, id,
                 name,
                 pathName,
                 scheme,
                 storageId,
                 creatorId,
                 creationTime,
                 lastModifierId,
                 lastModificationTime):
        self.Id = id
        self.Name = name
        self.PathName = pathName
        self.Scheme = scheme
        self.StorageId = storageId
        self.CreatorId = creatorId
        self.CreationTime = creationTime
        self.LastModifierId = lastModifierId
        self.LastModificationTime = lastModificationTime

    def __repr__(self) -> str:
        return f"FileDto(Id={self.Id}, \
            Name={self.Name}, \
            PathName={self.PathName}, \
            Scheme={self.Scheme}, \
            StorageId={self.StorageId}, \
            CreatorId={self.CreatorId}, \
            CreationTime={self.CreationTime}, \
            LastModifierId={self.LastModifierId}, \
            LastModificationTime={self.LastModificationTime}, \
            )"


def _api_organization_files(filter_by_path=None,
                            filter_by_name=None,
                            filter_by_begin_time=None,
                            filter_by_end_time=None):
    access_token = get_access_token()
    headers = {"Authorization": f"Bearer {access_token}"}
    params = {
        "PathName": filter_by_path,
        "Name": filter_by_name,
        "CreationTimeRegion": filter_by_begin_time,
        "CreationTimeEnd": filter_by_end_time
    }
    logger.debug(f"enumerate slide entries with conditions: {params}.")
    response = requests.get(get_storage_index_files_api_url(),
                            params=params,
                            headers=headers)
    if response.status_code < 200 or response.status_code >= 300:
        raise Exception(
            f"Can not get slide entries, {response.reason} {response.content}")
    content = json.loads(response.content)
    return [SlideEntryDto(**item) for item in content]


def _api_request_permission_token(entry_id) -> str:
    if not entry_id:
        raise ValueError(f"Invalid empty entry id.")
    access_token = get_access_token()
    params = {"EntryId": entry_id}
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.post(get_storage_index_request_permission_token_api_url(),
                             params=params,
                             headers=headers)
    if response.status_code < 200 or response.status_code >= 300:
        raise Exception(
            f"Can not get slide indices, {response.reason} {response.content}")
    return response.content


def _api_get_file_entry_asset(entry_id,
                              asset_file_name,
                              permission_token) -> bytes:
    if not entry_id:
        raise ValueError("Invalid empty entry id.")
    if not asset_file_name:
        raise ValueError("Invalid empty asset file name.")
    if not permission_token:
        raise ValueError("Invalid empty permission token.")
    access_token = get_access_token()
    params = {
        "FileEntryId": entry_id,
        "AssetFileName": asset_file_name,
        "PermissionToken": permission_token
    }
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(get_asset_file_entry_api_url(),
                            params=params,
                            headers=headers)
    if response.status_code < 200 or response.status_code >= 300:
        raise Exception(
            f"Can not get slide entries, {response.reason} {response.content}")
    if len(response.content) == 0:
        return b''
    content = json.loads(response.content)
    return content['bytes']


def get_slide_entry_annotations(entry_id):
    '''
    Get the annotations of slide entry.

    Args:
        entry_id (str): the id of slide entry.

    Returns:
        annotations (list(AnnotationDto)): annotations.
    '''
    asset_annotations_name = "annotations"
    permission_token = _api_request_permission_token(entry_id)
    annotations_bytes = _api_get_file_entry_asset(entry_id,
                                                  asset_annotations_name,
                                                  permission_token)
    if len(annotations_bytes) == 0:
        return []
    annotation_json = json.loads(base64.b64decode(annotations_bytes))
    annotations = [_convert_annotation(item) for item in annotation_json]
    return annotations


def _convert_annotation(csharp_annotation: dict):
    tags = csharp_annotation['Tags']
    comments = csharp_annotation['Comments']
    shape_type = csharp_annotation['Shape']['$type']
    if 'PolygonShape' in shape_type:
        vertices = csharp_annotation['Shape']['Vertices']

        vertices = [[float(i) for i in v.split(',')] for v in vertices]

        return _convert_polygon_annotation(tags, comments, vertices)
    if 'RectangleShape' in shape_type \
            or 'ArrowShape' in shape_type:
        bounds = csharp_annotation['Shape']['Bounds']
        bounds = [int(item) for item in bounds.split(',')]
        return _convert_rectangle_annotation(tags, comments, bounds)
    if 'EllipseShape' in shape_type:
        bounds = csharp_annotation['Shape']['Bounds']
        bounds = [int(item) for item in bounds.split(',')]
        return _convert_ellipse_annotation(tags, comments, bounds)

    raise Exception(f"Unsupported annotation shape {shape_type}.")


def _convert_polygon_annotation(tags, comments, vertices):
    bounds = []
    min = np.amin(vertices, axis=0)
    max = np.amax(vertices, axis=0)
    location = min
    size = max - min
    bounds.extend(location)
    bounds.extend(size)
    return AnnotationDto(tags, comments, bounds, vertices)


def _convert_rectangle_annotation(tags, comments, bounds):
    vertices = []
    x = bounds[0]
    y = bounds[1]
    width = bounds[2]
    height = bounds[3]
    vertices.append((x, y))
    vertices.append((x+width, y))
    vertices.append((x+width, y+height))
    vertices.append((x, y+height))
    return AnnotationDto(tags, comments, bounds, vertices)


def _convert_ellipse_annotation(tags, comments, bounds):
    point_count = 16
    vertices = []
    location = np.array(bounds[:2])
    size = np.array(bounds[2:])
    center = size/2 + location

    for i in range(point_count):
        angle = math.pi * 2 * i/point_count
        vertice = center + \
            ((math.cos(angle), math.sin(angle)) * size/2).astype(int)
        vertices.append(list(vertice))

    return AnnotationDto(tags, comments, bounds, vertices)


def get_slide_entries(filter_by_path=None,
                      filter_by_name=None):
    '''
    Get the entries of slide.

    Args:
        filter_by_path (str): filter slide entries by path name.

        filter_by_name (str): filter slide entries by name.

    Rerturns:
        slide_entries (list(SlideEntryDto)): the slide entries.
    '''

    filter_by_begin_time = None
    filter_by_end_time = None
    return _api_organization_files(filter_by_path,
                                   filter_by_name,
                                   filter_by_begin_time,
                                   filter_by_end_time)


def get_distinct_slide_ids(**kwargs):
    '''
    Get the distinct slide ids.
    '''
    logger.info("enumerate distinct slide ids.")
    entries = get_slide_entries(**kwargs)
    storage_ids = [entry.StorageId for entry in entries if entry]
    return list(set(storage_ids))
