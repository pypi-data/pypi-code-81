import os
import datetime
import pandas as pd

from tqdm import tqdm

from thanetwffapi.Time import Time


def feature_mean_df(df, mean):
    df.set_index('Timestamp', inplace=True)
    df = df.groupby('Foundation').resample(mean).mean()

    df.reset_index(inplace=True)
    df.set_index('Timestamp', inplace=True)

    # Fixing NaN
    # pad = copy value above and repeat
    # linear = continue with the same steps as earlier data points
    df.interpolate(method='pad', inplace=True)

    return df


def handle_out_of_bounds(df, action):
    channel_list = [ch for ch in df.columns if ch.startswith('Ch')]

    for ch in channel_list:
        idx_10 = df.loc[df[ch] == -10010].index
        idx_20 = df.loc[df[ch] == -10020].index

    if action == 'remove':
        df.drop(index=idx_10, inplace=True)
        df.drop(index=idx_20, inplace=True)
    elif action == 'mean':
        df[ch].replace([-10010, -10020], df[ch].mean(), inplace=True)
    elif isinstance(action, int):
        df[ch].replace([-10010, -10020], action, inplace=True)

    return df


class SGData:
    def __init__(self):
        pass

    def set_datapath(self, datapath) -> None:
        self.datapath = datapath

    def set_sg_folder_path(self, sg_folders: tuple) -> None:
        self.sg_folders = sg_folders

    def set_name(self, name: tuple) -> None:
        """ Method setting TEST for query

        :param name: name
        :type name: tuple of str
        :return: None
        """
        self.name = name

    def set_foundation(self, foundation: tuple) -> None:
        self.foundation = foundation

    def set_timestamp(self, timestamp: int) -> None:
        self.timestamp = timestamp

    def set_t_start(self, t_start: str) -> None:
        self.t_start = t_start

    def set_t_end(self, t_end: str) -> None:
        self.t_end = t_end

    def set_channels(self, channels: tuple) -> None:
        self.channels = channels

    def set_files(self, files: list) -> None:
        self.files = files

    def set_mean(self, mean: str) -> None:
        self.mean = mean

    def set_oob(self, oob) -> None:
        self.oob = oob

    def set_df_list(self, df_list: list) -> None:
        self.df_list = df_list

    def set_df(self, df: pd.DataFrame) -> None:
        self.df = df


