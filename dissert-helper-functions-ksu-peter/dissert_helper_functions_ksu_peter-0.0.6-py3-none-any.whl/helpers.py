class dbConnect():
    def __init__(self, sqlite_db="sqlite:////home/jupyter-pomkos/[databases]/dissert.db"):
        '''
        Class to connect to sqlited, then load and list tables
        
        input
        -----
        sqlite_db: str
            Location of database
        '''
        import sqlalchemy as sq
        engine = sq.create_engine(sqlite_db)
        cnx = engine.connect()
        meta = sq.MetaData()
        meta.reflect(engine)
        
        self.cnx = cnx
        self.meta = meta
        
    def save_files_to_db(self, recursive_loc = 'data'):
        '''
        Saves csv files to db. Saved for posterity
        
        input
        -----
        recursive_loc: str
            Location of parent folder where files are. Recursively includes all csv files within child folders of parent folder.
        '''
        import pandas as pd
        import sqlalchemy as sq
        
        files = os.listdir(recursive_loc)
        try:
            for file in files:
                if '.csv' in file:
                    df=pd.read_csv(f'data/{file}')
                    new_name = file.replace(".csv","")
                    df.to_sql(new_name,self.cnx, if_exists='replace', index=False)
            print("All files saved to db")
        except e as Exception:
            print(e)
        
    def load_table(self, table_name):
        'Loads a table from db'
        import sqlalchemy as sq
        import pandas as pd
        table = self.meta.tables[table_name]
        resultset = self.cnx.execute(sq.select([table])).fetchall()
        df = pd.DataFrame(resultset)
        df.columns = table.columns.keys()
        return df
    
    def list_tables(self):
        'Lists all tables in db'
        return list(self.meta.tables.keys())

def balancer(dataframe):
    '''
    Deprecated.
    
    Removes participants 2,6,7 so dataset can be analyzed with RM ANOVA. Only useful for Robert dataset.
    '''
    new_df = dataframe[(dataframe['id']!='pdsmart002')&
                       (dataframe['id']!='pdsmart006')&
                       (dataframe['id']!='pdsmart007')]
    return new_df

def cadence_extractor(dataframe, id_sess, side = 'head'):
    '''
    Checks where the cadence first hits 75 < cad < 80 in the first (if head) or last (if tail) rows.
    Purpose: to figure out when warmups first ended and cooldowns first began.
    
    input
    -----
    dataframe: Dataframe
    id_sess: list
        list of strings of participant codes
    side: string
        'head': will check the cadence of first (5*(len(dataframe))) rows
        'tail': will check the cadence of last (5*(len(dataframe))) rows
        
    return
    -----
    dictionary of (partsess: [index,mean]), which is the location where cadence first hit 75 < cad < 80
        partsess: str
            participant/session filter
        [index, mean, st_dev]: list
            List of values
        index: int
            The row's value cadence first became 75 < row < 80
        mean: float
            Mean of head or tail
        st_dev: float
            Standard deviation of head or tail
    '''
    import math # check for nan
    import numpy as np
    head = {}
    tail = {}
    for p in id_sess:
        cad_index = dataframe.columns.get_loc('cadence') # get location of cadence column
        result = dataframe[(dataframe['id_sess']==p)].reset_index(drop=True)
        result['cadence'] = result['cadence'].astype('float')
        ending = round(len(result)/3)
        for i in range(1,ending):
            if side == 'head':
                cad_loc = 5*i
                cut_result = result.iloc[:cad_loc,cad_index]
                cad = cut_result.iloc[-1]
                mean_num = result.iloc[:cad_loc,cad_index].mean()
                st_dev = result.iloc[:cad_loc,cad_index].std()
                if (cad > 75) & (cad < 90):
                    head[f'{p}'] = [cad_loc, mean_num, st_dev]
                    break
                elif np.isnan(mean_num):
                    head[f'{p}'] = mean_num
                    break
            elif side == 'tail':
                cad_loc = -5*i
                cut_result = result.iloc[cad_loc:,cad_index]
                cad = cut_result.iloc[1]
                mean_num = result.iloc[cad_loc:,cad_index].mean()
                st_dev = result.iloc[cad_loc:,cad_index].std()
                if (cad > 70) & (cad < 85):
                    tail[f'{p}'] = [cad_loc, cad, st_dev]
                    break
                elif np.isnan(mean_num):
                    tail[f'{p}'] = mean_num
                    break
    if side == 'head':
        return head
    elif side == 'tail':
        return tail

