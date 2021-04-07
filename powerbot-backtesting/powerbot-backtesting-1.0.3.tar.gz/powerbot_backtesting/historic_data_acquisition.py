import json
import requests
import hashlib
from pathlib import Path
from datetime import datetime, timedelta
from zipfile import ZipFile, BadZipFile
from typing import List

from powerbot_backtesting.exceptions import ChecksumError
from powerbot_backtesting.utils.constants import *
from powerbot_backtesting.utils import _find_cache
from powerbot_backtesting.historic_data_processing import process_historic_data

try:
    from swagger_client.rest import ApiException
except ModuleNotFoundError:
    raise ModuleNotFoundError(
        "You need an up-to-date swagger client in the top level of your project directory to run this package!")

def get_historic_data(api_key: str,
                      exchange: str,
                      delivery_areas: List[str],
                      day_from: str,
                      day_to: str = None,
                      cache_path: Path = None,
                      extract_files: bool = False,
                      process_data: bool = False,
                      skip_on_error: bool = False):
    """
    Function loads all public data for specified days in the specified delivery area. Output is a zipped directory
    containing all files in JSON format. Optionally, zip file can be extracted automatically and processed to be
    compatible with other functions in the powerbot_backtesting package.

    Args:
        api_key (str): Specific history instance API key
        exchange (str): One of the following: epex, hupx, tge, nordpool, southpool
        delivery_areas (list): List of EIC Area Codes for Delivery Areas
        day_from (str): Datetime/ String in format YYYY-MM-DD
        day_to (str): Datetime/ String in format YYYY-MM-DD
        cache_path (Path): Optional path for caching files
        extract_files (bool): True if zipped files should be extracted automatically (Warning: immense size increase)
        process_data (bool): True if extracted files should be processed to resemble files loaded via API
        skip_on_error (bool): True if all dates that cannot possibly be loaded (e.g. due to lack of access rights) are
        skipped if the difference between day_from and day_to is at least 2 days

    Returns:
        List of loaded file paths
    """
    # Validity check
    if not isinstance(day_from, datetime):
        try:
            day_from = datetime.strptime(day_from, DATE_YMD)
        except ValueError:
            raise ValueError("day_from needs to be a date or a string in YYYY-MM-DD format")
    if day_to and not isinstance(day_to, datetime):
        try:
            day_to = datetime.strptime(day_to, DATE_YMD)
        except ValueError:
            raise ValueError("day_to needs to be a date or a string in YYYY-MM-DD format")

    delivery_areas = delivery_areas if isinstance(delivery_areas, list) else [delivery_areas]
    cache_path = _find_cache() if not cache_path else cache_path
    cache_path = Path(cache_path) if not isinstance(cache_path, Path) else cache_path
    headers = {"accept": "application/zip", "X-API-KEY": api_key}
    day_to = day_to if day_to else day_from
    skip_on_error = True if skip_on_error and day_to and day_to-day_from >= timedelta(days=2) else False

    zipfiles = []
    extracted_files = {}
    retry = 0

    while day_from <= day_to:
        prevent_update = False

        for del_area in delivery_areas:
            host = f"https://history.powerbot-trading.com/history/{exchange}/{del_area}/{day_from.strftime(DATE_YMD)}"

            # Filepath
            filepath = cache_path.joinpath(f"history/{exchange}_{del_area}/{day_from.strftime(DATE_YM)}")

            # File
            filename = f"{day_from.strftime(DATE_MD)}_public_data.zip"
            zipfiles.append(f"{del_area}_{filename.strip('.zip')}")

            # Skip if file exists
            if not filepath.joinpath(filename).exists() and not filepath.joinpath(day_from.strftime(DATE_MD)).exists():
                # Load file
                r = requests.get(host, headers=headers, stream=True)
                m = hashlib.sha256()

                if skip_on_error and r.status_code in [204, 403]:
                    continue
                if r.status_code == 503:
                    raise ApiException(status=503, reason="Service unavailable or API rate limit exceeded")
                if r.status_code == 404:
                    raise ApiException(status=404, reason=f"Data for '{day_from}' in {del_area} has not been exported yet")
                if r.status_code == 403:
                    raise ApiException(status=403, reason="Currently used API Key does not have access to this data")
                if r.status_code == 204:
                    raise ApiException(status=204, reason=f"There is no data for '{day_from}' in {del_area}")

                # Create filepath only if file is valid
                filepath.mkdir(parents=True, exist_ok=True)

                with open(filepath.joinpath(filename), 'wb') as fd:
                    for chunk in r.iter_content(chunk_size=128):
                        m.update(chunk)
                        fd.write(chunk)

                expected_hash = json.loads([i for i in requests.get(host+"/sha256", headers=headers, stream=True).iter_lines()][0])["sha_256"]

                if not expected_hash == m.hexdigest():
                    if retry < 3: # Retry 3 times
                        filepath.joinpath(filename).unlink(missing_ok=False)
                        retry += 1
                        prevent_update = True
                        continue
                    if skip_on_error: # Skip
                        filepath.joinpath(filename).unlink(missing_ok=False)
                    else:
                        filepath.joinpath(filename).unlink(missing_ok=False)
                        raise ChecksumError("Corrupted file: expected sha256 checksum does not match sha256 of received files. Please try again.")

            # Extraction
            if extract_files and not filepath.joinpath(day_from.strftime(DATE_MD)).exists():
                try:
                    with ZipFile(filepath.joinpath(filename), 'r') as zip:
                        zip.extractall(filepath.joinpath(day_from.strftime(DATE_MD)))
                    # Delete Zip
                    filepath.joinpath(filename).unlink()

                except BadZipFile:
                    raise TypeError(f"The created file for day '{day_from}' is faulty. Please try to load it again")

            if extract_files:
                # Add to dictionary
                extracted_files[f"{del_area}_{filename.strip('.zip')}"] = [str(e) for e in filepath.joinpath(day_from.strftime(DATE_MD)).iterdir() if e.is_file()]

            retry = 0
        day_from = day_from + timedelta(days=1) if not prevent_update else day_from

    if not zipfiles:
        return []
    if extract_files:
        if process_data:
            return process_historic_data(extracted_files, exchange)
        return extracted_files
    return zipfiles


def get_history_key_info(api_key: str):
    """
    Returns information for the specified History API Key

    Args:
        api_key (str): History API Key

    Returns:
        Dict
    """
    headers = {"accept": "application/json", "X-API-KEY": api_key}
    host = "https://history.powerbot-trading.com/api-key"

    r = requests.get(host, headers=headers, stream=True)

    if r.status_code == 503:
        raise ApiException(status=503, reason="Service unavailable or API rate limit exceeded")
    if r.status_code == 400:
        raise ApiException(status=400, reason="Request could not be processed, please check your API Key")
    return r.json()