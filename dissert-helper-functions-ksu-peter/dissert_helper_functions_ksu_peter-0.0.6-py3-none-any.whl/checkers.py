def elapsed_time(dataframe, part, sess, timer='date'):
    '''
    Calculates the time that elapsed during each participant's session.

    input
    -----
    part: list
        List of participants to filter by
    sesh: list
        List of sessions that all participants went through
    timer: str
        Column that contains the time variable.
    '''
    delta_time = {}
    for p in part:
        for s in sess:
            my_df = dataframe[(dataframe['id']==p) & (dataframe['session']==s)]

            delta = my_df[timer].max() - my_df[timer].min()
            delta_time[f'{p}_{s}'] = delta        
    return delta_time


def mylist(myseries):
    '''
    Checks whether a series of integers is sequential. Returns EMPTY if list is empty.

    input
    -----
    mylist : series, int
    '''
    if myseries.empty == False:
        it = (x for x in myseries)
        first = next(it)
        return all(a == b for a, b in enumerate(it, first + 1))
    else:
        return '**LIST IS EMPTY**'


def sanity(new_df, num_part, num_sess):
    '''
    Checks that dataframe contains num_part participants, and that each participant has num_sess sessions, sends print statement. There is no output.
    
    Requires id and session columns

    input
    -----
    new_df: dataframe
        Dataframe to check
    num_part: int
        Number of participants
    num_sess: int
        Number of sessions per participant
        
    Source: https://stackoverflow.com/questions/28885455/python-check-whether-list-is-sequential-or-not/28885643#28885643
    '''
    part = list(new_df['id'].unique())
    sesh = list(new_df['session'].unique())
    part_size = len(new_df['id'].unique())
    if num_part == part_size:
        print(f'There are still {num_part} participants')
    else:
        print(f'Missing {num_part-part_size} participants')

    print(f'''-------------------
Checking whether {num_sess} sessions still exist
-------------------''')
    for p in part:
        ses_size = len(new_df[new_df['id']== p].loc[:,'session'].unique())
        if num_sess == ses_size:
            print(f'{p}: {True}')
        else:
            print(f'{p}: Missing {num_sess-ses_size} sessions')
