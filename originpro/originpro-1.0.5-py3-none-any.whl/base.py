"""
originpro
A package for interacting with Origin software via Python.
Copyright (c) 2020 OriginLab Corporation
"""
# pylint: disable=C0103,C0301,R0913
import abc
import xml.etree.ElementTree as ET
from .config import po
from .utils import origin_class, get_file_ext, _tree_to_dict

def _DC_from_ext(ext):
    if ext in ['.csv', '.asc', '.txt', '.dat']:
        return 'csv'
    if ext in ['.xls', '.xlsx']:
        return 'excel'

    raise ValueError('file type not supported, must be text or Excel files')


class BaseObject:
    """base class for all Origin objects"""
    def __init__(self, obj):
        if obj is None:
            raise TypeError
        self.obj = obj
        #print('constructor for ' + str(type(self.obj).__name__))
    def __str__(self):
        return self.obj.GetName()
    def __bool__(self):
        if self.obj is None:
            return False
        return self.obj.IsValid()
    def index(self):
        """interal index in corresponding collection of the object"""
        return self.obj.GetIndex()
    def get_str(self, prop):
        """Get object's LabTalk string property"""
        return self.obj.GetStrProp(prop)
    def get_int(self, prop):
        """Get object's LabTalk int property"""
        try:
            return int(self.get_float(prop))
        except ValueError:
            return 0
    def get_float(self, prop):
        """Get object's LabTalk float property"""
        return self.obj.GetNumProp(prop)
    def set_str(self, prop, value):
        """Set object's LabTalk string property"""
        self.obj.SetStrProp(prop, value)
    def set_int(self, prop, value):
        """Set object's LabTalk int property"""
        self.obj.SetNumProp(prop, int(value))
    def set_float(self, prop, value):
        """Set object's LabTalk float property"""
        self.obj.SetNumProp(prop, value)
    def method_int(self, name, arg=''):
        """execute object's LabTalk method that has an int return"""
        try:
            return int(self.method_float(name, arg))
        except ValueError:
            return 0
    def method_float(self, name, arg=''):
        """execute object's LabTalk method that has a float return"""
        return self.obj.DoMethod(name, arg)
    @property
    def name(self):
        """short name of the object"""
        return self.obj.GetName()
    @name.setter
    def name(self, value):
        """
        change the short name of an object, if there is a conflict,
        Origin will change to next available name automatically
        Examples:
            gp=op.new_graph()
            gp.name='Test'
            gp=op.new_graph()
            gp.name='Test'
            print(gp)#Test1
        """
        self.obj.SetName(value)
    @property
    def lname(self):
        """
        Property getter returns long name of object.

        Parameters:

        Returns:
            (str)

        Examples:
            print(wb.lname)
        """
        return self.obj.GetLongName()
    @lname.setter
    def lname(self, value):
        """
        Property setter sets long name of object.

        Parameters:
            value (str): long name

        Returns:
            None

        Examples:
            wb.lname = 'My Data'
        """
        self.obj.SetLongName(value)
    @property
    def comments(self):
        """
        Property getter returns long name of object.
        Examples:
            wb.comments='My labs data'
            print(wb.comments)
        """
        return self.obj.GetComments()
    @comments.setter
    def comments(self, value):
        """
        Property setter sets the comments of an object.
        Examples:
            wb.comments='My labs data'
            print(wb.comments)
        """
        self.obj.SetComments(value)
    @property
    def show(self):
        """
        Property getter returns show state of object.

        Parameters:

        Returns:
            (bool)

        Examples:
            print(wb.show)
        """
        return self.obj.GetShow()
    @show.setter
    def show(self, value):
        """
        Property setter sets show state of object.

        Parameters:
            value (bool): True to show object

        Returns:
            None

        Examples:
            wb.show = True
        """
        self.obj.SetShow(value)

    @property
    def usertree(self):
        """
            Return User Tree as ElementTree
        """
        s = self.get_str('tree')
        if not s:
            return ET.Element('OriginStorage')
        return ET.fromstring(s)

    @usertree.setter
    def usertree(self, tr):
        """
            Set User Tree

        Parameters:
            tr (ElementTree): tree to set
        """
        self.set_str('tree', ET.tostring(tr, encoding='unicode'))

    @property
    def userprops(self):
        """
            Return User Tree as dict
        """
        dd = {}
        tr = self.usertree
        if tr:
            for node in tr:
                _tree_to_dict(dd, node)
        return dd

    #@userprops.setter
    #def userprops(self, value):
        #pass


class BaseLayer(BaseObject):
    """base class for all Origin layers"""
    def __str__(self):
        graph = self.obj.GetParent()
        return '[{0}]{1}'.format(graph.GetName(), self.obj.GetName())

class BasePage(BaseObject):
    """
    base class for all Origin books and graph, it holds a PyOrigin Page
    """
    def __len__(self):
        return self.obj.Layers.GetCount()

    def lt_exec(self, labtalk):
        """
        executes a LabTalk statement.

        Parameters:
            labtalk (str): LabTalk statement

        Returns:
            None

        Examples:
            wb.lt_execute('page.longname$="lt_exec example"')
        """
        po.LT_execute(f'win -o {self.obj.GetName()} {{{labtalk}}}')

    def is_open(self):
        """
        Returns whether book is neither hidden, nor minimized.

        Parameters:

        Returns:
            (bool)

        Examples:
            b = wb.is_open()
        """
        return self.get_int('Win') > 2


