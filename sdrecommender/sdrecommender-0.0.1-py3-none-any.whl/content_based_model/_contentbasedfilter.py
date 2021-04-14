# Author : Pranav, Nishanth, Keshav, Rayees

# Imports
from math import sqrt
import pandas as pd
import numpy as np

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

from .._abcrecommender import ABCRecommender

class ContentBasedFilter(ABCRecommender):
    """ContentBasedFiltering : This method of recommending objects to a certain user depends solely on the contents of the item itself. This 'content' could be any parameter that describes 2 similar items to be similar. Using this parameter we can calculate the similarity between any 2 items purely based on their contents.
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
        
        # Vectorizer for item_categories
        tfidf_item_categories = TfidfVectorizer(token_pattern = '[a-zA-Z0-9\-]+')
        tfidf_item_categories_matrix = tfidf_item_categories.fit_transform(self.item_df[self.item_categories])
        
        # Compute Cosine Similarities between items using item categories
        self._cosine_sim_items = linear_kernel(tfidf_item_categories_matrix, tfidf_item_categories_matrix)
        
        # Check if item_id is common column in both dataframes: user_df and item_df
        assert ((self.item_id in self.user_df.columns) and (self.item_id in self.item_df.columns)), "No common name Found"
        
        # Check if item_rating is numeric
        assert np.issubdtype(self.user_df[self.item_rating].dtype, np.number), "Item Ratings must be numeric"
    
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
        assert item_name in set(self.item_df[self.item_name]), "Item Name missing in column"
        
        idx_item = self.item_df.loc[self.item_df[self.item_name].isin([item_name])].index
        
        sim_scores_items = list(enumerate(self._cosine_sim_items[idx_item][0]))
        sim_scores_items = sorted(sim_scores_items, key=lambda x: x[1], reverse=True)
        sim_scores_items = sim_scores_items[1:k + 1]
        
        item_indices = [i[0] for i in sim_scores_items]
        
        similar_items = self.item_df[self.item_name].iloc[item_indices].to_dict()
        
        if not as_dict:
            return list(similar_items.items())
        
        return similar_items

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
        
        # check if user_id is present in user_df
        assert user_id in set(self.user_df[self.user_id]), "User ID missing in user_df"
        
        recommended_item_list = []
        item_list = []
        df_filtered = self.user_df[self.user_df[self.user_id] == user_id]
        
        for key, row in df_filtered.iterrows():
            item_list.append((self.item_df[self.item_name][row[self.item_id] == self.item_df[self.item_id]]).values[0])
        
        item_list = set(item_list)
            
        for item in item_list:
            for key, item_recommended in self.getsimilaritems(item, k = max(2, 0.1 * k)).items():
                recommended_item_list.append((key, item_recommended))

       # removing already watched movie from recommended list
        recommended_item_list = [(key, value) for key, value in recommended_item_list if value not in item_list]
        recommended_item_list = list(set(recommended_item_list))
        
        recommended_item_dict = {key:value for key, value in recommended_item_list[:k]}
        
        if not as_dict:
            return list(recommended_item_dict.items())

        return recommended_item_dict