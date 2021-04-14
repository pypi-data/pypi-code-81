# Author : Pranav, Nishanth, Keshav, Rayees

# Imports
from math import sqrt
import pandas as pd
import numpy as np

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from sklearn.metrics import pairwise_distances

from scipy.spatial.distance import cosine, correlation

from .._abcrecommender import ABCRecommender

class UserItemFilter(ABCRecommender):
    """The underlying assumption of the collaborative filtering approach is that if a person A has the same opinion as a person B on an issue, A is more likely to have B's opinion on a different issue than that of a randomly chosen person.
    """

    def __init__(self, user_df, item_df, user_id, item_id, item_rating, item_categories, item_name):
        """
        This class expects a user_df with user_ids and their given numeric ratings to items with item_ids.
        Also expects an item_df with item_ids and their given title and categories it falls under.

        Args:
            user_df (pd.DataFrame): User DataFrame with User_id, item_id, rating pairs
            item_df (pd.DataFrame): Item DataFrame with item_id, item_name, item_categories fields
            user_id (str): column name of corresponding to user_id
            item_id (str): column name of corresponding to item_id
            item_rating (str): column name of corresponding to rating
            item_categories (str): column name of corresponding to item_categories
            item_name (str): column name of corresponding to item_name
        """

        self.user_df = user_df
        self.item_df = item_df
        self.user_id = user_id
        self.item_id = item_id
        self.item_rating = item_rating
        self.item_categories = item_categories
        self.item_name = item_name

        self.merged_df = pd.merge(item_df,user_df)
        
        pivot = self.merged_df.pivot_table(index = [item_name], columns = [self.user_id], values = self.item_rating).reset_index(drop = True).fillna(0)
        
        item_similarity = 1 - pairwise_distances(pivot.to_numpy(), metric = "cosine")
        
        np.fill_diagonal(item_similarity, 0)
    
        self.ratings_matrix_users = pd.DataFrame(item_similarity)
        
        
    def getsimilaritems(self ,item_name = "", k=10, as_dict = True):
        raise NotImplementedError("UserItemFilter does not support item similarity computation.")



    def getuserrecommendations(self, user_id, k=10, as_dict = True):
        """
        Returns k best match items based on user history.

        Args:
            user_id (str): [description]
            k (int, optional): [description]. Defaults to 10.
            as_dict (bool, optional): [description]. Defaults to True.
            
        Returns:
            item_id, item_name pairs which have closest matches user item history
            type : dict if as_dict = True else list of tuples
        """
        
        user2Items = self.user_df[self.user_df[self.user_id]== user_id][self.item_id]
        
        similar_user_series = self.ratings_matrix_users.idxmax(axis=1)
        
        df_similar_user= similar_user_series.to_frame()
        df_similar_user.columns=['similarUser']
        sim_user = df_similar_user.iloc[0, 0]
        
        df_recommended = pd.DataFrame()
        item_ids = self.user_df[self.user_df[self.user_id]== sim_user][self.item_id]
        
        for item_id in item_ids:
            
            if item_id not in user2Items:
                
                df_new = self.merged_df[(self.merged_df[self.user_id] == sim_user) & (self.merged_df[self.item_id] == item_id)]
                
                df_recommended = pd.concat([df_recommended, df_new])
                
        best_k = df_recommended.sort_values([self.item_rating], ascending = False)[1:k+1] 
       
        list_item_ids = best_k[self.item_id] 
        
        item_titles = []
        
        for item_id in list_item_ids:
            item_titles.append(self.item_df[self.item_df[self.item_id]== item_id][self.item_name])
            
        item_dict = {}
        for item in item_titles:
            item_dict.update(item.to_dict())
        
        if not as_dict:
            return list(item_dict.items())
        
        return item_dict