class DBook(BasePage):
    """base class for data books, like workbook and matrix book"""
    def __repr__(self):
        return f'{type(self).__name__}: ' + self.lt_range()

    def _get_book_type(self):
        if isinstance(self.obj, origin_class('WorksheetPage')):
            return 'w'
        if isinstance(self.obj, origin_class('MatrixPage')):
            return 'm'
        raise ValueError('wrong object type')

    def __getitem__(self, index):
        return self._sheet(self.obj.Layers(index))

    def __iter__(self):
        for elem in self.obj.Layers():
            yield self._sheet(elem)

    def _add_sheet(self, name, active):
        obj1 = self.obj.AddLayer(name)
        if active:
            self.set_int("active", obj1.GetIndex()+1)
        return obj1

    def lt_range(self):
        """return the Origin Range String that iddentify book object"""
        return f'[{self.obj.GetName()}]'

    @abc.abstractmethod
    def _sheet(self, obj):
        raise ValueError(f'{self.lt_range()} Derived class must define its own _sheet method!')

class DSheet(BaseObject):
    """base class for data sheets, like worksheets and matrix sheets"""
    def __str__(self):
        return self.lt_range()
    def __repr__(self):
        return 'DSheet: ' + self.lt_range()
    def _get_book(self):
        return self.obj.GetParent()

    @property
    def shape(self):
        """return the rows and columns of a sheet"""
        return self.obj.GetRowCount(), self.obj.GetColCount()
    @shape.setter
    def shape(self, val):
        """
        setting the number of rows and columns in a sheet
        Parameters:
            val (tuple): rows, cols, 0 = unchanged
        Returns:
            (tuple) the new shape
        Examples:
            wks=op.find_sheet()
            #leave rows unchanged and set to 3 columns
            wks.shape=0,3
        """
        if not isinstance(val, (tuple, list)) or len(val) != 2:
            raise ValueError('must set by rows, cols')
        rows, cols = val

        if isinstance(self.obj, origin_class('Matrixsheet')):
            if cols <= 0 or rows <= 0:
                raise ValueError('setting matrix sheet shape must provde both rows and cols')
            self.obj.SetShape(rows,cols)
        else:
            if cols > 0:
                self.obj.SetColCount(cols)
            if rows > 0:
                self.obj.SetRowCount(rows)

        return self.shape

    def remove_DC(self):
        """
        Removes Data Connector from a sheet.

        Parameters:

        Returns:
            None

        Examples:
            wks.remove_DC()
        """
        self.obj.LT_execute('wbook.dc.Remove()')

    def has_DC(self):
        """
        Returns whether a sheet has a Data Connector.

        Parameters:

        Returns:
            (str) name of the Data Connector, like 'csv', 'excel'

        Examples:
            dc = wb.has_DC()
            if len(dc):
                print(f'sheet is connected using {dc}')
        """
        if self.obj.GetNumProp('HasDC')==0:
            return ''
        dc_file = self.get_book().get_str('DC.Type')
        type_ = dc_file.split('_',2)[0]
        return type_.lower()

    def from_file(self, fname, keep_DC=True, dctype='', sel='', sparks=False):
        r"""
        Imports data from a file using a Data Connector.

        Parameters:
            fname (str): File path and name to import.
            keep_DC (bool): Keep the Data Connector in the book after import
            dctype (str): Data Connector name, like "Import Filter", "MATLAB", "NetCDF", if not specified, CSV or Excel connector will be used based on file name
            sel (str): selection in the file, this will depends on the connector
            sparks (bool): Allows sparklines or not, True will follow GUI setting to add sparklines, False will disable it completely
        Returns:
            None

        Examples:
            wks=op.find_sheet()
            fn=op.path('e') + 'Samples\\Import and Export\donations.csv'
            wks.from_file(fn, False)#remove connector after import to allow further edit of data
            wks2=op.new_sheet()
            wks2.from_file(op.path()+'test.xlsx')#assuming you have this in UFF(user file folder)
        """
        oldspark=int(po.LT_get_var('@IMPS'))
        newspark = 1 if sparks else 0
        po.LT_set_var("@IMPS", newspark)
        ext = get_file_ext(fname)
        DC = dctype if dctype else _DC_from_ext(ext)
        currentDC = self.has_DC()
        if currentDC and currentDC != DC:
            self.remove_DC()
            currentDC=''
        if not currentDC:
            self.obj.DoMethod('DC.Allow', '2')
            self.obj.LT_execute(f'wbook.dc.add({DC})')
        self.obj.SetStrProp('DC.Source', fname)
        #Import Filter Connector need to do wks.dc.Import(1) in order to find the OIF filter
        imp_arg = '1' if dctype=='Import Filter' else ''
        if sel:
            self.obj.SetStrProp('DC.Sel', sel)
            imp_arg = ''
        self.method_int('dc.import', imp_arg)
        po.LT_set_var("@IMPS", oldspark)
        #print(f'dc import return {ret}')
        if not keep_DC:
            self.remove_DC()

    def lt_range(self, use_name=True):
        """return the Origin Range String that iddentify each object"""
        book = self.obj.GetParent()
        if use_name:
            return '[{0}]{1}'.format(book.GetName(), self.obj.GetName())
        return '[{0}]{1}'.format(book.GetName(), self.index()+1)

    @abc.abstractmethod
    def get_book(self):
        'Must be implemented by dervied methods'
        raise ValueError(f'{self.lt_range()} Derived class must define its own get_book method!')

    @abc.abstractmethod
    def get_labels(self, type_ = 'L'):
        'get_labels'

    @abc.abstractmethod
    def set_labels(self, labels, type_ = 'L'):
        'set_labels'
