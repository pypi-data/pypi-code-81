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

class ItemItemFilter(ABCRecommender):
    """Item-item collaborative filtering, or item-based, or item-to-item, is a form of collaborative filtering for recommender systems based on the similarity between items calculated using people's ratings of those items.
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

        # Inner join on common item_id column
        self.merged_df = pd.merge(item_df, user_df)
        pivot = self.merged_df.pivot_table(index = [self.item_name], columns = [self.user_id], values = self.item_rating).reset_index(drop = True).fillna(0)
        
        # Compute item - item similarity
        self.item_similarity = 1 - pairwise_distances(pivot.to_numpy(), metric = "cosine")
        np.fill_diagonal(self.item_similarity, 0)
        self.ratings_matrix_items = pd.DataFrame(self.item_similarity)
        
    def getsimilaritems(self, item_name, k = 10, as_dict = True):
        """
        Returns k best matches to item_name based on cosine similarity of item_categories.

        Args:
            item_name (str): [description]
            k (int, optional): [description]. Defaults to 10.
            as_dict (bool, optional): [description]. Defaults to True.

        Returns:
            item_id, item_name pairs which have closest matches to input item_name
            type : dict if as_dict = True else list of tuples
        """
        # Check if item_name is present in item_df
        assert item_name in set(self.item_df[self.item_name])
        
        item_idx = self.item_df[self.item_df[self.item_name] == item_name].index.tolist()[0]
        self.item_df['similarity'] = self.ratings_matrix_items.iloc[item_idx]
        self.item_df.sort_values(by = ["similarity"], ascending = False, inplace = True)

        copied_df = self.item_df[0:k+1]
        item_dict = dict(zip(copied_df[self.item_name], copied_df[self.item_id]))
        
        if not as_dict:
            return list(item_dict.items())
        return item_dict
    

    def getuserrecommendations(self, user_id, k = 10, as_dict = True):
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
        user_item = self.merged_df[(self.merged_df[self.user_id] == user_id)]
        user_item = user_item.loc[user_item[self.item_rating].idxmax()][self.item_name]
        
        # get similar items to every item in user history
        self.getsimilaritems(user_item, max(1, int(0.2* k)))
        
        sorted_user_items = self.item_df[self.item_df['similarity'] >= 0.45][self.item_id]
        
        recommended_item = []
        df_recommended_item = pd.DataFrame()
        
        user2Item = self.user_df[self.user_df[self.user_id]== user_id][self.item_id]
        
        for item_id in sorted_user_items:
            if item_id not in user2Item:
                
                df_new = self.user_df[(self.user_df[self.item_id] == item_id)]
                df_recommended_item = pd.concat([df_recommended_item, df_new])
                
        best_k = df_recommended_item.sort_values([self.item_rating], ascending = False)[1:5*k + 1]
        
        list_item_ids = best_k[self.item_id] 
        item_titles = {}
        for item_id in list_item_ids:
            item_titles.update(self.item_df[self.item_df[self.item_id] == item_id][self.item_name].to_dict())
            if len(item_titles) == k:
                break
            
        if not as_dict:
            return list(item_titles.items())
    
        return item_titles