class CleanOldDf:
    '''
    Cleans up an unprocessed bike DF made up of several dynamic bike outputs (that was made with dynamic biking script).
    Must have columns: date, time, hr, cadence, power, id, session in that order.
    
    count_row true:
        Adds integers for each row, starting over at each session for each participant. Represents seconds. 
    date_time true:
        Combines date and time columns in one date column. 
    In both cases:
        Converts date to datetime; id and session to category.
    '''
    
    def __init__(self, df):
        import pandas as pd
        # Format the columns
        df.columns = list(pd.Series(df.columns).str.lower())
        df['id'] = df['id'].astype('category') # format column
        df['hr'] = pd.to_numeric(df['hr']) # format column
        df['session'] = df['session'].astype('category') # format column
        self.df = df
        
    def datetime_maker(self, count_row = False):
        '''
        Combines the date and time columns into one datetime column.
        
        input
        -----
        count_row: bool
            True: runs row_counter() function first, then combines the date and time columns
            False: just combines the date and time columns
            
        return
        ------
        df: Dataframe
            The dataframe with date and time combined, columns formatted, rows counted (if count_row=True)
        '''
        import pandas as pd
        # only call row_counter function if count_row = True, then reorder the columns
        if count_row == True:
            df = self.row_counter(maker=True)
            df[['id','session','date','time','seconds','hr','cadence','power']] 
        else:
            df = self.df.copy()
            df = df[['id','session','date','time','hr','cadence','power']]
        # Create date column
        df['date'] = df['date'] + " " + df['time']
        del df['time'] # remove time column
        df['date'] = pd.to_datetime(df['date'])
        return df

    def row_counter(self, maker=False):
        '''
        Adds a new seconds column that restarts from 0 for each participant + session combination
        
        input
        ------
        maker: bool
            If True, assumes the dataframe will be processed through self.datetime_maker next. Will not format date col to datetime.
        return
        ------
        df: Dataframe
            the input df, but with a new column of seconds and all colulmns formatted
        '''
        import pandas as pd
        old_df = self.df.copy()
        # Prepare to separate old_df into dictionary of dfs
        part = list(old_df['id'].unique()) # list of participants
        sesh = list(old_df['session'].unique()) # list of sessions
        sep_dfs = {}
        # Add in time component (each row is 1 second) to each df for each participant + session combination
        for p in part:
            for s in sesh:
                dfx = old_df[(old_df['id'] == p) & (old_df['session'] == s)] # select certain participant + session
                dfx = dfx.reset_index(drop = True) # get rid of the old index
                dfx = dfx.reset_index(drop = False) # create index column with new numbers
                dfx['seconds'] = dfx['index'] # rename column
                del dfx['index'] # remove index column
                sep_dfs[f'{p}_{s}'] = dfx # save into dictionary

        # Turn dictionary into a new df
        keys = sep_dfs.keys() 
        example = list(keys)[0]
        all_columns = list(sep_dfs[example].columns) # grab the columns names
        df = pd.DataFrame(columns = all_columns) # make a new blank df with column names        
        for key in keys:
            df = pd.concat((df, sep_dfs[key])) # concatenate the dfs into one big one
        df = df[['id','session','date','time','seconds','hr','cadence','power']]
        # Format columns
        df['date'] = pd.to_datetime(df['date']) if not maker else df['date']
        df['id'] = df['id'].astype('category')
        df['session'] = df['session'].astype('category')
        df['hr'] = pd.to_numeric(df['hr'])
        df['seconds'] = pd.to_numeric(df['seconds'])
        df = df.reset_index(drop = True) # new index 
        return df

