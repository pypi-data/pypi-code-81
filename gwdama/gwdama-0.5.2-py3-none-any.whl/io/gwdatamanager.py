# This file is part of the GwDataManager package.
# Import data from various location into a dictionary-like object.
# 

"""
GwDataManager
=============

This is the basic container to read and store data, and give acces to their manipulation in term of Datasets

This is based on `h5py` classe File and Datase, with some modifications.
In particular, the class Dataset comprizes some new methods and properties
to make it more easy to manipulate.
"""

import sys, time
import numpy as np
from os.path import join, isfile, split, splitext, basename, dirname
from glob import glob
from multiprocessing import Pool, cpu_count

# For the base classes and their extentions
import h5py
from .dataset import * 
from gwdama.utilities import find_run, _add_method

# For File object stored in memory or as temprary file
from io import BytesIO
from tempfile import TemporaryFile

# Locations of ffl
from . import ffl_paths

# imports related to gwdama
from .gwLogger import GWLogger

# Necessary to fetch open data and to handle gps times
from gwpy.timeseries import TimeSeries, TimeSeriesDict
from gwpy.time import to_gps

# Necessary to export or import as pandas Dataframe
from pandas import DataFrame

# To print warnings
from warnings import warn

# ----- Utility functions specific to GwDataManager -----

def recursive_struct(group, indent = '  '):
    """
    Function to print a nice tree structure:
    │
    ├──
    └──
    """
    to_print = ''
    if isinstance(group, h5py.Group):
        for i,k in enumerate(group.keys()):
            if i+1<len(group.keys()):
                to_print += indent + f"├── {k}\n"
            else:
                to_print += indent + f"└── {k}\n"
                
            if isinstance(group[k], h5py.Group) and (i+1<len(group.keys())):
                to_print += recursive_struct(group[k], indent=indent+'│   ')
            elif isinstance(group[k], h5py.Group):
                to_print += recursive_struct(group[k], indent=indent+'    ')
                  
    return to_print 

def key_changer(obj, key=None):
    """
    Check if a key is present in a dictionary-like object.
    If already present, change its name adding '_#', with increasing
    numbers.
    """
    if key is None:
        key = 'key'  # Default value
    if key in obj.keys():
        expand = 0
        while True:
            expand += 1
            new_key = key +'_'+ str(expand)
            if new_key in obj.keys():
                continue
            else:
                key = new_key
                break
    return key

# ----- Additional method of h5[y.Group to return Datasets -----

@_add_method(h5py.Group)
def to_DataFrame(self, **dfkwgs):
    """
    Convert this Group to a `pandas.DataFrame <https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html>`_. The names of the columns are the keys of each Dataset, and their numeric value is equal to their data. The Datasets must have the same length in order to be aligned, otherwise a ``TypeError`` will be raised.
    
    Parameters
    ----------
    dfkwgs : dict, optional
        Keyword arguments of `pandas.DataFrame <https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html>`_, excluding ``data``. By default, the ``index`` parameter is obtained from the ``times`` attribute of each Dataset if they are equal. Otherwise it is a RangeIndex
        
    Returns
    -------
     : `pandas.DataFrame <https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html>`_
         DataFrame representing the current `Group <https://docs.h5py.org/en/stable/high/group.html>`_ object
     
    Raises
    ------
    TypeError
        if the Datasets in this group have different lengths and can't be aligned into a dataframe
    """
    # Check that the length, t0 and sample rate of all the elemts of the group are the same
    chks = {'len': [], 't0': [], 'sample_rate': []}
    for val in self.values():
        if isinstance(val, h5py.Dataset):
            chks['len'].append(len(val))
            chks['t0'].append(val.attrs.get('t0', np.nan))
            chks['sample_rate'].append(val.attrs.get('sample_rate', np.nan))

    if not all(ll==chks['len'][0] for ll in chks['len']):
        raise TypeError("This group has Datasets of different lengths. Cannot align them to a Pandas DataFrame. Maybe this is due to different 'sample_rate' and 'duration' attributes. Try resampling, in this case")
    elif all(tt==chks['t0'][0] for tt in chks['t0']) and all(sr==chks['sample_rate'][0] for sr in chks['sample_rate']):            
        index = np.arange(chks['len'][0])/chks['sample_rate'][0] + chks['t0'][0]
        index_name = 'gps_time'
    else:
        warn("WARNING! The Datasets have not the same initial time or sample rate. The index of the resulting DataFrame is simply a RangeIndex")
        index = np.arange(chks['len'][0])
        index_name = None
    
    dfkwgs['index'] = dfkwgs.get('index', index)
    
    df = DataFrame(data={k: val[...] for k, val in self.items() if isinstance(val, h5py.Dataset)},**dfkwgs) 
    df.index.name = index_name
    
    return df
    
# ----- The Class -----

