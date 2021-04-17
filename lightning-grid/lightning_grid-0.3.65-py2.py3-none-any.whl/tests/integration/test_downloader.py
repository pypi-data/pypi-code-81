from pathlib import Path

from grid.downloader import DownloadableObject
from grid.downloader import Downloader


def test_downloader_downloads_data(tmpdir):
    """Downloader().download() downloads data in nested directories."""
    # Google logo
    url = 'https://www.google.com/images/branding/googlelogo/2x/googlelogo_color_272x92dp.png'
    directory_path = 'nested_0/nested_1'
    filename = 'test-filename.png'
    objects = [DownloadableObject(url=url, download_path=directory_path, filename=filename)]

    # Download file
    D = Downloader(downloadable_objects=objects, base_dir=tmpdir)
    D.download()

    # Test that file as been downloaded.
    assert Path(tmpdir).joinpath(directory_path).joinpath(filename).exists()
