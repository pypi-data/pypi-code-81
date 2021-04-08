import numpy as np

def process_mfo(data, acronyms, out_colname):
    data_active = data.loc[:, acronyms]
    
    #find rows with no answers
    data_active = (data_active.isna() == False).astype(int)
    
    sum_rows = np.sum(data_active, axis=1)
    idx_no_answer = np.where(sum_rows == 0)[0]
    
    #0: no one; 1: only mother, 3: only father, 5: only other, 
    #4: mother and father; 6: mother and other; 8: father and other; 9: mother father and other
    out_active = data_active * np.array([1, 3, 5, 0])
    out_active = out_active.sum(axis=1) 
    
    #set rows with no answers to nan
    out_active.iloc[idx_no_answer] = np.nan
    
    #0: no one
    #1: another only
    #2: one parent only
    #3: one parent and another
    #4: both parents
    #5: both parents and another
    score_active = data_active * np.array([2, 2, 1, 0])
    score_active = score_active.sum(axis=1) 
    
    #set rows with no answers to nan
    score_active.iloc[idx_no_answer] = np.nan
    
#    data[out_colname] = out_active
    data[f'{out_colname}_score'] = score_active
    data.drop(acronyms, axis=1, inplace=True)
    return(data)

def process_mfo_caregiver(data, acronyms, out_colname):
    data_active = data.loc[:, acronyms]
    
    #find rows with no answers
    data_active = (data_active.isna() == False).astype(int)
    
    sum_rows = np.sum(data_active, axis=1)
    idx_no_answer = np.where(sum_rows == 0)[0]
    
    #0: no one; 1: only mother, 3: only father, 5: only other, 
    #4: mother and father; 6: mother and other; 8: father and other; 9: mother father and other
    out_active = data_active * np.array([1, 3, 5, 0])
    out_active = out_active.sum(axis=1) 
    
    #set rows with no answers to nan
    out_active.iloc[idx_no_answer] = np.nan
    
    #0: no one
    #1: another only
    #2: one parent only
    #3: one parent and another
    #4: both parents
    #5: both parents and another
    score_active = data_active * np.array([2, 2, 1, 0])
    score_active = score_active.sum(axis=1) 
    
    #set rows with no answers to nan
    score_active.iloc[idx_no_answer] = np.nan
    
#    data[out_colname] = out_active
    data[f'{out_colname}_score'] = score_active
    data.drop(acronyms, axis=1, inplace=True)
    return(data)