class GwDataManager(h5py.File):
    """
    Main class for GW data management. Basically, this is an enhanced version of the :py:class:`h5py.File` class, with various methods for importing GW data from different sources, pre-processing functions, plotting, and more.
    
    One key aspect regards the ``storage`` of this file while in use, as specified by the corresponding parameter. This can be an actual *hdf5 file* saved on ``'disk'`` (to be passed to the previous parameter), or a `file-like object <https://docs.h5py.org/en/stable/high/file.html#python-file-like-objects>`_, such as a temporary file (``'tmp'``) on disk, or a `BytesIO file <https://docs.python.org/3/library/io.html#io.BytesIO>`_ using a in-memory bytes buffer (``'mem'``). The first method is the more common when manipulating existing files. The latter ``io.BytesIO``, being in-memory, is usually the fastest and particularly indicated for testing. If you want to write large amounts of data, a better option may be to store temporary data on disk using ``'tmp'``.
    
    Also, the parameter ``mode`` can be passed to the class instance. If ``storage='disk'``, this tells how to open the file; possible vallues are: ``'r'``, ``'r+'``, ``'a'``, ``'w'``, ```'w-'`` or ``'x'``. If the previous option allow modifying the file, then new memory is allocated on disk next to the one occupied by the source file. It is important to close the file once you are done with manipulating it, ``dama.close()``, or to make use of a `context manager <https://book.pythontips.com/en/latest/context_managers.html>`_: ``with GwDataManager('/path/to/file.h5', mode='r+') as dama: ...``.
    
    Instead, if the :class:`~gwdama.io.GwDataManager` istance refers to a file-like object (``'tmp'`` or ``'mem'``), one can can pass ``mode='r'``, and import the data stored in the hdf5 file at the path specified by ``dama_name``. In this case, a copy of the provided file is loaded in-memory or as a temporary file. Remeber to save it afterwards. An ``IOError`` is raised if this is not a valid path to a file. If ``mode`` is not specified (or if it has any other value), a blank file-like object is created.
    
    Parameters
    ----------
    dama_name : str, optional
        Name to assign to the :class:`~gwdama.io.GwDataManager` object or path to an existing hdf5 file if the ``mode`` parameter is set to this purpose (that is, ``'r'``, ``'r+'`` or ``'a'``). A defoult ``'mydama'`` is chosen if not provided.
    storage : str, optional
        This parameter determines where the bytes corresponding to this object are stored. Available options are ``'disk'``, useful when one wants to modify an existing "dama" (hdf5), or ``'mem'`` and ``'tmp'`` for a "file-like" object. In the case of ``'mem'`` (default), a BytesIO file is created in-memory. This is the fastest option and particularly recommended for testing. `If `'tmp'``, a temporary file is created on disk (but it is not accessible otherwise). This is the preferreed option when manipulating very large amounts of data.
    mode : str, optional
        When the ``storage`` parameter is set to ``'disk'``, this parameter determines the mode the file specified in ``dama_name`` is opened. Avaliable options are: ``'r'`` (read only, file must exist), ``'r+'`` (read/write, file must exist), ``'w'`` (create file, truncate if exists), ``'w-'`` or ``'x'`` (create file, fail if exists), and ``'a'`` (read/write if exists, create otherwise). The default behaviour is that ``mode='r'`` if ``storage='disk'``, that is, it attempts to read an existing file on disk if this option is chosen. Raises error if the file is not present. Instead, for the other available options of ``storage``, this parameter has no effect but in the case ``dama_name`` points to an existing file and this ``mode`` is set to ``'r'``. In this case, a new file like object is created with the content of the existing file (which is not modified otherwise).
    **kwargs : dict, optional
        Other parameters that can be passed to `h5py.File objects <https://docs.h5py.org/en/stable/high/file.html>`_. 
    
    Raises
    ------
    OSError
        if ``mode`` is ``'w-'`` or ``'x'`` and the file you want to create already exists, or with ``'r+'`` or ``'r'`` if the file you want to read doesn't exist.
    
    Examples
    --------
    Everything starts by initializing the :class:`~gwdama.io.GwDataManager` class like this::
    
      >>> dama = GwDataManager()
      
    If you want to assign a name to this instance, pass it within parentesis. By default, this is an in-memory object that will be cancelled when you close the Python session. However, it is good practice to close it beforehand with::
    
      >>> dama.close()
      
    Instead, if you want to open an existing hdf5 file, such as a previously created "dama", pass its name as the ``dama_name``, and make use of the value ``'r'`` (or similar) for the parameter ``mode``.
        
    Notes
    -----
    Refer to the description for more details on the parameter ``storage``, which determines the memory allocation of this class.
         
    """
    # NOTE: put methods in alphbetical order!
   
    def __init__(self, dama_name="mydama", storage='mem', mode=None, **kwargs):
        
        # Create a new temporary file. If dama_name is a path to a valid file, its content is recovered
        if storage in ('mem','tmp'):
            if storage=='mem':
                tf = BytesIO()
            elif storage=='tmp':
                tf = TemporaryFile()
            # Create in-memory object  
            super().__init__(tf, mode='w', **kwargs)    
            
            # Add a couple of attributes to this dataset, like a name and its time stamp
            self.attrs['dama_name'] = splitext(split(dama_name)[-1])[0]
            self.attrs['time_stamp']=str(time.strftime("%y-%m-%d_%Hh%Mm%Ss", time.localtime()))
            
            # A file exists at the path 'dama_name', try to get its content
            if isfile(dama_name) and (mode=='r'):
                print("Reading dama... ",end='')
                with h5py.File(dama_name, 'r') as existing_dama:
                    for k in existing_dama.keys():
                        existing_dama.copy(k,self)
                    for k in existing_dama.attrs.keys():
                        self.attrs[k] = existing_dama.attrs[k]
                    print(' done.')
                            
        elif storage=='disk':
            if isfile(dama_name) and (mode is None):   
                print("Reading dama... ",end='')
                super().__init__(dama_name, mode='r', **kwargs)
                print(' done.')

            elif isfile(dama_name):
                print("Reading dama... ",end='')
                super().__init__(dama_name, mode=mode, **kwargs)
                print(' done.')                
                          
            else:
                print('Creating new dama... ',end='')
                super().__init__(dama_name, mode=(mode or 'w-'), **kwargs)
                self.attrs['dama_name'] = splitext(split(dama_name)[-1])[0]
                self.attrs['time_stamp']=str(time.strftime("%y-%m-%d_%Hh%Mm%Ss", time.localtime()))                
                print(' done.')                   

                
    def __repr__(self):
        """
        String representation of the object.
        """
        str_to_print = f"<{type(self).__name__} object at {hex(id(self))}: {self.attrs['dama_name']}>"
        #for k, val in self.__data_dict.items():
        #    str_to_print +="\n  {:>8} : {}".format(k,val.__repr__())
        return str_to_print
 

    def __str__(self):
        str_to_print = f"{self.attrs['dama_name']}:\n"+ recursive_struct(self)
 
        str_to_print += "\n  Attributes:\n"
        for k, val in self.attrs.items():
            str_to_print += "  {:>12} : {}\n".format(k, val)

        return str_to_print

    
    @property
    def show_attrs(self):
        """
        Property that makes the :class:`~gwdama.io.GwDataManager` object to print in a conveninet way all of its attributes name and key pairs.
        """
        to_print = ''
        for k, val in self.attrs.items():
            to_print += "{:>10} : {}\n".format(k, val)
        #return to_print
        print(to_print)

        
    @property
    def groups(self):
        """
        This property returns a list with the name of each group and subgroup af the current :class:`~gwdama.io.GwDataManager` object.
        This fuction could be possibly improved allowing the possibility to create sublists for each group and subgroup.
        """
        groups = []
        self.visititems(lambda g,_: groups.append(str(g)))
        return groups
    
    def read_gwdata(self, start, end, data_source=None, dts_key=None, duplicate='rename', return_output=False, **kwargs):
        """   
        This is the main function to access data from various locations. Given the value of the ``data_source`` parameter, this method can read form files in the ``local`` file system, provided their paths, or some specifications about them, or from `GWOSC <https://www.gw-openscience.org/about/>`_, either online or from CVMFS. Depending on this parameter or on other passed as ``**kwargs``, this function selecs one from        :func:`~gwdama.io.GwDataManager.read_from_virgo`, :func:`~gwdama.io.GwDataManager.read_gwdata_gwosc_remote` or :func:`~gwdama.io.GwDataManager.read_gwdata_gwosc_cvmfs` methods. The corresponding data will be added to the current dataset.
        
        Parameters
        ----------
        start : LIGOTimeGPS, float, str
            GPS start time of required data. Any input parseable by to_gps is fine. For example, a quick way to provide dates is in the format of ``'YYYY-MM-DD (hh:mm:ss)'``
        end : LIGOTimeGPS, float, str, optional
            GPS stop time of required data; any input parseable by to_gps is fine
        data_source : str, optional
            defines the way data is read, and from where. Possible options: ``gwosc-online`` (default), ``gwosc-cvmfs``, ``local``. If none of the previous options hase been passed, then other parameters passed as keyword arguments are checked. For example, ``ffl_spec``, ``ffl_path`` or ``gwf_path``, which make to select option ``local``. Otherwise the default option is ``geosc-pnline``, meaning that the data are accessed from the GWOSC open data
        dts_key : str, optional
            name of the Dataset or of the Group to append to the :class:`~gwdama.io.GwDataManager`. If not provided and ``channels`` is provided and it is a string (single channel), then its name is used as ``dts_key``. If ``channels`` is a list of channels, then the ``dts_key`` is by defoult ``'channels'``
        duplicate : {``'replace'``, ``'rename'``, ``'raise'``}, optional
            If we try to append a dataset with an already existing key, we have the possibility
            to ``'replace'`` the previous one (deleting its content) or ``'rename'`` the corresponding
            key: "existing_key" -> "exisitng_key_1". Otherwise, with ``'rise'`` an error message is risen. Default ``'rename'``
        return_output : bool, optional
            If ``False`` (default), the new :class:`~gwdama.io.Dataset` is added to the :class:`~gwdama.io.GwDataManager` object and no output is returned. If ``True``, ``self['dts_key']`` is returned, which can be a Dataset or a Group depending on the number of channels that have been read
        **kwargs
            Depending on the ``data_source``, this are the keyword arguments for the corresponding direct method.
            For example, if ``data_source=='local'`` refer to the documentation of the method ``read_from_virgo``.
            If ``data_source=='gwosc-online'``, refer to ``read_gwdata_gwosc_remote``, or if ``data_source=='gwosc-cvmfs'`` to ``read_gwdata_gwosc_cvmfs``
            
        Returns
        -------
         : None, Dataset or Group
             Depending on the ``return_output`` parameter, and the number of channels that have been read
            
        Raises
        ------
        RuntimeError
            every time a wrong data source is provided
        
        Examples
        --------
        To import data from online gwosc (default), we only need to pass a time interval and the name of the interferometer whose data we are interested to: 
        
        >>> from gwdama.io import GwDataManager
        
        >>> start = "2017-08-14 11:59" # One minute before GW170814 merger
        >>> end   = "2017-08-14 12:00:10"
        >>> dama = GwDataManager()  # Default name 'mydama' assigned to the dictionary
        >>> dama.read_gwdata(start, end, ifo='L1')
        
        See Also
        --------
        :func:`~gwdama.io.GwDataManager.read_from_virgo`
        :func:`~gwdama.io.GwDataManager.read_gwdata_gwosc_remote`
        :func:`~gwdama.io.GwDataManager.read_gwdata_gwosc_cvmfs`
        
        """
        # Define a key if not provided:
        # - the name of the channel if there is only one
        # - 'channels' if there are more
        # - strain if we read from gwosc
        if not dts_key:
            if 'channels' in kwargs:
                if isinstance(kwargs['channels'], str):
                    dts_key = kwargs['channels']
                else:
                    dts_key = 'channels' # In this case this is a group
            else:
                dts_key = 'strain'
        
        # Define the data source if not provided
        if not data_source:
            if ('ffl_path' in kwargs) or ('ffl_spec' in kwargs) or ('gwf_path' in kwargs):
                data_source = 'local'
            else:
                data_source = 'gwosc-online'
        
        if (duplicate == "replace") and (dts_key in self.keys()):
            del self[dts_key]
        elif (duplicate == "rename") and (dts_key in self.keys()):
            dts_key = key_changer(self, key=dts_key)
        elif (dts_key in self.keys()):
            raise Exception("Unrecognised 'duplicate' parameter. Please, select either 'rename' or 'replace'.") 
        else:
            pass
        
        if data_source == "gwosc-cvmfs":
            dataset = self.read_gwdata_gwosc_cvmfs(start, end, **kwargs)
        elif data_source == "local":
            dataset = self.read_from_virgo(start=start, end=end, **kwargs)       
            
        elif data_source == "gwosc-online":
            dataset = self.read_gwdata_gwosc_remote(start, end, **kwargs)
        else:
            raise RuntimeError("Data source %s not yet implemented" % data_source)
         
        # Check wether the `dataset` is a gwpy TimeSeries or TimeSeriesDict:        
        if isinstance(dataset, TimeSeriesDict):
            grp = self.create_group(dts_key)
            for k in dataset.keys():
                dset = grp.create_dataset(k, data= dataset[k].data)
                dset.attrs.create('t0', dataset[k].t0)
                dset.attrs.create('unit', str(dataset[k].unit ))
                dset.attrs.create('channel', str(dataset[k].channel))
                dset.attrs.create('sample_rate', dataset[k].sample_rate.value)

        elif isinstance(dataset, TimeSeries):
            dset = self.create_dataset(dts_key, data= dataset.data)
            dset.attrs.create('t0', dataset.t0)
            dset.attrs.create('unit', str(dataset.unit ))
            dset.attrs.create('channel', str(dataset.channel))
            dset.attrs.create('sample_rate', dataset.sample_rate.value)
            
        if return_output:
            return self[dts_key]
                                     
    @staticmethod
    def _search_cvmfs(start=None, end=None,ifo='V1', rate='4k', data_format='hdf5',
                      cvmfs_path='/data2/cvmfs/gwosc.osgstorage.org/gwdata/'):
        """This methood searches the files corresponding to a given format in the
        provided gps time interval, science run (S5, S6, O1 or O2) and interferometer.

        In practice this is a twin of the ``find_gwf`` class method, meant to be
        used primarily on PC-Universe2, where cvmfs is mounted in the provided path,
        or on any other machine changing the path to cvmfs accordignly.

        Parameters
        ----------
        start : `~gwpy.time.LIGOTimeGPS`, float, str, optional
            starting gps time where to find the frame files.
            Default: 1126259462.4 for O1, 1187008882.4 for O2,
            Error for any other choice of run.
            
        end : `~gwpy.time.LIGOTimeGPS`, float, str, optional
            final gps time where to find the frame files. If ``start``
            is not provided, this is automatically set to 60 seconds.
        
        ifo : str, optional
            Name of the interferometer to read the data. Available options: 
                H1, L1, or V1 (default, only for the last part of O2)
 
        data_format : str, optional
            Either ``'hdf5'`` or ``'gwf'``
 
        cvmfs_path : str, optional
            Directory where to look for the hdf5 files. Default choice is the
            directory on PC-Universe2. Don't change this value unless you have
            your own cvmfs on your local machine.
     
        Returns
        -------
        gwf_paths : list of str 
            List of paths to the gwf/hdf5 file(s) in the provided interval.
            
        Notes
        -----
        Still in development.
        """
                
        # 0) Initialise some values if not provided
        if (m_tstart_gps is None):
            m_tstart_gps = 1126259462.4 - 30 # GW150914 - 30 seconds
            m_tstop_gps = m_tstart_gps + 60          # Overwrite the previous 'end'
            warn('Warning! No gps_start provided. GW150914 - 30 sec chosen instead.')
        else:
            m_tstart_gps = to_gps(m_tstart_gps)
            
        if m_tstop_gps is None:
            m_tstop_gps = m_tstart_gps+60
            warn('Warning! No gps_end provided. Duration set to 60 seconds.')     
        else:
            m_tstop_gps = to_gps(m_tstop_gps)
       
        run = find_run(m_tstart_gps, m_tstop_gps)
        
        # Check format and rate
        if m_data_format not in ('hdf5', 'gwf'):
            raise ValueError("Error!! Invalid data format!! It must be either hdf5 or gwf")
        elif m_data_format=='hdf5':
            frmtdir='hdf'
        elif m_data_format=='gwf':
            frmtdir='frame'
        
        if rate not in ('4k', '16k'):
            raise ValueError("Error!! Invalid rate! It must be either 4k or 16k. Remember that you can resample it later.")
        
        # 1) Define the path where to search the files               
        hdf5_paths = glob(join(cvmfs_path,run,'strain.'+rate,frmtdir+'.v1/',ifo,'**/*.'+m_data_format))
        
        # 2) Make a dictionary with start gps time as key, and path, duration, and end as vlas.
        gwf_dict = {int(float(k.split('-')[-2])): {'path': k,
                                                   'len':  int(float(k.split('-')[-1].rstrip(m_data_format))),
                                                    'stop': int(float(k.split('-')[-2]) + float(k.rstrip(m_data_format).split('-')[-1]))
                                                   }
                    for k in hdf5_paths}

        # 3) 
        mindict = {k: v for k, v in gwf_dict.items() if k <= m_tstart_gps}
        try:
            minvalue = max(mindict.keys())
        except ValueError:
            raise ValueError("ERROR!! No GWF file found. Provided gps_start is before the beginning of the ffl.")            
        maxdict = {k: v for k, v in gwf_dict.items() if k >= m_tstart_gps and m_tstop_gps <= v['stop']}
        try:
            maxvalue = min(maxdict.keys())
        except ValueError:
            raise ValueError("ERROR!! No GWF file found. Select new gps time interval or try another frame.")            
            
        gwf_paths = [v['path'] for k, v in gwf_dict.items() if k >= minvalue and k <= maxvalue and v['path'].endswith("."+m_data_format)]

        return gwf_paths
    
    def read_gwdata_gwosc_cvmfs(self, start=None, end=None, ifo='V1',
                                channels=None, nproc=1, rate='4k', data_format='hdf5',
                                crop=True, cvmfs_path='/data2/cvmfs/gwosc.osgstorage.org/gwdata/', **kwargs):
        """
        This method search GW data in the cvmfs aschive with the `_search_cvmfs` method,
        and returns a dataset (either TimeSeries or TimeSeriesDict).
        
        Parameters
        ----------
        run : str, optional
            Name of the run where to read the data. Available options: 
            S5, S6, O1, or O2 (default)
        
        ifo : str, optional
            Name of the interferometer to read the data. Available options: 
            H1, L1, or V1 (default, only for the last part of O2)
        
        cvmfs_path : str, optional
            Directory where to look for the hdf5 files. Default choice is the
            directory on PC-Universe2. Don't change this value unless you have
            your own cvmfs on your local machine.
        
        start : `~gwpy.time.LIGOTimeGPS`, float, str, optional
            starting gps time where to find the frame files. Default: 10 seconds ago
            
        end : `~gwpy.time.LIGOTimeGPS`, float, str, optional
            ending gps time where to find the frame file. If `m_tstart_gps` is not provided, and the default
            value of 10 secods ago is used instead, `mtstop_gps` becomes equal to `m_tstart_gps`+5. If `m_tstart_gps` is
            provided but not `mtstop_gps`, the default duration is set to 5 seconds as well
                   
        nproc : int, optional
            Number of precesses to use for reading the data. This number should be smaller than
            the number of threads that the machine is hable to handle. Also, remember to
            set it to 1 if you are calling this method inside some multiprocessing function
            (otherwise you will spawn an 'army of zombie'. Google it). The best performances
            are obtained when the number of precesses equals the number of gwf files from to read from.
            
        crop : bool, optional
            For some purpose, it can be useful to get the whole content of the gwf files
            corresponding to the data of interest. In this case, set this parameter as False.
            Otherwise, if you prefer the data cropped accordingly to the provided gps interval
            leave it True.
            
        Returns
        -------
        outGwDM : TimeSeriesDict 
            filled with the Datasets corresponding to the specifications
            provided in the input parameters
            
        """    
        # -- Improvement ---------------------
        # It is a waste of lines of code to repeat the gps checks etc. in each  method.
        # This will be improved in a next release 
        
       # 0) Initialise some values if not provided
        if not start:
            start = 1126259462.4 - 30 # GW150914 - 30 seconds
            end = start + 60          # Overwrite the previous 'end'
            warn('Warning! No gps_start provided. GW150914 - 30 sec chosen instead.')

        if not end:
            end = start+60
            warn('Warning! No gps_end provided. Duration set to 60 seconds.')     
    
        run = find_run(start,end)
            
        # Check format and rate
        if data_format not in ('hdf5', 'gwf'):
            raise ValueError("Error!! Invalid data format!! It must be either hdf5 or gwf")
        if rate not in ('4k', '16k'):
            raise ValueError("Error!! Invalid rate! It must be either 4k or 16k. Remember that you can resample it later.")
        
        # If the name of the channel(s) has been provided, replace the 'ifo' with one matching
        if isinstance(channels,list):
            ifo = channels[0][:2]
        elif isinstance(channels,str):
            ifo = channels[:2]
        else:
            # Define the channel names
            if (data_format=='gwf') and (rate=='4k') and (run not in ('O2','O3a')):
                channels=[f'{ifo}:LOSC-STRAIN',f'{ifo}:LOSC-DQMASK' ,f'{ifo}:LOSC-INJMASK']  # 4k before O2
            elif (data_format=='gwf') and (rate=='4k'):
                channels=[f'{ifo}:GWOSC-4KHZ_R1_STRAIN',f'{ifo}:GWOSC-4KHZ_R1_DQMASK' ,f'{ifo}:GWOSC-4KHZ_R1_INJMASK'] # 4k since O2
            elif (data_format=='gwf') and (rate=='16k'):
                channels=[f'{ifo}:GWOSC-16KHZ_R1_STRAIN',f'{ifo}:GWOSC-16KHZ_R1_DQMASK' ,f'{ifo}:GWOSC-16KHZ_R1_INJMASK'] 
        
        # 1) Make a dictionary of hdf5 file paths corresponding to the provided specs

        # Find the paths to the gwf's
        pths = self._search_cvmfs(ifo=ifo, start=start, end=end,
                                  cvmfs_path=cvmfs_path, rate=rate, data_format=data_format)
        
        # If data are read from just one gwf/hdf5, crop it immediately
        if len(pths)==1 and do_crop:
            if data_format=='hdf5':
                out_dataset = TimeSeries.read(source=pths, start=start, end=end, nproc=nproc, format='hdf5.losc', **kwargs)
            elif m_data_format=='gwf':
                out_dataset = TimeSeriesDict.read(source=pths, channels=channels, start=start, end=end,
                                                  nproc=nproc, dtype=np.float64, **kwargs)               
        elif not do_crop:
            if m_data_format=='hdf5':
                out_dataset = TimeSeries.read(source=pths, nproc=nproc, format='hdf5.losc', **kwargs)
            elif m_data_format=='gwf':
                out_dataset = TimeSeriesDict.read(source=pths, channels=channels, nproc=nproc, dtype=np.float64, **kwargs)                
                           
        elif len(pths)>1:
            if data_format=='hdf5':
                try:
                    TS = TimeSeries.read(source=pths, nproc=nproc, format='hdf5.losc', **kwargs)
                    out_dataset = TS.crop(start=to_gps(start), end=to_gps(end))
                except ValueError:
                    warn('WARNING!!! Selected data interval contains holes (missing data). Trying to fetch them form online gwosc' )
                    # Try to get it from online
                    try:
                        out_dataset = TimeSeries.fetch_open_data(ifo, start=start, end=end,
                                                                 tag=kwargs.get('tag','CLN'),format='hdf5', **kwargs)
                        out_dataset.sample_rate = sample_rate
                    except:
                        print('No way of obtaining this data... Sorry!' )
                        out_dataset = TimeSeries([])
                        pass
                
            elif data_format=='gwf':
                try:
                    out_dataset = TimeSeriesDict.read(source=pths, channels=channels, nproc=nproc, dtype=np.float64, **kwargs)
                    out_dataset = out_dataset.crop(start=to_gps(start), end=to_gps(end))
                except ValueError:
                    warn('WARNING!!! Selected data interval contains holes (missing data). Trying to fetch them form online gwosc' )
                    # Try to get it from online
                    try:
                        out_dataset = TimeSeries.fetch_open_data(ifo, start=start, end=end,
                                                                 tag=kwargs.get('tag','CLN'),format='hdf5', **kwargs)
                        out_dataset.sample_rate = sample_rate
                    except:
                        print('No way of obtaining this data... Sorry!' )
                        out_dataset = TimeSeries([])
                        pass           

        else:
            # Return whole frame files: k*100 seconds of data
            if data_format=='hdf5':
                out_dataset = TimeSeries.read(source=pths, start=start, format='hdf5.losc', **kwargs)
            elif data_format=='gwf':            
                out_dataset = TimeSeriesDict.read(source=pths, channels=channels, nproc=nproc, dtype=np.float64, **kwargs)            
              
        return out_dataset
    
    @staticmethod
    def read_gwdata_gwosc_remote(start, end, ifo='V1', data_format="hdf5", rate='4k', **kwargs):
        """
        Read GWOSC data from remote host server, which is by default: host='https://www.gw-openscience.org'
        This method is based on GWpy ``fetch_open_data``
        
        Parameters
        ----------
        ifo : str
            Either ``'L1'``, ``'H1'`` or ``'V1'``, the two-character prefix of the IFO in which you are interested
        start : LIGOTimeGPS, float, str, optional
            Starting gps time where to find the frame files. Default: 10 seconds ago
        end : 
            Stop
        name : str
            Name to give to this dataset
        data_format : hdf5 or gwf
            Data format
        **kwargs
            Any other keyword arguments are passed to the ``TimeSeries.fetch_open_data`` method of GWpy. Refer to `the documentation <https://gwpy.github.io/docs/stable/api/gwpy.timeseries.TimeSeries.html#gwpy.timeseries.TimeSeries.fetch_open_data>`_ for more details
            
        Returns
        -------
        gwpy.timeseries.TimeSeries
        
        """
        if rate in ('4k', 4096):
            sample_rate = 4096
        elif rate in ('16k', 16384):
            sample_rate = 16384
        else:
            raise ValueError("Inconsistent 'rate' parameter for gwosc!!! It must be either '4k' or '16k'.")
                 
        TS = TimeSeries.fetch_open_data(ifo, start, end, format=data_format,
                                        sample_rate=sample_rate, **kwargs)     
        TS.sample_rate = sample_rate
        return TS       

    def write_gwdama(self, filename=None, compression="gzip"):
        """
        Method to write the dataset into an hdf5 file. It preserves the hierarchical structure, of course, and all the attributes as metadata.
        
        Parameters
        ----------
        filename : str, optional
            Name of the output file. Default: ``output_gwdama_{}.h5'.format(self.['time_stamp'])``
        compression : str, optional
            Compression level. Default ``'gzip'``. Refer to the `Compression filter documentation <https://docs.h5py.org/en/stable/high/dataset.html#lossless-compression-filters>`_ of ``h5py`` for further details.

        """

        # defaut name
        m_ds = {}
        if not filename:
            filename = 'output_gwdama_{}.h5'.format(self.attrs['time_stamp'])

        if isfile(filename):
            warn('WARNING!! File already exists.')
        creation_time = str(time.strftime("%y-%m-%d_%Hh%Mm%Ss", time.localtime()))

        with h5py.File(filename, 'w') as out_hf:
            out_hf.attrs["time_stamp"] = creation_time
            for a, val in self.attrs.items():
                if a != "time_stamp":
                    out_hf.attrs[a] = val
            for ki in self.keys():
                self.copy(ki,out_hf)

    @staticmethod
    def find_gwf(start=None, end=None, ffl_spec="V1raw", ffl_path=None, gwf_path=None):
        """Fetch and return a list of GWF file paths corresponding to the provided gps time interval.
        Loading all the gwf paths of the data stored at Virgo is quite time consuming. This should be
        done only the first time though. Anyway, it is impossible to be sure that all the paths
        are already present in the class attribute gwf_paths wihout loading them again and checking if
        they are present. This last part should be improved in order to speed up the data acquisition. 
        
        Parameters
        ----------
        start : LIGOTimeGPS, float, str, optional
            starting gps time where to find the frame files. Default: 10 seconds ago
            
        end : LIGOTimeGPS, float, str, optional
            ending gps time where to find the frame file. If ``start`` is not provided, and the default
            value of 10 secods ago is used instead, `end` becomes equal to ``start``+5. If ``start`` is
            provided but not ``end``, the default duration is set to 5 seconds as well
            
        ffl_spec : str, optional
            Pre-encoded specs of the ffl file to read. Available options are: ``V1raw`` (default) for Virgo raw data on farm, ``V1trend``, for data sampled at 1Hz on farm, ``V1trend100`` for 0.01 Hz data on farm, ``H1`` and ``L1`` on farm, ``V1O3a``, ``H1O3a`` and ``L1O3a`` archived from O3a, ``Unipi_arch`` and ``Unipi_O3`` on Unipi servers. The latter are reachable only from "farmrda1" machines
            
        ffl_path : str, optional
            Alternative to  ``ffl_specs``: if the path to a local ffl file is available, the gwf corresponding to the specified
            gps interval are read from it and ``ffl_specs`` is ignored.                  
            
        gwf_path : str, optional
            Altenative to ffl files. It provides a path to a repository (also nested ones) where to look for gwf files. 
            
        Returns
        -------
        gwf_paths : `list`
            List of paths to the gwf file in the provided interval.
            
        """
        data_format = 'gwf'
        
        # 0) Initialise some values if not provided
        if not start:
            start = to_gps('now')-10
            end = start + 5          # Overwrite the previous 'end'
            warn('Warning! No gps_start provided. Changed to 10 seconds ago, and 5 seconds of duration.')
        else:
            start = to_gps(start)
            
        if not end:
            end = start+5
            warn('Warning! No gps_end provided. Duration set to 5 seconds.')     
        else:
            end = to_gps(end)
        
        # Get a list of gwf files. This can be done searching a path or reading an ffl file
        # A) Create a list from the gwf path
        if gwf_path:
            gwf_list = glob(join(gwf_path,f'*.{data_format}'))        
        
            gwf_dict = {int(basename(k).split('-')[-2]): {'path': k,
                                                         'len': int(splitext(basename(k).split('-')[-1])[0]),
                                                         'stop': int(splitext(basename(k).split('-')[-1])[0]) + int(basename(k).split('-')[-2])}
                        for k in gwf_list}
        # B) Obtain the list from ffl files
        else:
            if ffl_path:
                ffl = ffl_path
            else:            
                # Find where to fetch the data
                # Virgo
                if ffl_spec=="V1raw":
                    ffl = ffl_paths.V1_raw
                elif ffl_spec=="V1trend":
                    ffl = ffl_paths.V1_trend
                elif ffl_spec=="V1trend100":
                    ffl = ffl_paths.V1_trend100
                # at UniPi
                elif ffl_spec=="Unipi_O3":
                    ffl = ffl_paths.unipi_O3
                elif ffl_spec=="Unipi_arch":
                    ffl = ffl_paths.unipi_arch

                # O3a
                elif ffl_spec=="V1O3a":
                    ffl = ffl_paths.V1_O3a
                elif ffl_spec=="H1O3a":
                    ffl = ffl_paths.H1_O3a
                elif ffl_spec=="L1O3a":
                    ffl = ffl_paths.L1_O3a    

                # LIGO data from CIT
                # >>>> FIX: multiple frame <<<<
                elif ffl_spec=="H1":
                    if start<(to_gps('now')-3700):
                        ffl = ffl_paths.H1_older
                    elif start>(to_gps('now')-3600):
                        ffl = ffl_paths.H1_newer
                    else:
                        # <------ Fix reading from eterogeneous frames ----->
                        warn("Warning!!! Data not available online and not stored yet")
                elif ffl_spec=="L1":
                    if end<(to_gps('now')-3700):
                        ffl = ffl_paths.L1_older
                    elif end>(to_gps('now')-3600):
                        ffl = ffl_paths.L1_newer
                    else:
                        # <------ Fix reading from eterogeneous frames ----->
                        warn("Warning!!! Data not available online and not stored yet")        
                else:
                    raise ValueError("ERROR!! Unrecognised ffl spec. Check docstring")            

            # 1) Get the ffl (gwf list) corresponding to the desired data frame
            with open(ffl, 'r') as f:
                content = f.readlines()
                # content is a list (with hundreds of thousands of elements) of strings
                # containing the path to the gwf, the gps_start, the duration, and other
                # floats, usually equals to zero.
            content = [x.split() for x in content]

            # Make a dictionary with start gps time as key, and path, duration, and end as vlas.
            gwf_dict = {round(float(k[1])): {'path': k[0],
                                             'len': int(float(k[2])),
                                             'stop': round(float(k[1]) + int(float(k[2])))}
                        for k in content}

        # 2)
        mindict = {k: v for k, v in gwf_dict.items() if k <= start}
        try:
            minvalue = max(mindict.keys())
        except ValueError:
            raise ValueError("ERROR!! No GWF file found. Provided gps_start is before the beginning of the ffl.")            
        maxdict = {k: v for k, v in gwf_dict.items() if k >= start and end <= v['stop']}
        try:
            maxvalue = min(maxdict.keys())
        except ValueError:
            raise ValueError("ERROR!! No GWF file found. Select new gps time interval or try another frame.")            
            
        gwf_paths = [v['path'] for k, v in gwf_dict.items() if k >= minvalue and k <= maxvalue and v['path'].endswith(f'.{data_format}')]

        return gwf_paths
    
    @classmethod
    def read_from_virgo(cls, channels, start=None, end=None, nproc=1, crop=True, **kwargs):
        """This method reads GW data from GWFs, fetched with the ``ffind_gwf`` method,
        and returns a TimeSeriesDictionary object filled with data.
        
        Parameters
        ----------
        channels : list of strings
            List with the names of the Virgo channels whose data that should be read.
            Example: channels = ['V1:Hrec_hoft_16384Hz', 'V1:LSC_DARM']
        
        start : LIGOTimeGPS, float, str, optional
            starting gps time where to find the frame files. Default: 10 seconds ago
            
        end : LIGOTimeGPS, float, str, optional
            ending gps time where to find the frame file. If `start` is not provided, and the default
            value of 10 secods ago is used instead, `end` becomes equal to `start`+5. If `start` is
            provided but not `end`, the default duration is set to 5 seconds as well
                   
        nproc : int, optional
            Number of precesses to use for reading the data. This number should be smaller than
            the number of threads that the machine is hable to handle. Also, remember to
            set it to 1 if you are calling this method inside some multiprocessing function
            (otherwise you will spawn an 'army of zombie'. Google it). The best performances
            are obtained when the number of precesses equals the number of gwf files from to read from.
            
        crop : bool, optional
            For some purpose, it can be useful to get the whole content of the gwf files
            corresponding to the data of interest. In this case, set this parameter as False.
            Otherwise, if you prefer the data cropped accordingly to the provided gps interval
            leave it True.
            
        kwargs : dict, optional
            It contains keyword arguments to pass to ``find_gwf`` method, in particular ``ffl_spec``, ``ffl_path``, or ``gwf_path``
            and those for ``TimeSeries.read(...)``. Refer to the corresponding documentation for more details.
            
        Returns
        -------
        outTSD : TimeSeriesDict object
            Dictionary of TimeSeries corresponding to the specifications provided in the input parameters.
        """

        if isinstance(channels, str):
            channels = [channels]
        
        # Find the paths to the gwf's
        pths = cls.find_gwf(start=start, end=end, ffl_spec=kwargs.get("ffl_spec","V1raw"),
                            ffl_path=kwargs.get('ffl_path'), gwf_path=kwargs.get('gwf_path'))
        
        kwargs.pop('ffl_spec',None)
        kwargs.pop('ffl_path',None)
        kwargs.pop('gwf_path',None)
        
        # If data are read from just one gwf, crop it immediately
        if len(pths)==1 and crop:
            outTSD = TimeSeriesDict.read(source=pths, channels=channels, start=start, end=end,
                            nproc=nproc, dtype=np.float64, **kwargs)
        elif not crop:
            outTSD = TimeSeriesDict.read(source=pths, channels=channels, nproc=nproc, dtype=np.float64, **kwargs)

        elif len(pths)>1:
            outTSD = TimeSeriesDict.read(source=pths, channels=channels, nproc=nproc, dtype=np.float64, **kwargs)
            outTSD = outTSD.crop(start=to_gps(start), end=to_gps(end))
        else:
            # Return whole frame files: k*100 seconds of data
            outTSD = TimeSeriesDict.read(source=pths, channels=channels, nproc=nproc, dtype=np.float64, **kwargs)

        if len(outTSD)==1:
            outTSD = next(iter(outTSD.values()))
        return outTSD

    
    def from_TimeSeries(self, TS, dts_key=None, **kwgs):
        """
        Import into the current instance of :class:`~gwdama.io.GwDataManager` the TimeSeries or TimeSeriesDict of GWpy passed as an argument ot this method.
        
        Parameters
        ----------
        TS : `TimeSeries <https://gwpy.github.io/docs/stable/api/gwpy.timeseries.TimeSeries.html#gwpy.timeseries.TimeSeries>`_ or `TimeSeriesDiuct <https://gwpy.github.io/docs/stable/api/gwpy.timeseries.TimeSeries.html#gwpy.timeseries.TimeSeriesDict>`_
            GWpy object to import in :ref:`index:GWdama`
        dts_key : str, optional
            If ``TS`` is an instance of `TimeSeries <https://gwpy.github.io/docs/stable/api/gwpy.timeseries.TimeSeries.html#gwpy.timeseries.TimeSeries>`_, this parameter corresponds to the name to give to the :class:`~gwdama.io.Dataset` added to the current instance of :class:`~gwdama.io.GwDataManager`. If ``TS`` is a `TimeSeriesDiuct <https://gwpy.github.io/docs/stable/api/gwpy.timeseries.TimeSeries.html#gwpy.timeseries.TimeSeriesDict>`_, this is the name of the group where to create a :class:`~gwdama.io.Dataset` for every item of ``TS``. In this case, their names will be the keys of ``TS``
        
        **kwgs : dict, optional
            Other parameters that can be passed to the `.create_dataset method of h5py <https://docs.h5py.org/en/stable/high/group.html?highlight=create_dataset#h5py.Group.create_dataset>`_. This includes details on the compression format of this data: *e.g.* ``compression="gzip", compression_opts=9``. Refer to the documentation of h5py for further details
        
        Returns
        -------
         : Dataset or Group
            Dataset or Group corresponding to the imported `TimeSeries <https://gwpy.github.io/docs/stable/api/gwpy.timeseries.TimeSeries.html#gwpy.timeseries.TimeSeries>`_ or `TimeSeriesDiuct <https://gwpy.github.io/docs/stable/api/gwpy.timeseries.TimeSeries.html#gwpy.timeseries.TimeSeriesDict>`_

        See Also
        --------
        gwdama.io.Dataset.to_TimeSeries
        """
        
        if isinstance(TS, TimeSeriesDict):
            dts_key = dts_key or 'TS'
            for k, ts in TS.items():
                self.from_TimeSeries(ts, dts_key=f"{dts_key}/{k}", **kwgs)
            
        elif isinstance(TS, TimeSeries):
            dts_key = dts_key or 'TS'
            if dts_key in self:
                raise ValueError("Provided 'dts_key' already present in this dama. Please, pass a new name for it")
            self.create_dataset(name=dts_key, data=TS.value, **kwgs)
            
            # Add some attributes
            dts = self[dts_key]
            dts.attrs['t0'] = TS.t0.value
            dts.attrs['sample_rate'] = TS.sample_rate.value
            dts.attrs['unit'] = str(TS.unit)
            try:
                dts.attrs['channel'] = TS.channel.value
            except AttributeError:
                dts.attrs['channel'] = ''

        return self[dts_key]

#     def from_DataFrame(self, df, dts_key=None, **kwgs):
#         """
#         WORK in progress
        
#         Import into the current instance of :class:`~gwdama.io.GwDataManager` 
 
#         """
#         pass
        
#         if isinstance(TS, TimeSeriesDict):
#             dts_key = dts_key or 'TS'
#             for k, ts in TS.items():
#                 self.from_TimeSeries(ts, dts_key=f"{dts_key}/{k}", **kwgs)
            
#         elif isinstance(TS, TimeSeries):
#             dts_key = dts_key or 'TS'
#             if dts_key in self:
#                 raise ValueError("Provided 'dts_key' already present in this dama. Please, pass a new name for it")
#             self.create_dataset(name=dts_key, data=TS.value, **kwgs)
            
#             # Add some attributes
#             dts = self[dts_key]
#             dts.attrs['t0'] = TS.t0.value
#             dts.attrs['sample_rate'] = TS.sample_rate.value
#             dts.attrs['unit'] = str(TS.unit)
#             try:
#                 dts.attrs['channel'] = TS.channel.value
#             except AttributeError:
#                 dts.attrs['channel'] = ''

#         return self[dts_key]
