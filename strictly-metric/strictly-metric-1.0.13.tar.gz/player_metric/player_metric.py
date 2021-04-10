from player_metric.metric import per_game_metric_helper, agg_metric_helper

class PlayerMetric:
    """
        PlayerMetric
    """
    def __init__(self, df_all=None, df_boxscore=None):
        self.df_all = df_all
        self.df_boxscore = df_boxscore
    
    def preprocess(self, df):
        """
            preprocess steps
        """
        if df == "boxscore":
            df = self.df_boxscore
            df['mp'] = df['mp'].fillna("0:0")
        elif df == "all":
            df = self.df_all
        else:
            raise Exception("You can only only provide all or boxscore in the preprocess function. Please try again with the approciate parameters!")

        # drop index or unnamed columns
        try:
            df.drop(list(df.filter(regex = '(unnamed)|(^index)')), axis = 1, inplace = True)
        except:
            print("no column unnamed!")
        
        df.columns = [col_name.lower() for col_name in df.columns]
        df = df.fillna(0)

        return df

    def calculate_per_game_metric(self):
        self.df_boxscore = self.preprocess("boxscore")
        self.df_boxscore = per_game_metric_helper.touches(self.df_boxscore)
        self.df_boxscore = per_game_metric_helper.versatility_index(self.df_boxscore)
        self.df_boxscore = per_game_metric_helper.defensive_versatility_idx(self.df_boxscore)
        self.df_boxscore = per_game_metric_helper.bbref_scoring_possessions_and_offense_rating(self.df_boxscore)
        self.df_boxscore = per_game_metric_helper.non_scoring_possessions(self.df_boxscore)
        self.df_boxscore = per_game_metric_helper.win_score(self.df_boxscore)
        self.df_boxscore = per_game_metric_helper.individual_floor_percentage(self.df_boxscore)
        self.df_boxscore = per_game_metric_helper.player_impact_estimate(self.df_boxscore)
        
        return self.df_boxscore

    def calculate_aggregate_metric(self):
        self.df_all = self.preprocess("all")
        self.df_all = agg_metric_helper.seasons_left(self.df_all)
        self.df_all = agg_metric_helper.approx_value(self.df_all)
        self.df_all = agg_metric_helper.trade_value(self.df_all)
        self.df_all = agg_metric_helper.usage_efficiency_tradeoff(self.df_all)

        return self.df_all
