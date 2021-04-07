# file matrixb/matrix.py

# Copyright (c) 2019-2020 Kevin Crouse
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# @license: http://www.apache.org/licenses/LICENSE-2.0
# @author: Kevin Crouse (krcrouse@gmail.com)

import sys, os, re
import warnings
import datetime
import dateutil.parser
import copy

sys.path.insert(0,'../datacleaner')
import datacleaner
import matrixb
from .columnnormalizer import ColumnNormalizer
from .rowmap import MatrixRowmap
from .iterator import MatrixIterator

intre = re.compile(r'-?\d+$')
intfloatre = re.compile(r'-?\d+\.\0*$')
floatre = re.compile(r'-?\d*\.\d+$')

NoneType = type(None)

intdatere = re.compile(r'(\d\d\d\d)(\d\d)(\d\d)(\.0+)?$')
timere = re.compile(r'\s*(\d?\d)\:(\d\d)(\:(\d\d)(\.(\d+))?)?\s*(am|pm)$', re.I)

class Matrix(object):

    #-------------------------------------------------------------------------
    #
    #                        CLASS LEVEL VARIABLES/FUNCTIONS/PROPERTIES
    #
    #-------------------------------------------------------------------------


    def default_null_values(self=None):
        """list: The default null values - this is kept in function format that can be called in either class or object context, and can be easily extended in subclasses. """
        return(['NA', 'na', 'N/A', 'n/a', 'NULL', 'null', 'None', 'none', 'nan', 'NaN', '#N/A'])

    @classmethod
    def default_column_normalizer(self, shorthand_name=False):
        """ Provides an interface to a class-level column-normalizer, allowing for subclasses for common processes.  Defaults to matrixb.ColumnNormalizer, which translates to snake_case and replace almost all special characters to underscores (except for # or %).

            Args:
                shorthand_name: passed to the constructor of the matrixb.ColumnNormalizer to create a defualt set of normalization rules. Values are 'default' (removes all special characters except for [-, %, #] and converts to snake_case); 'conservative' (converts to snake case, preserving all special characters), 'ascii' (removes all non-alphanumeric and converts to snake_case). None indicates there should be no class-level column normalizer. Default to False, which should be interpreted as 'default'.
            Returns:
                The default column normalizer for the class, filtered by the shorthand name .
         """
        return(ColumnNormalizer(shorthand_name))

    #-------------------------------------------------------------------------
    #
    #                        CONSTRUCTOR
    #
    #-------------------------------------------------------------------------


    def __init__(self, source=None, columns=None, null_values=False, extra_null_values=None, indexed_columns=None, column_normalizer='default', columns_from_source=None, column_types=None, duplicate_column_policy='warning', recode_duplicates=True, rowcount_policy='error', autoclean=True, load_policy="lazy", data_cleaner=False):
        """
        Args:
            source (MatrixSource|list(list)|iterator, optional): The source for the matrix data. Expects a MatrixSource object, a primitive matrix that is a list of lists, or any iterator that returns a list as a row. Defaults to None.
            columns (list, optional): The list of raw column names, which will be normalized if column_normalizer is not None. Defaults to None.
            null_values (list, optional): A parameter to explicitly set the null values for the matrix object (see the null_values property for more information). Defaults to the class method, default_null_values.
            extra_null_values (list, optional): A list of additional cell values to be considered null, which will be added to the default set of null_values.
            column_normalizer (str|callable|object|None, optional). The details on how column names should be normalized, if at all. Can be any of the following. By default, the class-level default_column_normalizer() function will be called with the 'default' shorthand_name, and the result of this will be set as the object's column normalizer.
                None: Indicates no normalization should occur. Calls to the column_normalizer property will return None. Note that while no normalization will occur on column names, but strip() will still be applied to the column names.
                str: Use the string as the shorthand_name to pass to the class-level default_column_normalizer() function.
                Callable: A function that will be called on each column name to normalize it.
                Object: Any object must implement the DataCleaner interface, of which the clean function will be called on each column name.
            autoclean (bool, optional): If true, will clean every cell as loaded from the source using the object's data cleaner. Defaults to True.
            data_cleaner (object, optional): The object that cleans cell values when loaded (if autoclean is True). Defaults to datacleaner.DataCleaner.
            column_types (list|dict, optional): Specify the datatypes for specific columns, overriding the default datacleaner. Often used for numeric values that should be strings (like zipcodes) or to identify date, time, or other special column types. By default, no column constraints will be used and the matrix.datacleaner will determine the type. Parameter may be:
                    list(<datatype>): sets the data type for the columns in order, starting at the first column. The column_types list does not need to be equal to ncols - columns indexed higher than the typed list will use the default data cleaner, as will any None included within the index.
                    dict{column_name: <datatype>}|{column-number: <datatype>}: indicates specific columns and their respective datatype.
                    <datatype> can be: a python primitive types, date/time object (datetime.date, datetime.time, datetime.datetime), and 'maybeint' (allows for an int or string, but will raise an exception on other types or of the string appears to be another type).
            indexed_columns (list, optional): The initial list of columns to index. See documentation on indexing.
            columns_from_source (bool, optional): If True, the first row of the source will be used for the columns. Defers to the 'columns' parameter if defined, but defaults to True otherwise.
            duplicate_column_policy (enum('error', 'warning', 'ignore'), optional): Determines logging if duplicate column names are identified. If error, throws an exception. If warning, throws a warning. If ignore, continues without notification. Defaults to 'warning'
            recode_duplicates (bool, optional):
            rowcount_policy (['error', 'warning', 'ignore'], optional): Indicates how to handle situations in which a source row has a different number of cells than the number of columns. An exception is thrown on 'error', a warning is thrown on 'warning', and the row is silently accepted on 'ignore'. If the length of the row is longer than the length of the headers in 'warning' and 'ignore', the row will be truncated at the header length to preserve the squareness of the matrix.  Defaults to 'error'.
            load_policy
        """

        self._matrix = []
        self._columns = None
        self._colmap = None
        self._column_validators = None
        self.rows_loaded = 0
        self._loaded = False
        self._nextrowraw = None
        self._ncolumns = None
        self._indexed_columns = []
        self._indices = {}
        self._index_attributes = {}

        # for some cases, we use a default of False to mean "use a default value/object/setting" because None should explicitly mean "don't enact this feature"

        if data_cleaner:
            self._data_cleaner = data_cleaner
        elif data_cleaner == False:
            # default data cleaner
            self._data_cleaner = datacleaner.DataCleaner(null_values=null_values)
        else:
            self._data_cleaner = datacleaner.DataCleaner(
                null_values=null_values,
                transliterations=None,
                translations=None,
                convert_numbers=False,
            )

        # Add null value to the data cleaner.
        # If the construct parameter for null_values is False, it indicates that the default set of values should be used (which can be overriden in subclasses).
        if null_values is False:
            self._data_cleaner.add_null_values(self.default_null_values())
        if extra_null_values:
            self._data_cleaner.add_null_values(extra_null_values)

        #
        # Handle the column normalier
        #)
        if column_normalizer is None:
            # explicitly set to None, use the empty data cleaner that just strips preceeding and trailing whitespace
            self._column_normalizer = None
        elif type(column_normalizer) is str:
            # if string, pass it along to the default column normalizer setup
            self._column_normalizer = self.default_column_normalizer(column_normalizer)
        else:
            # Otherwise, the column normalizer must be an object that defines clean() or a function that will be called directly.
            self._column_normalizer = column_normalizer

        self._recode_duplicates = recode_duplicates
        if duplicate_column_policy not in ('error', 'warning', 'ignore'):
            raise Exception("duplicate_column_policy must be one of the following: ('error', 'warning', 'ignore')")
        self.duplicate_column_policy = duplicate_column_policy
        self.rowcount_policy = rowcount_policy
        self._autoclean = autoclean
        if load_policy not in ('lazy', 'manual', 'init'):
            raise Exception("Error on Matrix initialization: load_policy '"+load_policy+"' is not valid. Must be auto, deferred, or init")
        self._load_policy = load_policy


        #
        # Set up the source object. If it is a list, assume it is a resident list of lists and shortcut the source manipulation.
        #
        if source is None:
            self.source = None
            self._loaded = True
        elif type(source) is str:
            # --- filename. Identify the extension and load the source
            source_cls = matrixb.source.find_source_class(filename=source)
            if not source_cls:
                raise Exception("Extension " + ext + " does not have a known (and loaded) matrixb source")

            self.source = source_cls(source)
        else:
            self._loaded = False
            if type(source) is list:
                self.source = matrixb.source.Resident(source)
            else:
                self.source = source


        #
        # Set up columns
        #
        # If columns from source, set the unstandardized column list from the first row of the source
        if columns:
            self.columns = columns
        elif self.source:
            if columns_from_source or columns_from_source is None:
                try:
                    self.columns = next(self.source)
                except StopIteration:
                    # source is completely empty
                    self.columns = []
            else:
                self.columns = []

        if indexed_columns:
            for col in self.indexed_columns:
                self.index_column(col)

        # move parameters to simple instance variables.
        self.column_types = column_types

        # if requested to pre-load, do it now
        if load_policy == 'init':
            self.load()


    #-------------------------------------------------------------------------
    #
    #                        PROPERTIES
    #
    #-------------------------------------------------------------------------


    @property
    def column_normalizer(self):
        """ The column normalizer for this object."""
        return(self._column_normalizer)

    @property
    def loaded(self):
        """bool: indicates whether the MatrixSource has been processed through to completion. If the source is empty or null, loaded is true. """

        # if we haven't even attempted to load a row, we should check to make sure this isn't an empty source, which we can do by calling has_next
        if self._loaded == False and self._nextrowraw is None:
            self.has_next()

        return(self._loaded)

    @property
    def nrows(self):
        """int: The number of rows in the matrix. Raises an exception if the matrix has no data. Note that this requires the matrix to be entirely loaded and calls load implicitly. """
        self.load(automated=True)
        return(len(self))

    @property
    def ncolumns(self):
        """int: the number of columns in the matrix. Returns 0 if the matrix has no data and columns have not been defined. """
        # previously threw an error if empty, but that doesn't seem right.
        #raise Exception("Cannot call ncolumns if there is no matrix data.")
        return(self._ncolumns)

    @property
    def column_types(self):
        """dict(int => type): Column Types map the Column Index to the type that the column must be. At present, None is coded as null and is valid, regardless of the type. """
        return(self._column_types)

    @column_types.setter
    def column_types(self, column_types):
        if self.rows_loaded:
            raise Exception("At present, you cannot reset the column types after data has been loaded. This would require reanalysis of existing data, which is not implemented.")

        if type(column_types) is list:
            # okay, easy. just map the index to the type
            if len(column_types) > len(self.columns):
                raise Exception("list provided for column_types exceeds the number of columns for which types are being provided")
            self._column_types = {i: column_types[i] for i in range(len(column_types))}
        elif type(column_types) is dict:
            are_indices = True
            for key in column_types:
                if type(key) is not int or key >= len(self.columns):
                    are_indices = False
                    break

            if are_indices:
                # already in column index: validator type
                self._column_types = column_types
            else:
                self._column_types = {self.colmap[key]: column_types[key] for key in column_types}
        elif column_types is None:
            self._column_types = {}
        else:
            raise Exception("column types attempted to be set as an invaid format/object")

        # require a rebuild of the validators on the next load call
        self._column_validators = None

    @property
    def column_validators(self):
        """list: An array of length(columns) that provides closures to validate the values when rows are
        added, processed, or appended AND either autoclean is on or clean is stated explicitly.

        This uses the column_types parameter to create column-specific closures, and uses
        the default_datacleaner for anything else. Typechecking happens *after* null_values are
        processed, which may have implications for custom or sophisticated checking.
        """
        if self._column_validators:
            return(self._column_validators)

        if self._data_cleaner:
            default_cleaner =  self._data_cleaner.clean
        else:
            # just strip
            default_cleaner = lambda val: None if val is None else val.strip() if type(val) is str else val

        self._column_validators = []
        if not self.ncolumns:
            self._column_validators = lambda val: default_cleaner(val)
            return(self._column_validators)
        icol = 0
        for icol in range(self.ncolumns):
            typechecker = None
            if icol in self.column_types:
                coltype = self.column_types[icol]
                if type(coltype) in (type, str):
                    typechecker = self._typechecker(coltype)
                elif callable(coltype):
                    typechecker = self._lambdaclosure(coltype)
                else:
                    raise Exception("Column '"+str(self.columns[icol])+"' is specified to have column type '"+str(coltype)+"', but this does not have a defined parser in the datacleaner.")
            else:
                # No column type explicitly defined, so we use the default processing
                typechecker = default_cleaner

            self._column_validators.append(typechecker)
        return(self._column_validators)

    @property
    def indexed_columns(self):
        """list: A list of indexed columns. Indexed columns maintain a hash of the values in the columns to all of the row indices that the value relates to, to faciliate fast lookups when the dataset is large enough that the time to look up is a speed-performance concern. Indexing requires the entire dataset to be loaded into memory (and will do so on the first lookup) and so it is inconsistent with delayed load or non-resident implementations. The user cannot set the indexed_columns after initialization because of the level of processing involved. Instead, they should use the index functions to manipulate this list (e//e.g., index_column)."""
        return(self._indexed_columns)

    @property
    def columns(self):
        """list|none: The column names for the matrix, after they have been normalized."""
        if self._columns is None:
            return(None)
        return(self._columns.copy())

    @columns.setter
    def columns(self, new_columns, override=False):
        """Sets or resets the column names for this matrix.

        Args:
            new_columns (list): A list of raw column headers for this matrix. This list will be normalized given the present column_normalizer.
            override (bool): If the matrix or column headers have already been defined, it is expected that new_columns will have the same number of items as the old set of columns, and an exception is thrown otherwise. If override if true, no exception is thrown. Further, if the new set of columns is greater than the old set, the existing matrix will be extended to account for it. If the new set of columns is smaller than the old set, then the columns will be extended with blank headers to accommodate it.  Default is False.

        Raises:
            IndexError if override is False, the matrix already has ncolumns set, and the number of columns in new_columns is not equaly to ncolumns.
            """
        if self.columns is not None or self._matrix:
            print("Cols:", self.columns)
            print("m:", self._matrix)
            print("New cols:", new_columns)
            if len(new_columns) != self.ncolumns:
                if not override:
                    raise IndexError("When resetting column names, the new set of columns must have exactly the same number of columns as the old set, unless explicitly overriden")
                elif len(new_columns) < self.ncolumns:
                    # extend new_columns to match the length
                    new_columns = new_columns + [None] * (self.ncolumns - len(new_columns))
                else:
                    # extend the matrix
                    self.add_columns([None] * (self.ncolumns - len(new_columns)))

        self._render_columns(new_columns)

        # reindex the columns if there were some indices
        if self.indexed_columns:
            for col in self.indexed_columns:
                self.index_column(col)

    @property
    def colmap(self):
        """ dict: a hash that maps the normalized column name to the 0-based index of the column.

        Raises:
            Exception if a duplicate column is found and the recode_duplicates property is True, as this should have been translated in the _render_columns function, or the programmer should have taken strides to add/change a non-duplicated column name. If this exception is thrown, it probably means the programmer changed the column name manually. """
        if self._colmap is None:
            self._colmap = {}
            for i, column in enumerate(self.columns):
                if column in self._colmap:
                    if type(self._colmap[column]) is list:
                        # add it to already existing bucket
                        self._colmap[column].append(i)
                    elif not self.recode_duplicates:
                        # we convert colmap to an array and add this index as the second entry.
                        self._colmap[column] = [ self._colmap[column], i ]
                    else:
                        raise Exception("Found duplicate columns names '"+str(column)+"', but recode_duplicates is True, and so these should have been recoded previously")
                else:
                    self._colmap[column] = i
        return(self._colmap)

    @property
    def autoclean(self):
        """bool: Returns indicates whether data rows will be cleaned as loaded."""
        return(self._autoclean)

    @property
    def data_cleaner(self):
        """ The data-cleaner object used to clean cell values. """
        return(self._data_cleaner)

    @property
    def null_values(self):
        """ null_values (list) : A list of values that should be translated to None if encountered wholly in a cell, especially used to automatically convert variants of null/blank/empty cells to consisently be None when processing via Python. To add null values after object creation, use the function add_null_values(). Delegates to the data cleaner; if there is no data cleaner, empty list is returned."""
        if self.data_cleaner:
            return(self.data_cleaner.null_values)
        return([])

    @property
    def recode_duplicates(self):
        """bool: Returns whether duplicate column names are recoded or not. If True, duplicate column names will have the actual names recoded with an iterator (e.g., columns ['A', 'B', 'B'] -> ['A', 'B.1', 'B.2'] and the colmap is {'A': 0, 'B.1': 1, 'B.2': 2, }). If false, the colmap property will point to an array of column indexes for columns with duplicate names, and any calls to rowmap() will include an ordered array of all of the values, but all non-duplicated columns will continue to be a direct map of column name to value (e.g., columns ['A', 'B', 'B'] remain as they are, but colmap becomes {'A': 0, 'B': [1,2], }). Defaults to True."""
        return(self._recode_duplicates)

    @property
    def rowcount_policy(self):
        """rowcount_policy: enum of {'error', 'warning', 'ignore'/None, 'accommodate'}. Policy for any matrix data line (that is not empty) that exceeds the number of elements in the header. Defaults to 'error'
            None/'ignore': the row is spliced down to the column length, appended to the matrix, and processing continue.
            'error': raises exception to note that the row has more values than the number of columns.
            'warning': call warnings.warn for any row that exceeds the column length, chop off the extraneous values, and continue
            'accommodate': dynamically extend the matrix to accommodate extra columns if discovered during processing. This will add new column elements that are blank and extend the existing matrix to account for them. This is not an efficient process. """
        return(self._rowcount_policy)

    @rowcount_policy.setter
    def rowcount_policy(self, value):
        valid_policies = (None, 'ignore', 'error', 'warning', 'accommodate')
        if value not in valid_policies:
            raise Exception("Rowcount policy must be one of " + str(valid_policies))
        self._rowcount_policy = value

    @property
    def load_policy(self):
        """enum('lazy', 'deferred', 'init'): When data is loaded from the source. Defaults to "lazy".
            'lazy': Each row of data is loaded when the next row is referenced or when a function that requires all data to return the correct result is called. All matrix sources are assumed to be serial data sources (as with a file), and so if a future row is referenced before the intermediary rows have been loaded, all rows between the presently loaded row and the referenced row will be loaded.
            'init': All data is loaded when the object is initialized or when the source is added.
            'manual': Each row is loaded only when the programmer explicitly calls load() or load_next(). If a function is called that requires all data, an exception is thrown."""
        return(self._load_policy)

    #-------------------------------------------------------------------------
    #
    #                        PUBLIC FUNCTIONS
    #
    #-------------------------------------------------------------------------

    def rowmap(self):
        """ returns a MatrixRowmap object that is a derivative of this matrix """
        # return an array of hashes of columns:value
        return(MatrixRowmap(self))

    def rowmap_list(self):
        """ returns a list of rowmaps """
        result = []
        for row in self._matrix:
            result.append({ self.columns[i]:row[i] for i in range(len(self.columns)) })
        return(result)

    def delete_index(self, column):
        """ Deletes the index associated with the column.

        Args:
            column (str|int): The column to delete.  This can be one of the following:
                int : the index of the column
                str: uses the colmap to determine the column location
        """

        if type(column) is int:
            index = column
        else:
            index = self.colmap[column]
        del self._indexed_columns[self._indexed_columns.index(index)]
        del self._indicies[index]
        del self._index_attributes[index]

    def index_column(self, column, ignore_null=False, unique=False):
        """ create and maintain an index to specific columns to be used with lookup() later. Note that this will greatly increase the speed to look up specific values in the columns, but it does require the entire matrix to be loaded before a lookup() can occur. So index/lookup and deferred load/storage are essentially mutually exclusive.

        Args:
            column (str|int|dict): The column definition about which to maintain the index.  This can be one of the following:
                str: uses the colmap to determine the column location
                int : expected to be the index of the column
                dict of {'type':'column_name', 'value': column_name_var} : if you have non-string column names, this should be your format
        """
        icol = self._parse_column_definition(column)
        if icol is None:
            raise Exception("Matrix does not have column "+str(column)+" to index")
        if icol in self.indexed_columns:
            warnings.warn("Column " + str(icol) + " is already indexed")
            return
        self._indexed_columns.append(icol)
        self._indices[icol] = {}
        self._index_attributes[icol] = {'ignore_null': ignore_null, 'unique': unique}
        if not self._matrix:
            return

        for i in range(0, len(self._matrix)):
            self._index_value(i, icol, self._matrix[i][icol])

    def lookup(self, column, value):
        '''
        Lookup a value in a column index. This column must have been previously indexed.

        Params:
            column {str|int|dict}: the column, column-name, or column-defintion for the index to be searched. See the index_column() function for a description of the column-definition dict.
        '''

        icol = self._parse_column_definition(column)
        if icol not in self._indices:
            raise Exception("Matrix does not have an index on column "+column)

        if value in self._indices[icol]:
            return(self._indices[icol][value])
        return(None)

    def set_column_type(self, column, column_type):
        """ sets the column type for a listed column, after the instatiation of the object but before any rows have been loaded. At present, it does not retroactively check column values (and throws an error).

        Args:
            column (int|str): the column index or name in question.
            column_type (type|class|'maybeint'): the required type for the column.

        TODO:
            Update to retroactively apply to values after some rows have been loaded.
        """

        if self.rows_loaded:
            raise Exception("At present, you cannot reset the column types after data has been loaded. This would require reanalysis of existing data, which is not implemented.")

        if type(column) is int and column < len(self.columns):
            self._column_types[column] = column_type
        else:
            self._column_types[ self.colmap[column] ] = column_type

        self._column_validators = None

    def add_columns(self, n=None, columns=None):
        """ Add one or more columns to the end of the current matrix. It will retroactively add null values to existing rows.

        Args:
            n (int, optional): The number of columns to add. If n is used and the 'columns' arg is not, the columns will have no name. Either 'n' or 'columns' is required.
            columns(list[str], optional): The names of the new columns to add. Either 'n' or 'columns' is required.
        """

        if n is None and columns is None:
            raise Exception("add_columns reqires either parameter n or columns to be provided")
        elif n is not None and columns is not None and len(columns) != n:
            raise Exception(f"User specified adding {n} columns but provided {len(columns)} names: {columns}")

        if columns is None:
            columns = [None] * n

        # if there are no columns, we only permit adding columns if there is no data
        if not self.columns:
            if self.rows_loaded:
                raise Exception("Cannot add column names to a non-empty matrix that does not have column names set for the current columns. Set current columns first.")
            # matrix is empty, so just set the columns as the column names
            self._columns = columns
            self._ncolumns += len(columns)
            return

        for newcol in columns:
            if newcol in self._columns:
                raise Exception("Cannot add a new column with the same name as an existing one")

        self._columns += columns
        self._ncolumns += len(columns)
        self._colmap = None # recalc

        # now get the actual matrix that is in existance to be square
        extra = [None] * len(columns)
        for row in self._matrix:
            row.extend(extra.copy())


    def delete_column(self, *column):
        """Deletes the column from the matrix. Also deletes any related index and updates the colmap appropriately.

        Args:
            column (int|str): The reference to the column to delete. If an integer, uses it as the column index. If a string, looks up the index in the colmap. For convenience, will take multiple column values if provided.
        """
        for col in column:
            if type(col) is int:
                index = col
            else:
                index = self.colmap[col]

            if index in self._indices:
                self.delete_index(index)

            self.load()
            del self._columns[index]
            for row in self._matrix:
                del row[index]
        self._colmap = None
        self._ncolumns = len(self._columns)


    def rename_column(self, column, column_name):
        """Rename one or more columns and updates secondary data structures appropriately. Safer than manually renaming the column using self.columns[i] = X

        Args:
            column (int|str): The column to rename. If an integer, uses it as the column index. If a string, looks up the index in the colmap.
            column_name (int|str|None): The new name of the column.
        Raises:
            Exception if column_name already exists in the list of columns and recode_duplicates is True. This function does not auto-recode duplicate names.
        """
        if type(column) is int:
            index = column
        else:
            index = self.colmap[column]

        if column_name in self.columns and self.recode_duplicates:
            if column_name == self._columns[index]:
                # they renamed the column to itself.. Ignore.
                return
            raise Exception("Attempted to rename a column to a name that duplicates another column. This is not allowed if self.recode_duplicates is True.")

        oldname = self._columns[index]
        self._columns[index] = column_name
        self._colmap = None # clear the colmap so it will be rebuilt

        # remap the index if it exists
        if oldname in self._indices:
            self._indices[newname] = self._indices[oldname]
            del self._indices[oldname]

    def copy(self, conditions=None):
        """Copy the current matrix by value, so that changes to the copy do not affect the data structure of the present. Note that this will be very memory intensive for very large matrices.

        Args:
            condtions (list[dict],optional): An optional set of conditions or functions to apply during the copy. For each row, if any condition is false, the row will not be included. Each condition may be defined with the following key-value arguments:
                column (str): the column name to apply the condition to.
                value: a value that will be compared to the value in the listed column.
                function (str, optional): a specific type of function for the comparison. At present, only 're' and 'eq' are supported. For 'eq', it is a test of equality. For 're', it is a regular expression search based on value.

        Returns:
            The copy of the matrix.
        """

        mbcopy = Matrix()
        mbcopy.__dict__ = copy.deepcopy(self.__dict__)

        if not conditions:
            return(mbcopy)

        # now manage conditions
        if type(conditions) is dict:
            conditions = [ conditions ]
        # determine the functions to apply to each row
        functions = []
        for cond in conditions:
            col = mbcopy.colmap[cond['column']]
            if 'function' not in cond or cond['function'] == 'eq':
                func = lambda row: True if row[col] == cond['value'] else False
            elif cond['function'] == 're':
                func = lambda row: True if re.search(cond['value'], row[col]) else False
            else:
                raise Exception('Matrix copy does not undestand conditional function' + cond['function'])
            functions.append(func)

        # now create the new matrix and iterate over the old
        newmatrix = []
        for row in self._matrix:
            skip=False
            for f in functions:
                if not f(row):
                    skip=True
                    break
            # this row is legit
            if not skip:
                newmatrix.append(row.copy())

        mbcopy._matrix = newmatrix

        # now reindex
        for col in self._indices:
            # this is naive - eventually needs to handle unique and other parameters
            mbcopy.index_column(col, **self._index_attributes[col])

        #! return
        return(mbcopy)

    def load(self, automated=False):
        """ Immediately loads all data from the matrix source into the internal data.

        Args:
            automated(bool): Indicates whether this is an 'automated,' i.e. when this occurs as an automated fashion as a side effect of another call (such as nrows). The automated argument is only important if the load_policy is 'manual', when an automated load will throw an error. Default to False (so that the user calling matrixb.load() manually works as expected).

        Raises:
            Exception when the load_policy is 'manual' and 'automated' is True. This is provided so a user can explicitly prevent a load of the mull matrix from the source, such as when the user wishes to prevent a side effect of a full load when the source is too large for the available memory our would take too long for the intended time-to-process of the broader program.
        """

        if self.loaded:
            return

        if automated and self.load_policy == 'manual':
            raise Exception("call to matrixb function requiring fully loaded matrix on an instance that has not been fully loaded, and load_policy is 'manual'")

        try:
            while self.load_next():
                pass
        except StopIteration:
            pass

    def has_next(self):
        """
        Returns:
            True if there is a next row to be loaded.
            False if there is no next row to be loaded.
            None if there is no source, so that implicit tests will evaluate the same as False for Resident matrices.

        Note:
            If no rows have been loaded, this will load the first row and place it in the private variable representing the next row. This may therefore create a side effect if there is a possibility that the source is not initialized to the point of serving out the first row.

        Development Note:
            2. I'm not certain that this shouldn't be a function of the source class and be delegated there.
        """
        if not self.source:
            return(None)

        if self._nextrowraw is None:
            if self.rows_loaded == 0:
                try:
                    self._nextrowraw = next(self.source)
                except StopIteration:
                    self._loaded = True
                    return(False)
            else:
                raise Exception("It should not be possible for the cached next raw row to be None if the source is partially loaded")


        if self.loaded:
            return(False)

        return(True)

    def load_next(self):
        """ Loads the next row from source and processes it, updates the 'loaded' property when complete.

        Returns:
            The parsed, next row.

        Raises:
            StopItration if the source has been exhausted / fully loaded.
         """
        #
        # Note: We implement a 1-row lookahead so that (a) the loaded property returns True after the last row is loaded and without the need to attempt to load a non-existant row, and (b) we can efficiently implement has_next().
        #
        # Were we ever to attempt to adapt matrixb to use a live source in which the next row may not be ready,
        # this approach will need to be modified or subclassed.

        if self.loaded or not self.source:
            raise StopIteration

        if self._nextrowraw is None:
            # this is the first attempt to load a row (invariant: _nextrowraw is null and loaded is False only when (a) now rows have been loaded, (b) the first row has not be pre-intialized via has_next()).
            # Since has_next() will preinit the row and set loaded should there be no row, we just call that
            if not self.has_next():
                raise StopIteration

        current_raw = self._nextrowraw
        try:
            self._nextrowraw = next(self.source)
        except StopIteration:
            # if we catch the StopIteration here, that means there is no *next* row -- not that there is no
            # current row!
            self._loaded = True
            self._nextrowraw = False
        return(self._addrow(current_raw))


    def load_to(self, key):
        """ Loads the source to the ith element.

        Args:
            key (int): The index to which the source should be loaded.
        Returns:
            The row of the matrix at location key (base-0).
        Raises:
            IndexError if key is greater than the length of the source.
         """
        if self.rows_loaded > key:
            return(self._matrix[key])

        if self.loaded:
            raise IndexError("Requested to load list element " + str(key) + ", but matrixb source has only " + str(len(self)) + " elements")

        while self.rows_loaded <= key:
            try:
                row = self.load_next()
            except StopIteration:
                raise IndexError("Requested to load list element " + str(key) + ", but matrixb source has only " + str(len(self)) + " elements")
        return(row)

    #-------------------------------------------------------------------------
    #
    #                        EXPORT / OUTPUT / CAST FUNCTIONS
    #
    #-------------------------------------------------------------------------

    def export(self, filename, topmatter=None, autosize=False):
        """ Export to file. Will ascertain from the extension.

        Args:
            filename {str}: The filename
            topmatter {scalar|list(list)}: either details to be placed in the top cell or a matrix to be places above the table. empty rows of the matrix will be interpretted as blank lines.
            autosize {bool}: Attempt to autosize columns for formats that support it (excel). This can be timeconsuming. Defaults to false. NOT IMPLEMENTED YET.
        """
        self.load(automated=True)
        filename = os.path.expanduser(filename)
        source_cls = matrixb.source.find_source_class(filename=filename)
        if not source_cls:
            raise Exception("Cannot identify a valid source module for file " + filename)
        return(source_cls.export_to(self, filename, topmatter=topmatter, autosize=autosize))

    def dataframe(self):
        # return a dict of column_name -> array of values
        result = {}
        for col in self.columns:
            result[col] = []

        colrange = range(0, len(self.columns))
        for row in self:
            for i in colrange:
                result[self.columns[i]].append(row[i])

        return(result)

    def to_dataframe(self):
        """Export the matrix data into a Pandas DataFarme """
        import pandas as pd
        df = {col:[] for col in self.columns}
        collist = range(len(self.columns))
        cols = self.columns
        for row in self:
            for col in collist:
                df[cols[col]].append(row[col])
        return pd.DataFrame(df, columns=cols)

    def print_csv(self):
        """ Print data in a comma separated format to standard output. Quote strings iff they contain questionable characters """

        badchar = re.compile(r'[,\n\r\"]')
        quotechar = re.compile(r'"')

        print(",".join([ self._print_cell(colname) for colname in self.columns]))
        for row in self:
            print(",".join([ '' if x is None else x if type(x) is not str else '"' + quotechar.sub('""', x) + '"' if badchar.search(x) else x for x in row]))
        print("")

    #-------------------------------------------------------------------------
    #
    #                        ARRAY INFERFACE FUNCTIONS
    #
    #-------------------------------------------------------------------------
    # The following provide for the matrixb object to behave like a native array matrix, so users can replace former native arrays of arrays with a matrixb and expect code to work as previously.

    def iter(self):
        """ returns an iterator of the rows of the matrix """
        return(MatrixIterator(self))

    def __getitem__(self, key):
        """ Implements array item get. """
        if type(key) is not int:
            raise TypeError("matrixb index values must be integers, call to matrix['"+str(key)+"'] fails.")
        return(self.load_to(key))


    def __setitem__(self, key, row):
        """ Implements array item set. """
        # must be an entire row
        if type(row) is not list or len(row) != len(self.columns):
            raise Exception("setting a matrixb row must be exactly the length of the number of columns")
        self.load_to(key)
        self._matrix[key] = row
        if self.indexed_columns:
            raise Exception("TODO: alter indices for set")

    def __delitem__(self, key):
        """ Implements array item delete. """
        self.load_to(key)
        del self._matrix[key]
        self.rows_loaded -= 1
        if self.indexed_columns:
            raise Exception("TODO: alter indices for deleting")

    def __len__(self):
        """Implements array length. Note that this requires the entire source to be loaded."""
        self.load(automated=True)
        return(self.rows_loaded)

    def _addrow(self, row, key=None):
        """ This is the internal/private function via which any row goes onto the matrix. This function should funnel from both the processing of original matrix sources as well as manipulations to matrices after they've been loaded.

        Args:
            row (list): The new row to be appended/inserted. The row will be cleaned if autoclean is True, tested to see if the cleaned value is in the list of null_values, checked against the expected row-length (and if len(row) != obj.ncolumns, action is taken based on the rowcount_policy), and the row is indexed based on any indexed_columns.
            key (int, optional): The index at which to insert the row. Default is appended to the end.
        Returns:
            list: the cleaned/processed row.
        Raises:
            IndexError if len(row) > self.ncolumns, conditional on the rowcount policy.
            TypeError if row is not a list or tuple
        """
        if type(row) is not list:
            if type(row) is tuple:
                row = list(row)
            else:
                raise TypeError("Row to be added to the matrix is not a list or tuple: " + str(row))

        if self.autoclean:
            row = self.clean(row)
        elif self.null_values:
            for i, val in enumerate(row):
                if val in self.null_values:
                    row[i] = None

        # verify length
        if self.ncolumns is None:
            # -- this better be the first row. Set the number of columns based on it
            if self.rows_loaded:
                raise Exception("Internal state is wrong: ncolumns have not been set and there is matrix data already.")
            self._ncolumns = len(row)
        else:
            if len(row) != self.ncolumns and self.rowcount_policy:
                if len(row) > self.ncolumns:
                    if self.rowcount_policy != 'accommodate':
                        raise IndexError("Row " + str(self.rows_loaded) + " in source has more values than defined columns")
                    else:
                        # in this case, we extend the entire matrix dynamically to accommodate
                        # the new size
                        self.add_columns(n=(len(row) - self.ncolumns))
                elif len(row) < self.ncolumns:
                    row.extend([None] * (self.ncolumns - len(row)))

            if self.indexed_columns:
                if key:
                    raise Exception("TOOD: Allow for reindexing when adding a new row that is not at the end")
                for icol in self.indexed_columns:
                    self._index_values(len(self._matrix), icol, row[icol])

        if key is None:
            self._matrix.append(row)
        else:
            self._matrix.insert(key, row)
        self.rows_loaded += 1
        return(row)

    def append(self, row):
        """Adds the row to the end of the matrix (entire source will be loaded if not already done)"""
        if type(row) not in (list, tuple,):
            raise TypeError("Can only append a list/tuple to a matrix")
        self.load(automated=True)
        # we copy the row to avoid side-effects if the users wishes to manipulate it separately
        self._addrow(row.copy())

    def extend(self, rows):
        """Extends the matrix with the rows (entire source will be loaded if not already done)"""
        self.load(automated=True)
        for row in rows:
            if type(row) not in (list, tuple,):
                raise TypeError("Can only append a list/tuple to a matrix")
            # we copy the row to avoid side-effects if the users wishes to manipulate it separately
            self._addrow(row.copy())

    def insert(self, key, row):
        """Inserts the row parameter into the matrix at location 'key' (source will be loaded to the ith position if not already done).

        Args:
            key (int): the index at which point to insert the new row.
            row (array): the new row to insert. This needs to conform to all other row expectations - it must be the same width as the matrix (or the rowcount_policy needs to be set accordingly)
        """
        # NOTE: Ensure that this does not impact the planned future addition of keeping track of the original row index in the source.
        if type(row) not in (list, tuple,):
            raise TypeError("Can only append a list/tuple to a matrix")
        self.load_to(key)
        # we copy the row to avoid side-effects if the users wishes to manipulate it separately
        self._addrow(row.copy(), key=key)

    def pop(self, key=None):
        """ An implementation of array pop for the matrix. """
        if key is None:
            # get the last row
            key = self.nrows - 1
        self.load_to(key)
        self._matrix.pop(key)
        self.rows_loaded -= 1
        if self.indexed_columns:
            raise Exception("TODO: alter indices for pop")

    def sort(self, key=None, reverse=None):
        """ An implementation of array sort for the matrix. """
        self._matrix.sort(key=key, reverse=reverse)
        self.rebuild_indices()

    #-------------------------------------------------------------------------
    #
    #                        PRIVATE FUNCTIONS
    #
    #-------------------------------------------------------------------------

    def clean(self, row):
        # goes through and does some nice string and text cleaning
        # if dtypes are set, take care of them
        if type(row) is tuple:
            # - if tuple, is read only, and we need to convert to something
            # writable
            row = list(row)
        validators = self.column_validators
        try:
            # choose the correct max col to iterate to, whichis the less of the column validators
            # or the number of elements in the row.
            if not type(validators) is list:
                for i in range(0, len(row)):
                    row[i] = validators(row[i])
            else:
                max = len(validators)
                if len(row) < max:
                    max = len(row)
                for i in range(0, max):
                    if type(row[i]) is str:
                        #
                        # Todo: this should be handled by the datacleaner, not matrix
                        #
                        row[i] = row[i].strip()
                        if row[i] in self.null_values:
                            row[i] = None
                        #
                        #
                        #

                    if validators[i]:
                        row[i] = validators[i](row[i])
        # we get this a lot, so we want more information
        except Exception as Argument:
            print("Failed to parse and assign datatypes to all rows")
            print("This happens in col="    +self.columns[i]+" ("+str(i)+") with row value "+str(row[i]))
            print("Entire Row = ", row)
            raise Argument

        # account for blank cells at the end, which may not have parsed
        while self.columns and len(row) < len(self.columns):
            row.append(None)

        # account for rows that are longer than the columns
        if self.columns and len(row) > len(self.columns):
            # expand the matrix if policy is allow
            if self.rowcount_policy == 'accommodate':
                for newcol in range(self.ncolumns, len(row)):
                    self.add_column(name='<blank>')
            # append the row - for all other policies, we chop down and append the row,
            # but the user can do things
            else:
                if self.rowcount_policy == 'error':
                    raise Exception("strict_count error: columns have "+str(self.ncolumns)+" fields, but the following row has " + str(len(row)) + ": \n", ' ; '.join(str(x) for x in row))
                elif self.rowcount_policy == 'warning':
                    warnings.warn("Columns have " + str(self.ncolumns) + " fields, but a row has " + str(len(row)) + " items. Chopping off extra values.")
                # if we get here, the policy allows this to happen
                row = row[:len(self.columns)]

        return(row)

    def make_hashmap(self, row):
        return({ self.columns[i]:row[i] for i in range(len(self.columns)) })


    def _render_columns(self, original_columns):
        """ Processes the original set of column names and creates all of the column-related data structures references by the following properties: columns, ncolumns, duplicate_columns, colmap, original_columns"""
        columns = list(original_columns)
        colmap = {} # hash of {column_name: location of column}
        column_duplicates={} # hash of { column_name: # of duplicates }

        for i in range(0,len(columns)):
            # columns cannot be none, but if they are blank and came through one of the stock MatrixSources
            # they will be processed as blank, and here they are converted to a string
            if self.column_normalizer:
                if callable(self.column_normalizer):
                    # can always pass in just a function
                    columns[i] = self.column_normalizer(columns[i])
                else:
                    columns[i] = self.column_normalizer.clean(columns[i])
            elif type(columns[i]) is str:
                columns[i] = columns[i].strip()

            # make sure there are no duplicate columnss...
            # if there are, we mangle them to be non-problematic
            if columns[i] in column_duplicates:
                # already duplicated! just iterate
                column_duplicates[columns[i]] += 1

                if self.recode_duplicates:
                    columns[i] += '.' + str(column_duplicates[columns[i]])
                    colmap[columns[i]] = i
                else:
                    colmap[columns[i]].append(i)

            elif columns[i] in colmap:
                # we just found a duplicate column, but it has not been duplicated previously.
                # add to the duplicate map with number of columns that have duplicate names.

                if self.duplicate_column_policy == 'error':
                    raise Exception("Found duplicate column name "+columns[i]+" in MatrixB (and duplicate_column_policy is 'error').")
                elif self.duplicate_column_policy == 'warning':
                    if self.recode_duplicates:
                        warnings.warn("Found duplicate column name "+columns[i]+" in MatrixB.  names to be recoded to " + columns[i] + ".<index>")
                    else:
                        warnings.warn("Found duplicate column name "+columns[i]+" in MatrixB.  Names are not recoded; the colmap will point to arrays for columns with duplicates")


                column_duplicates[columns[i]] = 2
                if not self.recode_duplicates:
                    # we convert colmap to an array and add this index as the second entry.
                    colmap[columns[i]] = [ colmap[columns[i]], i ]
                else:
                    # remap the old colmap (in this case, colmap[columns[i]] != i because of the duplication)
                    colmap[ columns[i] + '.1' ] = colmap[ columns[i] ]
                    columns[ colmap[columns[i]] ] = columns[i] + '.1'
                    del colmap[ columns[i] ]

                    # now map the current column
                    columns[ i ] = columns[i] + '.2'
                    colmap[columns[i]] = i
            else:
                colmap[columns[i]] = i

        # if there are duplicates, save them
        self._original_columns = original_columns
        self._columns = columns
        self._colmap = colmap
        self._column_duplicates = column_duplicates
        self._ncolumns = len(columns)


    def _parse_column_definition(self, column_definition):
        """ helper function to parse different ways to denote a column definition. This is used by multiple functions, including index_column and lookup

        Params:
            column: The column definition about which to maintain the index.  This can be one of the following:
                {str} : uses the colmap to determine the column location
                {int} : expected to be the index of the column
                {dict} of {'type':'column_name', 'value': column_name_var} : if you have non-string column names, this should be your format

        Returns: The index of the column if it was found, otherwise None
        """
        if type(column_definition) is dict:
            if column_definition['type'] != 'column_name':
                raise Exception("Do not know how to index a column of type '"+str(column_definition['type'])+"'")
            return(self.colmap[column_definition['value']])
        elif type(column_definition) is str:
            return(self.colmap[column_definition])
        elif type(column_definition) is int and column_definition < len(self.columns):
            return(column_definition)
        return(None)

    def _index_values(self, row, icol, values):
        """ A function to add a new value to an index """

        if type(values) not in (list,tuple):
            values = [ values ]
        for value in values:
            if None == value or value == '':
                if self._index_attributes[icol]['ignore_null']:
                    continue
                else:
                    raise Exception("Default index behavior is not-null, and nulls found in column " + str(icol)+". Add ignore_null=True if desired")
            if self._index_attributes[icol]['unique']:
                if value in self._indices[icol]:
                    raise Exception("Unique index requested for column "+str(icol)+", but column is not unique for value "+value)
                else:
                    self._indices[icol][value] = row
            else:
                if value not in self._indices[icol]:
                    self._indices[icol][value] = []
                self._indices[icol][value].append(row)

    def _remove_value_from_index(self, row, icol, value):
        if value not in self._indices[icol]:
            raise Exception("Cannot find value in index for column " + str(icol) + ". Is your index out of sync?")

        if self._index_attributes[icol]['unique']:
            if self._indices[icol][value] != row:
                raise Exception("Unexpected row set for the value in a unique index!")
            del self._indices[icol][value]
        else:
            row_index = self._indices[icol][value].index(row)
            if row_index < 0:
                raise Exception("Cannot find row in the index to delete!")
            del self._indices[icol][value][row_index]

    def _typechecker(self, vartype):
        if vartype is bool:
            return(lambda val: datacleaner.DataCleaner.parse_boolean(val))
        elif vartype is datetime.datetime:
            return(lambda val: datacleaner.DataCleaner.parse_datetime(val))
        elif vartype is datetime.date:
            return(lambda val: datacleaner.DataCleaner.parse_date(val))
        elif vartype is datetime.time:
            return(lambda val: datacleaner.DataCleaner.parse_time(val))
        elif vartype == 'maybeint':
            return(lambda val: datacleaner.DataCleaner.parse_maybeint(val))
        else:
            return(lambda val: None if val is None else vartype(val))
            #raise Exception("Column type '"+str(vartype)+"' does not have a defined parser in the datacleaner.")

    def _typeclosure(self, type):
        return(lambda val: val if type(val) in (type, NoneType) else type(val))

    def _lambdaclosure(self, closure):
        return(lambda val: closure(val))


    def make_rowmap(self, row):
        return({colname: row[ self.colmap[colname] ] for colname in self.columns})

    def rebuild_indices(self):
        indices = list(self._indices.keys())
        self._indices = {}
        for col in indices:
            self.index_column(col, ignore_null=self._index_attributes[col]['ignore_null'], unique=self._index_attributes[col]['unique'])

    def __getstate__(self):
        """ To serialize/pickle """

        # load all rows
        self.load(automated=True)

        state = self.__dict__.copy()
        # -- remove generated objects that don't pickle well and can be regenerated upon reload
        for attrib in ('_column_validators', '_column_normalizer'):
            del state[attrib]

        return(state)


    def __setstate__(self, state):
        """ To load from pickle """
        self.__dict__ = state
