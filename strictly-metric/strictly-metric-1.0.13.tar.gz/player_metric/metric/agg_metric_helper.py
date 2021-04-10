import pandas as pd
import numpy as np

def seasons_left(df_all):
    ''' 
    Seasons Left is the estimate of how many seasons the player has left to play
    '''
    df_grouped = df_all.groupby(['player_id','player_name','season','pos']).max("season").reset_index()
    df_grouped = df_grouped[['player_id','player_name','age','pos']]
    df_grouped = df_grouped.groupby("pos").mean().reset_index()

    def helper_age_func(row):
      current_age = row['age']
      current_pos = row['pos']
      age = df_grouped[df_grouped['pos'] == current_pos]['age'].values
      return age - 0.75*current_age

    df_all['seasons_left'] = df_all[['age','pos']].apply(lambda x: helper_age_func(x),axis=1)
    df_all = df_all.explode('seasons_left')
    return df_all

def approx_value(df_all):
    '''
    Approximate Value is the metric which is an estimate of a player’s value,making no fine distinctions,
    but, rather, distinguishing easily between very good seasons, average seasons, and poor seasons.
    '''
    df_all['fg_missed'] = df_all['fga_totals'] - df_all['fg_totals']
    df_all['ft_missed'] = df_all['fta_totals'] - df_all['ft_totals']
    credits = df_all['pts_totals']+df_all['ast_totals']+df_all['trb_totals']+df_all['stl_totals']+ \
    df_all['blk_totals']-df_all['fg_missed']-df_all['ft_missed']-df_all['tov_totals']
    df_all['approx_value'] = pow(credits,0.75)/21
    return df_all

def trade_value(df_all):
    '''
    Trade Value is the estimate using a player’s age and his approximate value to determine how much value a player has left in his career. 
    Invented by Bill James.
    
    Trade Value Formula=[(Approximate Value- 27-0.75*Age)2(27-0.75*Age +1)*Approximate Value]/190+(Approximate Value)*2/13
    '''
    df_all['trade_value'] = (pow(df_all['approx_value']-df_all['seasons_left'],2)*(df_all['seasons_left']+1)*df_all['approx_value'])/190+df_all['approx_value']*2/13
    return df_all

def usage_efficiency_tradeoff(df_all):
    '''
    Trade-off between usage and efficiency is the mathematical relationship between usage rate and efficiency.
    Trade-off between usage and efficiency explains the player’s gain of offensive rating (points per 100 possessions) for the drop of each percent of usage.
    '''
    def estimate_coef(x, y): 
        # number of observations/points 
        n = np.size(x) 
    
        # mean of x and y vector 
        m_x, m_y = np.mean(x), np.mean(y) 
    
        # calculating cross-deviation and deviation about x 
        SS_xy = np.sum(y*x) - n*m_y*m_x 
        SS_xx = np.sum(x*x) - n*m_x*m_x 
    
        # calculating regression coefficients 
        b_1 = SS_xy / SS_xx 
        b_0 = m_y - b_1*m_x 
    
        return(b_0, b_1)

    df_temp = df_all[['player_id', 'season', 'mp_advanced', 'pts_per100', 'usg__advanced']].groupby(['player_id', 'season']).apply(lambda x: x.loc[x.mp_advanced.idxmax()]).drop(['player_id', 'season'], axis=1).reset_index()
    list_unique_player = df_temp["player_id"].unique()
    for player in list_unique_player:
        current_player = df_temp[df_temp["player_id"] == player].sort_values(by=['season'])
        x = current_player["pts_per100"].to_numpy()
        y = current_player["usg__advanced"].to_numpy()
        df_temp.loc[df_temp.player_id == player, 'usage_per_eff'] = estimate_coef(x,y)[1]

    return df_all.merge(df_temp[['player_id', 'season', 'usage_per_eff']], on=['player_id', 'season'])