class SGQuery:
    """ Builder class to strain gauge data

    - Example
    >>> sg_df = SGQuery(datapath).with_localdata(datapath). \
        .with_name(test_file.txt).with_foundation("E07")
    """

    _msg = 'SGQuery Queries files based on parameters, and returns a pandas DataFrame ' \
           'with selected corrections for timestamp and channels corrections.'

    def __init__(self):
        self.sg = SGData()

    def __getattr__(self, attr):
        """ Method for checking if query syntax is correct, raises error if syntax is violated
        """
        if attr not in ['with_local_data', 'with_name', 'with_foundation', 'with_mean', 'feature_mean_df'
                        'select_files', 'correct_channels', 'to_df']:
            print(self)
            raise AttributeError('{}() is not supported. \n{}'
                                 '\n\n\n{}'.format(attr, self, self._msg))

    def __repr__(self):
        """ Method displaying hint for available next steps

        :return: message with hint for available options
        """
        if hasattr(self.sg, 'files'):
            return ('Files are queried. Select channel corrections, and/or timestamp correction: '
                    '[correct_channels_microstrain(), correct_channels_realvalue(), correct_timestamp()].\n'
                    'Use .to_df() to get an unaltered dataframe.\n'
                    'After selected correction, use to_df() to return the corrected DataFrame.\n'
                    'Ex: SGQuery().using_db("{}").with_name("*").query_files()'
                    '.correct_channels_microstrain().correct_timestamp().to_df()'.format(self.sg.datapath))
        if hasattr(self.sg, 'name') or hasattr(self.sg, 'foundation'):
            return ('Parameters are selected for querying, Select query_files() '
                    'or select other parameters for querying [with_name, with_foundation, with_duration].\n'
                    'Ex: SGQuery().using_db("{}").with_name("*").query_files()'.format(self.sg.datapath))
        if hasattr(self.sg, 'datapath'):
            return ('Datapath selected, choose query parameters '
                    '[with_name, with_foundation, with_duration]\n'
                    'Ex: SGQuery().using_db("{}").with_name("*")'.format(self.sg.datapath))
        else:
            return ('Select db with using_db(Datapath)\n '
                    'Ex: SGQuery().using_db("../SG data")')

    def shortcut(self, datapath):
        # get current path
        # path_gf = '../SG_GF'
        # self.using_db(datapath).with_name('*').query_files().correct_channels('microstrain', path_gf)
        pass

    def using_db(self, datapath):
        """ Method setting datapath for db used to query files
        :param datapath: string path to SG files
        """
        self.sg.set_datapath(datapath)
        sg_folder_list = [os.path.join(datapath, f) for f in os.listdir(datapath) if '_structure' in f]
        self.sg.set_sg_folder_path(sg_folder_list)
        return self

    def with_name(self, *name):
        """ Method selecting file names to query
        :param name: name of files
        """
        self.sg.set_name(name)
        return self

    def with_foundation(self, *foundation):
        """ Method setting foundation type for query
        :param foundation: name of faundations, as string
        :return:
        """
        self.sg.set_foundation(foundation)
        return self

    def with_timestamp(self, *timestamp):
        print('NOT IMPLEMNTED')
        return self

    def with_duration(self, t_start=None, t_end=None, duration=None):

        t_start, t_end = Time.convert_time_duration(t_start, t_end)

        self.sg.set_t_start(t_start)
        self.sg.set_t_end(t_end)
        return self

    def with_channels(self, *channels):
        for ch in channels:
            if ch <= 0 or ch > 56:
                raise ValueError('Error: Select channel betwenee 1 and 56, channel {} does not exist'.format(ch))
        self.sg.set_channels(channels)
        return self

    def with_mean(self, mean):
        self.sg.set_mean(mean)
        return self

    def remove_out_of_bounds(self):
        self.sg.set_oob('remove')
        return self

    def set_out_of_bounds(self, value):
        if isinstance(value, int) or value == 'mean':
            self.sg.set_oob(value)
        else:
            raise ValueError('Error, value not valid {}. Value can be integer, or the string "mean"'.format(value))
        return self

    def query_files(self, skip_10_rows=True, **kwargs):
        """ Query files from datapath

        :return: self
        """
        files = []

        skip_files = kwargs['skip_files'] if 'skip_files' in kwargs else 1

        if hasattr(self.sg, 'name'):
            files = files + self.selecting_files_name(skip_files)
        if hasattr(self.sg, 'foundation'):
            files = files + self.selecting_files_foundation(skip_files)
        if hasattr(self.sg, 'timestamp'):
            files = files + self.selecting_files_timestamp()
        if hasattr(self.sg, 't_start') and hasattr(self.sg, 't_end'):
            if (hasattr(self.sg, 'name')) or (hasattr(self.sg, 'foundation')):
                time_files = self.selecting_files_duration(skip_files)
                files = list(set(time_files) & set(files))
            else:
                files = files + self.selecting_files_duration(skip_files)

        # Prevent Duplication
        print('Querying {} files: '.format(len(files)))

        files = list(set(files)) # Remove uplicates
        self.sg.set_files(files)
        self.files_to_df(skip_10_rows)

        df = self.concatinate_dataframes()
        self.sg.set_df(df)

        if hasattr(self.sg, 'oob'):
            handle_out_of_bounds(self.sg.df, self.sg.oob)
        else:
            handle_out_of_bounds(self.sg.df, 'remove')

        if hasattr(self.sg, 'mean'):
            self.correct_timestamp()
            self.sg.df = feature_mean_df(self.sg.df, self.sg.mean)

        return self

    def correct_channels_microstrain(self):
        """ Corrects the 56 channels from 16bit A/D Value to microstrain
        """
        a, b = 0.5127031, -16800

        file_dir = os.path.dirname(__file__)
        sg_gf_dir = os.path.join(file_dir, 'SG_GF')

        foundation_gf_dict = {}  # Adding dictionary for foundation - lookup saves time, no need to re-read csv

        foundation_list = [foundation for foundation in self.sg.df['Foundation'].unique()]

        for foundation in foundation_list:
            try:
                df = self.sg.df.loc[self.sg.df['Foundation'] == foundation]

                ch_cols = [col for col in df if col.startswith('Ch')]

                if foundation in foundation_gf_dict:
                    gf_df = foundation_gf_dict[foundation]
                else:
                    gf_df = self.foundation_channel_gf(foundation, sg_gf_dir)
                    foundation_gf_dict[foundation] = gf_df

                for col in ch_cols:
                    ch_gf = (float(gf_df.loc[(gf_df['Channel'] == int(col[-2:])), 'GF']))
                    self.sg.df.loc[self.sg.df['Foundation'] == foundation, col] = \
                        df[col].apply(lambda x: ((a * x) + b) / ch_gf)

            except Exception as e:
                print('Error: Cannot correct channels to Micro Strain: {}'.format(e))

        return self

    def correct_channels_realvalue(self):
        """ Corrects the 56 channels from 16bit A/D Value to either realvalue
        """
        a, b = 0.5127031, -16800
        foundation_list = [foundation for foundation in self.sg.df['Foundation'].unique()]

        for foundation in foundation_list:
            try:
                df = self.sg.df.loc[self.sg.df['Foundation'] == foundation]

                ch_cols = [col for col in df if col.startswith('Ch')]

                for col in ch_cols:
                    self.sg.df.loc[self.sg.df['Foundation'] == foundation, col] = \
                        df[col].apply(lambda x: (a * x) + b)
            except Exception as e:
                print('Error: Cannot correct channels to Real Value')
        return self

    def correct_channels_advalue(self):
        """ No Correction to the 56 channels from 16bit A/D Value
        :param value: [microstrain, realvalue]
        :return:
        """
        return self

    def correct_timestamp(self):
        if ('Timestamp' in self.sg.df) or (isinstance(self.sg.df.index, pd.DatetimeIndex)):
            return self

        try:
            self.sg.df.insert(0, 'Timestamp', 0, False)  # Dont need this, but it places Timestamp as the first column
            self.sg.df['Timestamp'] = self.sg.df['Time'].apply(lambda x: datetime.datetime.utcfromtimestamp((x - 25569) * 86400.0))
            self.sg.df.drop(['Time', 'mS'], axis=1, inplace=True)
        except Exception as e:
            print('Error: Could not convert time to timestamp')

        return self

    def correct_timestamp_with_ms(self):
        # TODO: Use both ms and timestamp to create a more accurate timestamp
        print('this is not done!')
        # s = 1199.479 / 60
        # t = 0.991316666666666 * 60

        return self

    def sort_timestamp(self):
        self.sg.df.sort_index(inplace=True)

        return self

    def to_df(self):
        if not (isinstance(self.sg.df.index, pd.DatetimeIndex)) and 'Timestamp' in self.sg.df.columns:
            self.sg.df.set_index('Timestamp', inplace=True)

        return self.sg.df

    def to_csv(self):
        print('Exporting to csv')

    # =========================== HELPER FUNCTIONS - MOVE OUT ===============================
    def concatinate_dataframes(self):
        concat_df = pd.concat([df for df in self.sg.df_list], axis=0, ignore_index=True)
        self.sg.df_list[:] = []
        return concat_df

    def selecting_all_files(self, skip):
        print('Query all files in datapath {}'.format(self.sg.datapath))
        files = []
        try:
            for i in range(len(self.sg.sg_folders)):
                files = files + [os.path.join(self.sg.sg_folders[i], f) for f in
                                 os.listdir(self.sg.sg_folders[i])[0::skip]]
        except AttributeError as e:
            print('Error querying all files')

        return files

    def selecting_files_name(self, skip):
        files = []
        try:
            if '*' in self.sg.name:
                files = self.selecting_all_files(skip)
            else:
                for i in range(len(self.sg.sg_folders)):
                    files = files + [os.path.join(self.sg.sg_folders[i], f) for f in self.sg.name
                                     if os.path.isfile(os.path.join(self.sg.sg_folders[i], f))]
        except AttributeError as e:
            print('Error querying files based on name')

        return files

    def selecting_files_foundation(self, skip):
        files = []
        try:
            if '*' in self.sg.foundation:
                files = self.selecting_all_files(skip)
            else:
                foundation_folders = []
                for folder in self.sg.foundation:
                    foundation_folders = foundation_folders + [f for f in self.sg.sg_folders if folder in f]
                for i in range(len(foundation_folders)):
                    files = files + [os.path.join(foundation_folders[i], f) for f
                                     in os.listdir(foundation_folders[i])[0::skip]]
        except AttributeError as e:
            print('Error querying files based on foundation')

        return files

    def selecting_files_timestamp(self):
        pass

    def selecting_files_duration(self, skip):
        print('Selecting Files between {} and {}'.format(self.sg.t_start, self.sg.t_end))
        files = []
        try:
            for i in tqdm(range(len(self.sg.sg_folders))):

                files = files + [os.path.join(self.sg.sg_folders[i], f) for f in os.listdir(self.sg.sg_folders[i])[0::skip]
                                 if Time.validate_date_file(f, self.sg.t_start, self.sg.t_end)]
        except AttributeError as e:
            print('Error querying files based on name')

        return files

    def foundation_channel_gf(self, channel_name, path):
        file_name = channel_name + '_GF.csv'
        file = os.path.join(path, file_name)
        df = pd.read_csv(file)

        return df

    def files_to_df(self, skip_10_rows):
        """ Takes select SG text files (from select_files function) with SG Data, and converts it to one Pandas DataFrame

        :returns:
        """
        dfs = []
        if len(self.sg.files) == 0:
            raise ValueError('Cannot query requested files, in path{}'.format(self.sg.datapath))
        for path in tqdm(self.sg.files):
            file = open(path, 'r')
            o_f = file.readlines()

            # Retrive relevant info from header & Find Start of data columns
            header_info = self.retrive_header_info(path)
            idx_start = self.sg_table_start(path)

            # Column Names
            try:
                col = o_f[idx_start - 1].split()
                col[1] = col[1] + col[2]
                col[2] = 'mS'
            except TypeError as e:
                print("Error: {}\n"
                      "File {} not on correct format".format(e, path))
                continue

            # Retrieve Column Data from files, and create DataFrame
            rows = o_f[idx_start + 10::10] if skip_10_rows else o_f[idx_start + 1:]
            row_list = [row.split() for row in rows]

            if hasattr(self.sg, 'channels'):
                try:
                    # Removes the Rel.time column (col 1)
                    info_columns = [0, 2]

                    # if [0,1,2] as info_columns is used (including Rel.time) - instead of [0, 2] -,
                    # then remember to subtract -1 to (ch + len(info_columns))
                    selected_column_number = info_columns + [ch + len(info_columns) for ch in self.sg.channels]

                    col = [col[c] for c in selected_column_number]

                    for i in range(len(row_list)):
                        row_list[i] = [row_list[i][col] for col in selected_column_number]
                except IndexError as e:
                    print("Error, file {} don't have requested channels".format(path))
                    continue

            try:
                df = pd.DataFrame(row_list, columns=col)
                df = df.apply(pd.to_numeric)
            except Exception as e:
                print('Could not turn file {} into dataframe'.format(path))
                continue

            # Insert Additional Columns [TODO: Add insert file_name?]
            df.insert(0, 'Foundation', header_info[0], False)

            dfs = dfs + [df]

        self.sg.set_df_list(dfs)

        return self

    def sg_table_start(self, path):
        table_marker = '-----'

        # TODO : NEEDS ERROR HANDLING, WHAT IF NO TABLE_MARKER FOUND?
        with open(path, 'r') as f:
            for index, line in enumerate(f):
                if table_marker in line:
                    return index

        # TODO : ERROR - return something?
        # print('ERROR: File [{}] is not on standard format!'.format(path))
        return self

    def retrive_header_info(self, path):
        """ Retrives selected information from the header of SG Data Files.

        :arg
        """
        header_info = []
        foundation_marker = 'Foundation '

        # Find start of table
        # TODO: Fix retrive header info mess ...
        with open(path, 'r') as f:
            for index, line in enumerate(f):
                if foundation_marker in line:
                    pos = (line.find('Foundation '))
                    header_info.append(line[pos + 11:pos + 14])
                if index == 13:
                    break

        return header_info
