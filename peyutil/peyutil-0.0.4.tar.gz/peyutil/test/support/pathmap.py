#! /usr/bin/env python
"""Path mapping for various test resources."""
##############################################################################
#  Based on DendroPy Phylogenetic Computing Library.
#
#  Copyright 2010 Jeet Sukumaran and Mark T. Holder.
#  All rights reserved.
#
#  See "LICENSE.txt" for terms and conditions of usage.
#
#  If you use this work or any portion thereof in published work,
#  please cite it as:
#
#     Sukumaran, J. and M. T. Holder. 2010. DendroPy: a Python library
#     for phylogenetic computing. Bioinformatics 26: 1569-1571.
#
##############################################################################

try:
    import anyjson
except:
    # pylint: disable=attribute-defined-outside-init
    import json

    class Wrapper(object):
        """No-op class."""
        pass

    anyjson = Wrapper()
    anyjson.loads = json.loads
import codecs
import os
from peyutil import pretty_timestamp, write_as_json


class PathMapForTests(object):
    """Class with attributes that make it easy to find different types of testing data."""

    def __init__(self, path_map_filepath):
        """Uses the parent directory of `path_map_filepath` to find other testing dirs."""
        support_dir = os.path.dirname(path_map_filepath)
        self.tests_dir = os.path.join(support_dir, os.path.pardir)
        self.package_dir = os.path.join(self.tests_dir, os.path.pardir)
        self.scripts_dir = os.path.join(self.package_dir, os.path.pardir, "scripts")
        self.tests_data_dir = os.path.join(self.tests_dir, "data")
        self.tests_output_dir = os.path.join(self.tests_dir, "output")
        self.tests_scratch_dir = os.path.join(self.tests_dir, "scratch")

    def all_files(self, prefix):
        """Returns a set of filepaths to all test data."""
        d = os.path.join(self.tests_data_dir, prefix)
        s = set()
        for p in os.listdir(d):
            fp = os.path.join(d, p)
            if os.path.isfile(fp):
                s.add(fp)
        return s

    def nexson_obj(self, filename):
        """Returns a JSON load result from `filename` in the TESTS/data/nexson."""
        with self.nexson_file_obj(filename) as fo:
            fc = fo.read()
            return anyjson.loads(fc)

    def nexson_file_obj(self, filename):
        """Returns readable file object for testing NexSON in `filename`."""
        fp = self.nexson_source_path(filename=filename)
        return codecs.open(fp, mode='r', encoding='utf-8')

    def shared_test_dir(self):
        """Returns the fullpath to the shared-api-tests dir in the tests."""
        return os.path.join(self.tests_data_dir, "shared-api-tests")

    def nexson_source_path(self, filename=None):
        """Returns the fullpath for testing a NexSON in `filename`."""
        if filename is None:
            filename = ""
        return os.path.join(self.tests_data_dir, "nexson", filename)

    def nexml_source_path(self, filename=None):
        """Returns the fullpath for testing a NeXML in `filename`."""
        if filename is None:
            filename = ""
        return os.path.join(self.tests_data_dir, "nexml", filename)

    def named_output_stream(self, filename=None, suffix_timestamp=True):
        """Returns writable file stream of the file from a `named_ouput_path call`."""
        fp = self.named_output_path(filename=filename, suffix_timestamp=suffix_timestamp)
        return open(fp, "w")

    def named_output_path(self, filename=None, suffix_timestamp=True):
        """Returns a filepath to filename in the testing output dir.

        If `suffix_timestamp` is True, results of `pretty_timestamp` will
        be appended to the filename.
        """
        if filename is None:
            filename = ""
        else:
            if isinstance(filename, list):
                filename = os.path.sep.join(filename)
            if suffix_timestamp:
                filename = "%s.%s" % (filename, pretty_timestamp(style=1))
        if not os.path.exists(self.tests_output_dir):
            os.makedirs(self.tests_output_dir)
        return os.path.join(self.tests_output_dir, filename)

    def script_source_path(self, filename=None):
        """Returns the full path to a `filename` in the package's scripts dir."""
        if filename is None:
            filename = ""
        return os.path.join(self.scripts_dir, filename)

    def next_unique_scratch_filepath(self, fn):
        """Returns the full path to a scratch file starting with `fn` in the scratch dir."""
        frag = os.path.join(self.tests_scratch_dir, fn)
        if os.path.exists(self.tests_scratch_dir):
            if not os.path.isdir(self.tests_scratch_dir):
                mf = 'Cannot create temp file "{f}" because a file "{c}" is in the way'
                msg = mf.format(f=frag, c=self.tests_scratch_dir)
                raise RuntimeError(msg)
        else:
            os.makedirs(self.tests_scratch_dir)
        return self.next_unique_filepath(frag)

    def next_unique_filepath(self, fp):
        """Not thread safe! adds numeric suffix to `fp` until the path does not exist."""
        if os.path.exists(fp):
            ind = 0
            while True:
                np = '{f}.{i:d}'.format(f=fp, i=ind)
                if not os.path.exists(np):
                    return np
                ind += 1
        return fp

    def json_source_path(self, filename=None):
        """Returns the fullpath for testing a JSON in `filename`."""
        if filename is None:
            filename = ""
        return os.path.join(self.tests_data_dir, "json", filename)

    def collection_obj(self, filename):
        """Returns a JSON load result from `filename` in the collection test dir."""
        with self.collection_file_obj(filename) as fo:
            fc = fo.read()
            return anyjson.loads(fc)

    def collection_file_obj(self, filename):
        """Returns a readable file object from `collection_source_path` call."""
        fp = self.collection_source_path(filename=filename)
        return codecs.open(fp, mode='r', encoding='utf-8')

    def collection_source_path(self, filename=None):
        """Returns a absolute  filepath to `filename` in TESTS/data/colletions dir."""
        if filename is None:
            filename = ""
        return os.path.join(self.tests_data_dir, "collections", filename)

    def amendment_obj(self, filename):
        """Returns a JSON load result from `filename` in the amendments test dir."""
        with self.amendment_file_obj(filename) as fo:
            fc = fo.read()
            return anyjson.loads(fc)

    def amendment_file_obj(self, filename):
        """Returns a readable file object from `amendment_source_path` call."""
        fp = self.amendment_source_path(filename=filename)
        return codecs.open(fp, mode='r', encoding='utf-8')

    def amendment_source_path(self, filename=None):
        """Returns a absolute  filepath to `filename` in TESTS/data/amendments dir."""
        if filename is None:
            filename = ""
        return os.path.join(self.tests_data_dir, "amendments", filename)

    def equal_blob_check(self, unit_test, diff_file_tag, first, second):
        """Trips unit_test failure if `first` != `second` after writing diff files."""
        if first != second:
            # dd = DictDiff.create(first, second)
            ofn = self.next_unique_scratch_filepath(diff_file_tag + '.obtained_rt')
            efn = self.next_unique_scratch_filepath(diff_file_tag + '.expected_rt')
            write_as_json(first, ofn)
            write_as_json(second, efn)
            # er = dd.edits_expr()
            if first != second:
                m_fmt = "Conversion failed see files {o} and {e}"
                m = m_fmt.format(o=ofn, e=efn)
                unit_test.assertEqual("", m)


def get_test_path_mapper():
    """Factory for PathMapForTests object for the package."""
    return PathMapForTests(path_map_filepath=__file__)