class dateAnalysis:
    def __init__(self, dataframe, session = 'session', date='date'):
        '''
        Includes two functions that will extract the date from each participant, and then finds the elapsed time between sessions.
        
        input
        -----
        dataframe: pd.DataFrame
            Dataframe with at least 'id','date' variables
        session: str
            String with name of variable that contains session numbers
        date: datetime
            Column with all dates
        participant: str
            Column with ids of participants
            
        self.var
        self.date_df: pd.DataFrame
            Dataframe of id, session, and date only
        '''
        self.dataframe = dataframe
        self.session = session
        self.date = date
        
        dataframe['datetime'] = dataframe[date]
        try:
            dataframe['date'] = dataframe['datetime'].apply(lambda x: x.date())
        except:
            print("Looks like date column is already just dates without time")
        dataframe = dataframe.astype({
            'id':str,
            session:str
        })

        date_df = dataframe.groupby(['id',session,'date']).mean().reset_index()[['id',session,'date']]
        date_df = date_df.sort_values(['id','date'])
        date_df = date_df.reset_index(drop=True)
        
        self.date_df = date_df
        print("Now you can use dateAnalysis.date_diff() to find the difference in dates")

    def date_diff(self, dataframe = None, session = 'session', date = 'date', participant='id'):
        '''
        For use after date_finder function

        Returns a new dataframe with sessions as columns and date of occurrance as datapoint for each participant
        Two new columns are included: elapsed (days between first and last sessions, datetime) and 
        elap_int (days between first and last sessions, int)
        
        input
        -----
        dataframe: pd.DataFrame
            Dataframe created by dateAnalysis.date_finder(). If none given, uses self.date_df
        '''
        import pandas as pd
        
        if not dataframe:
            dataframe = self.date_df
        
        list_date = list(dataframe[session].unique()) # date col for each session
        list_date.append('elapsed')
        new_date = pd.DataFrame(columns=list_date,index=dataframe[participant].unique()) # new df of NaNs to fill in
        # extract the start, mid, end dates for each session


        for part in dataframe[participant].unique():
            temp_df = dataframe[dataframe[participant]==part].reset_index(drop=True)
            date_sr = temp_df[date].sort_values()

            for i in range(len(date_sr)):            
                new_date.loc[part,list_date[i]] = date_sr[i]

        new_date['elapsed'] = new_date[list_date[-2]] - new_date[list_date[0]]
        new_date['elap_int'] = new_date['elapsed'].apply(lambda x: str(x)).str.extract('(\d\d?) days')
        self.new_date = new_date
        return new_date
    
    def date_consistent_checker(self, clean_df=None):
        '''
        Checks the number of days elapsed between datetime columns, where the columns are in sequential order

        input
        -----
        clean_df: pd.DataFrame
            Usually created with dateAnalysis.date_diff()
            Sessions must be in own col, each col consisting of datetime.date objects.
        '''
        import pandas as pd
        if type(clean_df) == pd.DataFrame:
            dataframe = clean_df.copy()
        else:
            dataframe = self.new_date.copy()

        for num in range(len(dataframe.columns)-2):
            try:
                dataframe[f"elap{num+2}-{num+1}"] = dataframe[f"session{num+2}"] - dataframe[f"session{num + 1}"]
                dataframe[f"elap_int{num+2}-{num+1}"] = dataframe[f"elap{num+2}-{num+1}"].apply(lambda x: str(x)).str.extract('(\d\d?) days')
                print(f"Finished session{num+1}")

            except Exception as e:
                if 'session' in str(e):
                    print(f"Reached end, no session called {e}")
                else:
                    print("Something bad occurred.")
                    print(e)

        return dataframe

def perc_time_in_col(dataframe, col, threshold = 0, perc = 'greater', id_col='id_sess'):
    '''
    OG purpose: Calculates the percent occurrance of positive `col` values per `id_col`. 
    NOT whether the mean is neg or pos.
    
    input
    -----
    dataframe: pd.DataFrame
    col: str
        Variable of interest to count
    threshold: int
        Number (noninclusive) to consider as threshold
    perc: string
        One of "greater", "lesser", or "equal"
        Determines how to compare all values to the threshold
    id_col: str
        Column participants are identified by
        
    return
    ------
    df_merged: pd.DataFrame
        Each row represents one `id_col`
        Columns are counts of `col` < 0 and perc in negative for each `id_col`
    '''
    try:
        all_count = dataframe.groupby([id_col]).count()[[col]] # count number of lines per id_col

        if perc == 'greater':
            val_ = dataframe[dataframe[col] > threshold] # filter to > threshold
            compare = 'pos'
        elif perc == 'lesser':
            val_ = dataframe[dataframe[col] < threshold] # filter to < threshold
            compare = 'neg'
        else:
            val_ = dataframe[dataframe[col] == threshold] # filter to equal threshold
            compare = f'_{threshold}'

        val_count = val_.groupby([id_col]).count()[[col]] # count number of positive lines per id_col

        df1 = all_count.reset_index() # reset indexes so dataframes can be merged
        df2 = val_count.reset_index()

        df_merged = df2.merge(df1, on=[id_col], suffixes=[f'_{compare}','_all'])
        # calculate and round percent
        df_merged[f'perc_time_in_{compare}'] = round(100*(df_merged[f'{col}_{compare}']/df_merged[f'{col}_all']),2)
        df_merged = df_merged.sort_values(f'perc_time_in_{compare}', ascending=False)
        return df_merged
    except Exception as e:
        print('REMINDER: make sure participant ID and session labels are one variable (ex: id_sess)')
        return e
            
