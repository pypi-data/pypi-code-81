#%%
from datetime import datetime, timedelta, date
from typing import List, Union, Iterator

#%%
def daterange(start_date: datetime,
              end_date: datetime,
              interval: timedelta = timedelta(days=1)) -> Iterator[datetime]:

    for i in range(0, int((end_date - start_date).total_seconds()), int(interval.total_seconds())):
        yield start_date + timedelta(seconds=i)


def chunks(it, n):
    chunk = []
    for i in it:
        chunk.append(i)
        if len(chunk) >= n:
            yield chunk
            chunk = []

    if len(chunk) > 0:
        yield chunk

#%%
def timestamp_chunk(start_timestamp: datetime,
                    end_timestamp: datetime,
                    interval: timedelta = timedelta(hours=1)) -> Iterator[datetime]:

    for i in range(int(interval.total_seconds()), int((end_timestamp - start_timestamp).total_seconds()), int(interval.total_seconds())):
        yield start_timestamp + timedelta(seconds=i) - interval, start_timestamp + timedelta(seconds=i)

# %%
