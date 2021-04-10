import pandas as pd 

def touches(df_boxscore):
    '''
    Touches estimate the number of times a player touched the ball in an attacking position on the floor. 
    The theory behind the formula is that once a player gets the ball, he can only do one of four things (aside from dribbling, of course):
        - pass 
        - shoot
        - draw a foul
        - commit a turnover
    Touches Formula=Field Goal Attempts + Turnovers + (Free Throw Attempts / (Team’s Free Throw Attempts/Opponents Personal Fouls)) + (Assists/0.17)
    '''

    # helper function
    def compute_touches(row):
        current_game_id = row['game_id']
        current_team = row['team_id']

        home_team_metric = df_groupby[(df_groupby['game_id'] == current_game_id) & (df_groupby['team_id'] == current_team)]
        away_team_metric = df_groupby[(df_groupby['game_id'] == current_game_id) & (df_groupby['team_id'] != current_team)]
        
        try:
            return row['fga'] + row['tov'] \
                + (row['fta'] / (home_team_metric['fga'].to_list()[0] / away_team_metric['pf'].to_list()[0]) + row['ast']/0.17)
        except:
            return 0.0

    # Touches Formula=Field Goal Attempts + Turnovers + (Free Throw Attempts / (Team’s Free Throw Attempts/Opponents Personal Fouls)) + (Assists/0.17)
    df_groupby = df_boxscore.groupby(['game_id', 'team_id']).sum().reset_index()
    df_boxscore['touches'] = df_boxscore.apply(lambda row: compute_touches(row), axis=1)

    return df_boxscore

def versatility_index(df_boxscore): 
    '''
    Versatility Index, which is invented by John Hollinger, is a metric that measures a player’s ability to produce in more than one statistic.
    The metric uses points, assists, and rebounds. The average player will score around a five on the index, while top players score above 10.
    '''
    df_boxscore['versatility_index'] = pow(df_boxscore['pts']* df_boxscore['trb']*df_boxscore['ast'],0.33)
    return df_boxscore

def non_scoring_possessions(df_boxscore):
    '''
    Non-scoring player possessions would be a player’S missed field goals, plus free throws that weren’t rebounded by his team, plus his turnovers.
    Method 1:
    non scoring Possessions= FGA-(FGA-FG)*OR%-FG-0.5*FT+0.4*FTA+TO
    
    OR%= TMOR/(TMFGA-TMFG)
    TMOR= Total team offensive rebounds, 
    TMFGA= Total field goals attempted by team, 
    TMFG= Total field goals made by team

    Method 2:
    total possession - scoring possession = non-scoring-possessions
    '''
    # # helper function
    # def compute_non_scoring_possessions(row):
    #     current_game_id = row['game_id']
    #     current_team = row['team_id']

    #     home_team_metric = df_groupby[(df_groupby['game_id'] == current_game_id) & (df_groupby['team_id'] == current_team)]
    #     away_team_metric = df_groupby[(df_groupby['game_id'] == current_game_id) & (df_groupby['team_id'] != current_team)]
        
    #     OR_percent = home_team_metric['orb'].to_list()[0]/(home_team_metric['fga'].to_list()[0] - home_team_metric['fg'].to_list()[0])

    #     try:
    #         return row['fga']- 1.07* (row['fga']- row['fg']) * OR_percent - row['fg'] - 0.5*row['ft']+0.4*row['fta']+row['tov']
    #     except:
    #         return 0.0
    
    # df_groupby = df_boxscore.groupby(['game_id', 'team_id']).sum().reset_index()
    df_boxscore['non_scoring_pos'] = df_boxscore['total_poss'] - df_boxscore['scoring_pos']
    return df_boxscore