def df_to_dic(dataframe, col1, col2):
    '''
    Takes a dataframe and two columns. Returns a dictionary. Assumes col1 and col2 have a 1:1 ratio of key:value
    
    input
    -----
    col1: str
        The column to use as key
    col2: str
        The column to use as value
    '''
    temp_dic = {}

    for i, row in dataframe.iterrows():
        if row[col1] in temp_dic.keys():
            continue
        else: 
            temp_dic[row[col1]] = row[col2]
    return temp_dic

def dic_to_df(my_dic):
    '''
    Takes a dictionary of dfs, extracts the first df. Appends all other dfs to the first df.
    
    input:
    -----
    my_dic: dic
        Dictionary of dataframes
        
    output:
    ------
    new_df: dataframe
    '''
    import pandas as pd
    new_df = pd.DataFrame(columns= list(my_dic[list(my_dic.keys())[0]].columns))
    for p in list(my_dic.keys()):
        temp_df = my_dic[p]
        new_df = pd.concat([new_df, temp_df])
        new_df = new_df.reset_index(drop=True)
        
    return new_df 
    
def list_maker(dataframe, cat1='id', cat2='session'):
    '''
    Makes a list of all unique objects in a dataframe. Returns 2 lists.

    input
    -----
    cat1: str
        Column that first categoricals are in
    cat2: str
        Column that second categoricals are in
    '''
    participant = list(dataframe[cat1].unique())
    session = list(dataframe[cat2].unique())
    return participant, session

def make_last_cols(s, my_var, my_stat):
    '''
    Creates names for columns in a standard dynamic bike entropy report file.
    
    input
    -----
    s: int
        If none: does not add session to prefix
        If int: session number
    my_var: str
        One of hr, cad, pow
    my_stat: int
        Meant for using in for loop. Can be 1-5 for mean, std, samen, apen, spen respectively
        
    output
    ------
    str
        Name of the column
    '''
    if s == 'none':
        if my_stat == 1:
            return f'{my_var}_mean'
        if my_stat == 2:
            return f'{my_var}_std'
        if my_stat == 3:
            return f'{my_var}_samen'
        if my_stat == 4:
            return f'{my_var}_apen'
        if my_stat == 5:
            return f'{my_var}_spen'
    else:
        if my_stat == 1:
            return f'session{s}_{my_var}_mean'
        if my_stat == 2:
            return f'session{s}_{my_var}_std'
        if my_stat == 3:
            return f'session{s}_{my_var}_samen'
        if my_stat == 4:
            return f'session{s}_{my_var}_apen'
        if my_stat == 5:
            return f'session{s}_{my_var}_spen'
        
def num_scriptor(phrase, script):
    '''
    Turns all numbers into subscripts or superscripts

    input
    -----
    phrase: str
        Any string with digits in it
    script: str
        'sub': creates subscripts
        'sup': creates superscripts
        
    return
    ------
    phrase: str
        String with the digits sub/superscripted
    
    Source: https://stackoverflow.com/a/24392215/
    '''
    if script == 'sub':
        SUB = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")
        return phrase.translate(SUB)
    elif script == 'sup':
        SUP = str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹")
        return phrase.translate(SUP)
    else:
        return 'script must be sub or sup'
    
def plot_corr_triangle(df, output=None,annot=True, figsize=(11,9), **kwargs):
    '''
    Gets the lower half of a correlation dataframe, plots it.
    
    input
    -----
    df: pd.DataFrame
        Dataframe previously run through the pd.DataFrame.corr() functions
    output: str
        Saves the figure as that filename
    annot: bool
        Whether to show correlations in the heatmap
    **kwargs:
        All keywords are passed to sns.heatmap()

    Source: https://stackoverflow.com/a/59173863
    '''
    import numpy as np
    import seaborn as sns
    import matplotlib.pyplot as plt
    
    mask = np.zeros_like(df, dtype=np.bool)
    mask[np.triu_indices_from(mask)] = True

    # Want diagonal elements as well
    mask[np.diag_indices_from(mask)] = False

    # Set up the matplotlib figure
    f, ax = plt.subplots(figsize=figsize)

    # Generate a custom diverging colormap
    cmap = sns.diverging_palette(220, 10, as_cmap=True)

    # Draw the heatmap with the mask and correct aspect ratio
    sns_plot = sns.heatmap(df,mask=mask, cmap=cmap, annot=annot, vmin=-1, vmax=1, center=0,
            square=True, linewidths=.5, cbar_kws={"shrink": .5}, **kwargs)
    plt.yticks(rotation=0)
    # save to file
    if type(output) == str:
        fig = sns_plot.get_figure()
        fig.savefig(output)
    
