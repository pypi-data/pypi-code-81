import pandas as pd
import sqlite3

def ExportDB(df):
    con = sqlite3.connect("/Users/jiayiwang08/Desktop/sqlite/test.db")
    df.to_sql('new_table', con, if_exists='replace', index=False)



