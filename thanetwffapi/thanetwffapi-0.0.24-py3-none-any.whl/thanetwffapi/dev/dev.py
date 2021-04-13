from thanetwffapi.query.SGQuery import SGQuery

# ============== Builder ==============
# How to use:
# using_db(path) - sets the path where files are stored

# === with-keyword: queries files based on these descriptions. all can use wildcard ('*') to select all
# with_name - tuples of name ('name1','name2')
# with_foundation - tuples of foundations
# with_timestamp - tuples of timestamps
# with_channels() - tuples, select channels
# with_mean() - Enter period that should be grouped and taken mean of. E.g. '30s', '1min', '3w', '1y' ..

# === Out Of Bounds
# remove_out_of_bounds() - depricated (this is default, don't need to be set)
# set_out_of_bounds(value) - set values that are out of bounds, with either a int value, or 'mean' of the channel

# === query files - query_files()
# query_files() - with (default) params skip_10_rows=True, skip_files=1
# skip_10_rows = True : in each file, select the tenth row, if False select all rows
# skip_files : number of files skipped when querying

# === corrections
# correct_channels_microstrain()
# correct_channels_realvalue()
# correct_channels_advalue()
# -- If non of these are chosen, AD value
# correct_timestamp()

# === Select
# to_df() - returns queried data as pandas DataFrame
# to_csv() - returns queried data as csv in folder
# ======================================
#local_path = '/media/sagmo/BD7B-08F8/UNI/7. Sem/Bac/Project_Related/Data/OneDrive_1'
local_path = '/media/sagmo/My Book/workspace/uni/bac/data/Thanet - foundation monitoring data'

test_file = 'A02-20170823-000000-001000.txt'
test_file_2 = 'A07-20170820-161000-162000.txt'

# t_start = '20170823-000000'
# t_end = '20170823-235900'


t_start = '20171017-000000'
t_end = '20171018-000000'



# import time
# tot_time = 0
# start = time.time()
#
# end = time.time()
# tot_time = tot_time + (end - start)
# print("Time: ", end - start)
# print('Time average: ', tot_time/1)


sg_df = SGQuery() \
    .using_db(local_path) \
    .with_foundation('A02') \
    .with_duration(t_start, t_end) \
    .with_channels(1, 3, 5, 7) \
    .with_mean('1min') \
    .query_files() \
    .correct_channels_microstrain() \
    .correct_timestamp() \
    .sort_timestamp() \
    .to_df()

print(sg_df)