def scoring_possessions(df_boxscore):
    '''
    Scoring player possessions would be the player’s field goals that weren’t assisted on, plus a certain percentage of his field goals that were assisted on,
    plus a certain percentage of his assists, plus his free throws made.

    Scoring Possessions Formula=(Field Goals Made) – 0.37*(Field Goals Made)*Q/R + 0.37*(Player Assists) + 0.5*(Free Throws Made)
    
    where;
        Q=5*(Player Minutes)*(Team Assist Total)/(Team Total Minutes)-(Player Assists)
        R=5*(Player Minutes)*(Team Field Goals Made)/(Team Minutes)-(Player Assists)
    '''

    def compute_scoring_pos(row):
        current_game_id = row['game_id']
        current_team = row['team_id']

        home_team_metric = df_groupby[(df_groupby['game_id'] == current_game_id) & (df_groupby['team_id'] == current_team)]
        away_team_metric = df_groupby[(df_groupby['game_id'] == current_game_id) & (df_groupby['team_id'] != current_team)]

        print(home_team_metric['mins_played'])
        print(away_team_metric['mins_played'])

        try:
            Q =(row['mins_played']*home_team_metric['ast'].to_list()[0]/home_team_metric['mins_played'].to_list()[0])-row['ast']
            R =(row['mins_played']*home_team_metric['fg'].to_list()[0]/home_team_metric['mins_played'].to_list()[0])-row['ast']

            return row['fg'] -  0.37*row['fg']*Q/R + 0.37*row['ast']+0.5*row['ft']
        except:
            return None
            
    df_boxscore['mins_played'] = df_boxscore['minutes'] + df_boxscore['seconds']/60
    df_groupby = df_boxscore.groupby(['game_id', 'team_id']).sum().reset_index()
    df_boxscore['scoring_pos'] = df_boxscore.apply(lambda row: compute_scoring_pos(row), axis=1) 

    return df_boxscore

def win_score(df_boxscore):
    '''
    Win Score is David Berri’s metric that indicates the relative value of a player’s points,rebounds, steals, turnovers, and field goal attempts.
    '''
    df_boxscore['win_score'] = df_boxscore['pts']+df_boxscore['trb']+df_boxscore['stl']+0.5*df_boxscore['ast']+ \
        0.5*df_boxscore['blk']-df_boxscore['fga']-df_boxscore['tov']-0.5*df_boxscore['fta']-0.5*df_boxscore['pf']

    return df_boxscore


def individual_floor_percentage(df_boxscore):
    '''
    Individual Floor Percentage is a metric that indicates the ratio of a player’s scoring possessions by his total possessions.
    When a player ends his team’s possession, it would be a possession charged to him. This gives the player’s total possessions.
    When a player scored or assisted on a score, a scoring possession would be charged to him.

    Individual Floor Percentage Formula=100*(Player’s Scoring Possessions)/(Player’s Total Possessions)
    '''
    df_boxscore['indiv_floor_percent'] = df_boxscore['scoring_pos']/df_boxscore['total_poss']*100

    return df_boxscore 

def defensive_versatility_idx(df_boxscore):
    '''
    Defensive Versatility Index is a novel metric by StrictBytheNumbers, which attempts to quantify the ability of a player
    to produce in more than more defensive statistic.
    '''
    df_boxscore['def_versatility_index'] = pow(df_boxscore['blk']* df_boxscore['stl']*df_boxscore['drb'],0.33) - 2*df_boxscore['pf']

    return df_boxscore

def player_impact_estimate(df_boxscore):
    '''
    Player Impact Estimate aka PIE is a metric to gauge a player’s all-around contribution to the game. 
    Almost all statistical categories in the box score are involved in the PIE formula.
    '''
    df_boxscore.reset_index(inplace=True)
    game_total = df_boxscore.groupby('game_id').sum().reset_index().drop(['starter'],axis=1)
    player_join_game = df_boxscore.merge(game_total, how='left',on='game_id',suffixes=['_p','_game'])
    
    
    df_boxscore['pie']= (player_join_game['pts_p'] + player_join_game['fg_p'] + player_join_game['ft_p'] - player_join_game['fga_p'] - player_join_game['fta_p'] \
       + player_join_game['drb_p']+ 0.5*player_join_game['orb_p'] + player_join_game['ast_p']+ player_join_game['stl_p']+ 0.5*player_join_game['blk_p'] - player_join_game['pf_p'] - player_join_game['tov_p']) \
       /(player_join_game['pts_game'] + player_join_game['fg_game'] + player_join_game['ft_game'] - player_join_game['fga_game'] - player_join_game['fta_game'] \
         + player_join_game['drb_game']+ 0.5*player_join_game['orb_game'] + player_join_game['ast_game']+ player_join_game['stl_game']+ 0.5*player_join_game['blk_game'] - player_join_game['pf_game'] - player_join_game['tov_game'])

    return df_boxscore

