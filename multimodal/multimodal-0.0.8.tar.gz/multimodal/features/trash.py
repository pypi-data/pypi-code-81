
# def download_file(url, directory, filename=None):
#     local_filename = filename or get_basename(url)
#     output_path = os.path.join(directory, local_filename)
#     with DownloadProgressBar(
#         unit="B", unit_scale=True, miniters=1, desc=url.split("/")[-1]
#     ) as t:
#         urllib.request.urlretrieve(url, filename=output_path, reporthook=t.update_to)


# def download_file(url, directory, filename=None):
#     local_filename = filename or get_basename(url)
#     local_path = os.path.join(directory, local_filename)
#     with requests.get(url, stream=True) as r:
#         with open(local_path, "wb") as f:
#             shutil.copyfileobj(r.raw, f)
#     return local_path


# class Features:
#     def __init__(self, download_dir, url="https://"):
#         self.download_dir = download_dir
#         self.download_path = os.path.join(download_dir, "coco-bottom-up-36.zip")
#         self.url = url
#         if not os.path.exists(self.download_path):
#             self.download_zip()
#         self.zipfile = None  # lazy loading

#     def download_zip(self):
#         os.system(
#             "wget {url} {download_path}".format(
#                 url=self.url, download_path=self.download_path
#             )
#         )

#     def open_zipfile(self):
#         self.zipfipe = zipfile.ZipFile(self.download_path)

#     def get(self, image_name):
#         pass