def plot_box(dataframe, column='cadence', by='id'):
    '''
    Creates basic boxplot

    input
    -----
    x: str
    y: str
    '''
    return dataframe.boxplot(column=column,by=by,rot=45)

def plot_facet_scatter(dataframe, x, y, fac_col, fac_row, sharex=True, sharey=True):
    '''
    Creates facetgrid using seaborn and matplotlib

    input
    -----
    x: str
    y: str
    fac_col: str
        Dataframe col that will serve as col for facet grid
    fac_row: str
        Dataframe col that will serve as row for facet grid
    '''
    import matplotlib.pyplot as plt
    import seaborn as sns
    
    g = sns.FacetGrid(dataframe, col= fac_col,row= fac_row, sharex=sharex, sharey=sharey)
    return g.map(plt.scatter, x, y)

def plot_scatter(dataframe, x, y):
    '''
    Creates basic scatter plot

    input
    -----
    x: str
    y: str
    '''
    return dataframe.plot(x=x, y=y, kind='scatter')

def roll_diff_df(dataframe, window=[2,30,60,90], id_col='id_sess', diff_col = 'cadence'):
    '''
    Creates a new dataframe representing the rolling difference between rows for each participant
    
    input:
    ------
    dataframe: pd.DataFrame
    window: list
        Windows for rolling difference
    id_col: str
        Column within dataframe used to identify participants/sessions
    diff_col: str
        Column to do rolling difference on
    
    return:
    ------
    my_dic: dictionary of dataframes
        New columns labeled as `diff_col_win`. Use h.dic_to_df() to convert to df.
    '''
    
    temp_dic = {}
    for p in list(dataframe[id_col].unique()):
        temp_df = dataframe[dataframe[id_col] == p]
        for win in window:
            temp_df[f'diff_{diff_col[:3]}_{win}'] = temp_df[diff_col].diff(win)
        temp_dic[p] = temp_df

    return temp_dic

def session_extractor(dataframe, head_dic, tail_dic):
    '''
    Extract the sessions from each participant
    
    input
    -----
    dataframe
    head_dic: dic
        Dictionary in format of dic{id = [loc, mean, std]} where id represents participant/session combo,
        and loc represents the row index where the cutting will start
    tail_dic: dic
        Dictionary in format of dic{id = [loc, mean, std]} where id represents participant/session combo,
        and loc represents the row index where the cutting will end
        
    return
    ------
    new_df: dataframe
        Original dataframe but with each participant/session combo shortened according to given dictionaries.
    '''
    import pandas as pd
    # cut out subdataframes
    temp_dic = {}
    for key, value_h in head_dic.items():
        value_t = tail_dic[key]
        temp_df = dataframe[dataframe['id_sess'] == key]
        temp_df = temp_df.reset_index(drop = True)
        temp_df = temp_df.iloc[value_h[0]:value_t[0],:]
        temp_df = temp_df.reset_index(drop = True)
        temp_dic[key] = temp_df
    
    # recreate dataframe
    new_df = pd.DataFrame(columns = list(dataframe.columns))
    for key, value in temp_dic.items():
        new_df = pd.concat([new_df, value])
    new_df = new_df.reset_index(drop = True)
    
    return new_df

def z_score_calc(dataframe,col,overall = True, group = 'id'):
    '''
    Calculates the z score of each value in a series. 
    
    input:
    ------
    dataframe: pd.DataFrame
    col: str
        Column in dataframe to analyze
    overall: bool
        True: analyzes series without regard to group
        False: analyzes each group independently, then returns a df containing one ID and one z-score column.
    group: str
        Column where identifiers or participants are
    '''
    import pandas as pd
    if overall == True:
        my_series = dataframe[col]
        z_col = ((my_series) - my_series.mean()) / my_series.std()
        dataframe[f'{col}_overall_z_score'] = z_col
        return z_col
    else:
        z_df = pd.DataFrame(columns = [group,f'{col}_z_score'])
        my_groups = list(dataframe[group].unique())
        for g in my_groups:
            my_series = dataframe[dataframe[group] == g][col]
            z_score = ((my_series) - my_series.mean()) / my_series.std()
            temp_z_df = pd.DataFrame()
            temp_z_df[f'{col}_z_score'] = z_score
            temp_z_df[group] = g
            z_df = z_df.append(temp_z_df)
        return z_df