def bbref_scoring_possessions_and_offense_rating(df_boxscore):
    '''
    Scoring player possessions would be the player’s field goals that weren’t assisted on, plus a certain percentage of his field goals that were assisted on,
    plus a certain percentage of his assists, plus his free throws made.

    The Scoring Possessions formula is by far the most complex:
    ScPoss = (FG_Part + AST_Part + FT_Part) * (1 - (Team_ORB / Team_Scoring_Poss) * Team_ORB_Weight * Team_Play%) + ORB_Part

    FG_Part = FGM * (1 - 0.5 * ((PTS - FTM) / (2 * FGA)) * qAST)
    qAST = ((MP / (Team_MP / 5)) * (1.14 * ((Team_AST - AST) / Team_FGM))) + ((((Team_AST / Team_MP) * MP * 5 - AST) / ((Team_FGM / Team_MP) * MP * 5 - FGM)) * (1 - (MP / (Team_MP / 5))))
    AST_Part = 0.5 * (((Team_PTS - Team_FTM) - (PTS - FTM)) / (2 * (Team_FGA - FGA))) * AST
    FT_Part = (1-(1-(FTM/FTA))^2)*0.4*FTA
    Team_Scoring_Poss = Team_FGM + (1 - (1 - (Team_FTM / Team_FTA))^2) * Team_FTA * 0.4
    Team_ORB_Weight = ((1 - Team_ORB%) * Team_Play%) / ((1 - Team_ORB%) * Team_Play% + Team_ORB% * (1 - Team_Play%))
    Team_ORB% = Team_ORB / (Team_ORB + (Opponent_TRB - Opponent_ORB))
    Team_Play% = Team_Scoring_Poss / (Team_FGA + Team_FTA * 0.4 + Team_TOV)
    ORB_Part = ORB * Team_ORB_Weight * Team_Play%
    Missed FG and Missed FT Possessions are calculated as follows:

    FGxPoss = (FGA - FGM) * (1 - 1.07 * Team_ORB%)
    FTxPoss = ((1 - (FTM / FTA))^2) * 0.4 * FTA
    Total Possessions are then computed like so:

    TotPoss = ScPoss + FGxPoss + FTxPoss + TOV

    PProd = (PProd_FG_Part + PProd_AST_Part + FTM) * (1 - (Team_ORB / Team_Scoring_Poss) * Team_ORB_Weight * Team_Play%) + PProd_ORB_Part
    where:

    PProd_FG_Part = 2 * (FGM + 0.5 * 3PM) * (1 - 0.5 * ((PTS - FTM) / (2 * FGA)) * qAST)
    PProd_AST_Part = 2 * ((Team_FGM - FGM + 0.5 * (Team_3PM - 3PM)) / (Team_FGM - FGM)) * 0.5 * (((Team_PTS - Team_FTM) - (PTS - FTM)) / (2 * (Team_FGA - FGA))) * AST
    PProd_ORB_Part = ORB * Team_ORB_Weight * Team_Play% * (Team_PTS / (Team_FGM + (1 - (1 - (Team_FTM / Team_FTA))^2) * 0.4 * Team_FTA))

    ORtg = 100 * (PProd / TotPoss)
    '''
    def compute_bbref_scoring_possessions_and_offense_rating(row):
        current_game_id = row['game_id']
        current_team = row['team_id']
        
        home_team_metric = df_groupby[(df_groupby['game_id'] == current_game_id) & (df_groupby['team_id'] == current_team)]
        away_team_metric = df_groupby[(df_groupby['game_id'] == current_game_id) & (df_groupby['team_id'] != current_team)]
        
        #handle null and zero values
        if row['fg'] == 0:
            q_ast = 0
        else:
            q_ast = ((row['mins_played'] / (home_team_metric['mins_played'].to_list()[0]/5)) * (1.14 * ((home_team_metric['ast'].to_list()[0] - row['ast']) / home_team_metric['fg'].to_list()[0]))) \
                + ((((home_team_metric['ast'].to_list()[0]/home_team_metric['mins_played'].to_list()[0]) * row['mins_played'] * 5 - row['ast']) / ((home_team_metric['fg'].to_list()[0]/home_team_metric['mins_played'].to_list()[0]) * row['mins_played'] * 5 - row['fg'])) \
                  * (1 - (row['mins_played'] / (home_team_metric['mins_played'].to_list()[0] / 5))))
        if row['fga'] == 0:
            fg_part = 0
            pprod_fg_part = 0
        else:
            fg_part = row['fg'] + (1 - 0.5 * ((row['pts'] - row['ft']) / (2 * row['fga'])) * q_ast) # this could be zero
            pprod_fg_part = 2 * (row['fg'] + 0.5 * row['3p']) * (1 - 0.5 * ((row['pts'] - row['ft']) / (2 * row['fga'])) * q_ast)
             
        if row['fta'] == 0:
            ft_part = 0
            ftx_poss = 0
        else:
            ft_part = (1 - (1 - (row['ft']/row['fta']))**2) * 0.4 * row['fta'] # this could be zero
            ftx_poss = ((1 - (row['ft'] / row['fta']))**2) * 0.4 * row['fta']
        
        ast_part = 0.5 * (((home_team_metric['pts'].to_list()[0] - home_team_metric['ft'].to_list()[0]) - (row['pts'] - row['ft'])) / (2 * (home_team_metric['fga'].to_list()[0] - row['fga']))) * row['ast']
        team_scoring_poss = home_team_metric['fg'].to_list()[0] + (1 - (1 - (home_team_metric['ft'].to_list()[0] / home_team_metric['fta'].to_list()[0]))**2) * home_team_metric['fta'].to_list()[0] * 0.4
        team_orb_perc = home_team_metric['orb'].to_list()[0] / (home_team_metric['orb'].to_list()[0] + (away_team_metric['trb'].to_list()[0] - away_team_metric['orb'].to_list()[0]))
        team_play_per = team_scoring_poss / (home_team_metric['fga'].to_list()[0] + home_team_metric['fta'].to_list()[0] * 0.4 + home_team_metric['tov'].to_list()[0])
        team_orb_weight = ((1 - team_orb_perc) * team_play_per) / ((1 - team_orb_perc) * team_play_per + team_orb_perc * (1-team_play_per))
        orb_part = row['orb'] * team_orb_weight * team_play_per
        
        scoring_poss = (fg_part + ast_part + ft_part) * (1 - (home_team_metric['orb'].to_list()[0] / team_scoring_poss) * team_orb_weight * team_play_per) + orb_part
        
        fgx_poss = (row['fga'] - row['fg']) * (1 - 1.07 * team_orb_perc)
        
        total_poss = scoring_poss + fgx_poss + ftx_poss + row['tov']
        
        # offense rating step by step
        
        pprod_ast_part = 2 * ((home_team_metric['fg'].to_list()[0] - row['fg'] + 0.5 * (home_team_metric['3p'].to_list()[0] - row['3p'])) / (home_team_metric['fg'].to_list()[0] - row['fg'])) \
                * 0.5 * (((home_team_metric['pts'].to_list()[0] - home_team_metric['ft'].to_list()[0]) - (row['pts'] - row['ft'])) / (2 * (home_team_metric['fga'].to_list()[0] - row['fga']))) * row['ast']
        pprod_orb_part = row['orb'] * team_orb_weight * team_play_per * (home_team_metric['pts'].to_list()[0] / (home_team_metric['fg'].to_list()[0] + (1 - (1 \
            - (home_team_metric['ft'].to_list()[0] / home_team_metric['fta'].to_list()[0]))**2) * 0.4 * home_team_metric['fta'].to_list()[0]))
        
        # individual points porduced
        pprod = (pprod_fg_part + pprod_ast_part + row['ft']) * (1 - (home_team_metric['orb'].to_list()[0] / team_scoring_poss) * team_orb_weight * team_play_per) + pprod_orb_part
        
        try:
            ortg = 100 * (pprod / total_poss)
        except:
            ortg = 0
        
        return scoring_poss, total_poss, ortg

    df_boxscore['mins_played'] = df_boxscore['minutes'] + df_boxscore['seconds']/60
    df_groupby = df_boxscore.groupby(['game_id', 'team_id']).sum().reset_index()
    df_boxscore['scoring_pos'], df_boxscore['total_poss'], df_boxscore['off_rating'] = zip(*df_boxscore.apply(lambda row: compute_bbref_scoring_possessions_and_offense_rating(row), axis=1))

    return df_boxscore