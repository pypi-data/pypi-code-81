# coding: utf-8
# ##########################################################################
#
# Copyright (c) 2016-2017 European Synchrotron Radiation Facility
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
# ###########################################################################

__authors__ = ["H. Payno"]
__license__ = "MIT"
__date__ = "17/05/2017"


import os
import logging
import shutil
from urllib.request import urlopen, ProxyHandler, build_opener

logger = logging.getLogger(__file__)
url_base = "http://www.edna-site.org/pub/est/"


def DownloadDataset(dataset, output_folder, timeout, unpack=False):
    # create if needed path scan
    url = url_base + dataset

    logger.info("Trying to download scan %s, timeout set to %ss", dataset, timeout)
    dictProxies = {}
    if "http_proxy" in os.environ:
        dictProxies["http"] = os.environ["http_proxy"]
        dictProxies["https"] = os.environ["http_proxy"]
    if "https_proxy" in os.environ:
        dictProxies["https"] = os.environ["https_proxy"]
    if dictProxies:
        proxy_handler = ProxyHandler(dictProxies)
        opener = build_opener(proxy_handler).open
    else:
        opener = urlopen
    logger.info("wget %s" % url)
    data = opener(url, data=None, timeout=timeout).read()
    logger.info("Image %s successfully downloaded." % dataset)

    if not os.path.isdir(output_folder):
        os.mkdir(output_folder)

    try:
        archive_folder = os.path.join(output_folder, os.path.basename(dataset))
        with open(archive_folder, "wb") as outfile:
            outfile.write(data)
    except IOError:
        raise IOError(
            "unable to write downloaded \
                        data to disk at %s"
            % archive_folder
        )

    if unpack is True:
        shutil.unpack_archive(archive_folder, extract_dir=output_folder, format="bztar")
        os.remove(archive_folder)


def extract_properties_from_dict(my_str) -> dict:
    """
    Convert parameters provided from a string to a dictionary.
    expected syntax is param1:value1,param2:value2
    would return { param1: value1, param2: value2 }
    try to cast each value to a number (float).
    """
    params = {}
    param_list = my_str.split(",")
    failures = []
    for param in param_list:
        try:
            param_name, param_value = param.split(":")
        except Exception as e:
            logger.info("Fail to cast some parameters: {}".format(e))
            failures.append(param)
        else:
            try:
                param_value = float(param_value)
            except Exception:
                pass
            params[param_name] = param_value
    if len(failures) > 0:
        logger.warning("Fail to convert some parameters : {}".format(failures))
    return params
