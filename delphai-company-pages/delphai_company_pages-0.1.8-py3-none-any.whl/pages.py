from typing import List
from azure.storage.blob.aio import BlobClient, StorageStreamDownloader
from azure.core.exceptions import ResourceNotFoundError
from warcio.archiveiterator import ArchiveIterator
import os
from dataclasses import dataclass
import asyncio
import networkx as nx
from networkx.readwrite.json_graph import cytoscape_graph
import json

temp_dir = os.environ.get('TEMP_DIR') or '/tmp'


@dataclass
class Meta:
  _id: str
  name: str
  company_url: str
  redirected_url: str
  short_desc: str = None
  headquarters: str = None


@dataclass
class Page:
  target_url: str
  text: str


@dataclass
class Pages:
  info: str
  pages: List[Page]
  graph: nx.Graph
  meta: Meta


def process_pages(pages_file: str):
  pages: List[Page] = []
  with open(pages_file, 'rb') as stream_file:
    for record in ArchiveIterator(stream_file):
      if record.rec_type == 'warcinfo':
        info = record.raw_stream.read()
      elif record.rec_type == 'resource':
        text = record.content_stream().read().decode('utf-8')
        page = Page(target_url=record.rec_headers.get_header('WARC-Target-URI'), text=text)
        pages.append(page)
  return pages, info


def process_graph(graph_file: str):
  with open(graph_file, 'rb') as stream_file:
    json_data = json.load(stream_file)
  graph = cytoscape_graph(json_data)
  return graph


def process_meta(meta_file: str):
  with open(meta_file, 'rb') as stream_file:
    json_data = json.load(stream_file)
  meta = Meta(**json_data)
  return meta


async def download_file(connection_string: str, container: str, source: str, destination: str):
  blob = BlobClient.from_connection_string(connection_string, container, source)
  async with blob:
    stream: StorageStreamDownloader = await blob.download_blob()
    data = await stream.readall()
  dest_file = os.path.abspath(destination)
  with open(dest_file, 'wb') as stream_file:
    stream_file.write(data)
  return dest_file


async def get_pages(connection_string: str, container: str, domain: str) -> Pages:
  download_dir = f'{temp_dir}/{domain}'
  os.makedirs(download_dir, exist_ok=True)
  source_prefix = f'{domain}/{domain}'
  dest_prefix = f'{download_dir}/{domain}'

  files = {'pages': 'text.warc.gz', 'graph': 'graph.json', 'meta': 'meta.json'}

  tasks = []

  for key, suffix in files.items():
    task = download_file(connection_string, container, f'{source_prefix}-{suffix}', f'{dest_prefix}-{suffix}')
    tasks.append(task)
  pages_file, graph_file, meta_file = await asyncio.gather(*tasks, return_exceptions=True)
  pages, graph, info, meta = None, None, None, None
  if not isinstance(pages_file, ResourceNotFoundError):
    pages, info = process_pages(pages_file)
  if not isinstance(meta_file, ResourceNotFoundError):
    meta = process_meta(meta_file)
  if not isinstance(graph_file, ResourceNotFoundError):
    graph = process_graph(graph_file)
  return Pages(info, pages, graph, meta)