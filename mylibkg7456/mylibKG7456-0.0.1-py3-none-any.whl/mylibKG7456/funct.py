import pandas as pd

from pandas import json_normalize
from SPARQLWrapper import SPARQLWrapper, JSON

import matplotlib.pyplot as plt
import plotly.express as px
import plotly.figure_factory as ff

from imageio import imread
import re
import time

class vizKG:
  """
  Instantiate vizKG object.
  
  """

  def __init__(self, sparql_query, sparql_service_url, mode='table'):
      """
      Constructs all the necessary attributes for the vizKG object

      :param (string) sparql_query: The SPARQL query to retrieve.
      :param (string) sparql_service_url: The SPARQL endpoint URL.
      :param (string) mode: Type of visualization
                            Default = 'table'
                            Option = {"table", "imageGrid", "Timeline"}.
      :param (pandas.Dataframe | list[list]) dataframe: The table query
      """

      self.sparql_query = sparql_query
      self.sparql_service_url = sparql_service_url
      self.mode = mode
      self.dataframe = self.query_result()
      

  def query_result(self, is_value='True'):
      """
      Query the endpoint with the given query string and return the results as a pandas Dataframe.

      :param (bool) is_value: The boolean to filter (dot)value column.

      Returns
      -------
      (pandas.Dataframe) table: The result of processing table      
      """

      sparql = SPARQLWrapper(self.sparql_service_url, agent="Sparql Wrapper on Jupyter example")  
      
      sparql.setQuery(self.sparql_query)
      sparql.setReturnFormat(JSON)

      # ask for the result
      result = sparql.query().convert()
      table  = json_normalize(result["results"]["bindings"])

      #extract value
      if is_value:
        df = table.filter(regex='.value')
        table = df.rename(columns = lambda col: col.replace(".value", ""))
      
      #rename column
      table = self.rename_column(table)

      return table


  def rename_column(self, dataframe):
      """
      Rename column of dataframe based on regex validity check

      :param (pandas.Dataframe) dataframe: The table of query result.

      Returns
      -------
      (pandas.Dataframe) table: The result of renaming table column             
      """

      #Regex pattern
      pattern_url = r"^(?:http(s)?:\/\/)?[\w.-]+(?:\.[\w\.-]+)+[\w\-\._~:/?#[\]@!\$&'\(\)\*\+,;=.]+$" #regex url
      pattern_img = r"^http(s)?://(?:[a-z0-9\-]+\.)+[a-z]{2,6}(?:/[^/#?]+)+\.(?:jpg|gif|png)$"        #regex img
      pattern_coordinate = r"^Point"
      pattern_label = r"Label$"

      for i in range (len(dataframe.columns)):
        check = dataframe[dataframe.columns[i]].iloc[0]
        if re.match(pattern_url, check):
          if 'uri' in dataframe.columns:
            if 'uri2' in dataframe.columns:
              dataframe = dataframe.rename(columns={dataframe.columns[i]: "uri_"+str(dataframe.columns[i])}, errors="raise")
            else:          
              dataframe = dataframe.rename(columns={dataframe.columns[i]: "uri2"}, errors="raise")
          else:
            dataframe = dataframe.rename(columns={dataframe.columns[i]: "uri"}, errors="raise")
        elif re.match(pattern_img, check): 
          dataframe =  dataframe.rename(columns={dataframe.columns[i]: "pic"}, errors="raise")
        elif re.match(pattern_coordinate, check):
          dataframe =  dataframe.rename(columns={dataframe.columns[i]: "coordinate"}, errors="raise")
        elif i == len(dataframe.columns)-1 and (re.match(pattern_label, check)):
          dataframe = dataframe.rename(columns={dataframe.columns[i]: dataframe.columns[i]}, errors="raise")

      #change data types in each column
      dataframe = self.change_dtypes(dataframe)  
      
      return dataframe


  def change_dtypes(self, dataframe):
      """
      Change data type column of dataframe

      :param dataframe (pandas.Dataframe): The result of renaming table column .

      Returns
      -------
      (pandas.Dataframe) table: The result of changing data type table column             
      """

      for column in dataframe:
        try:
          dataframe[column] = dataframe[column].astype('datetime64')
        except ValueError:
          pass
      for column in dataframe:
        try:
          dataframe[column] = dataframe[column].astype('float64')
        except (ValueError, TypeError):
          pass
      return dataframe

  def check_property(self, dataframe):
      """
      Find candidate for visualization

      :param dataframe (pandas.Dataframe): The result of changing data type table column.

      Returns
      -------
      (list) candidate_visualization: List of candidate visualization
      """

      candidate_visualization = []
      #reserved name column
      reserved_name = ['uri', 'pic', 'coordinate']

      dateColumn = [name for name in self.dataframe.columns if self.dataframe[name].dtypes == 'datetime64[ns]']
      integerColumn = [name for name in self.dataframe.columns if self.dataframe[name].dtypes == 'float64']
      objectColumn = [name for name in self.dataframe.columns if not name.startswith(tuple(reserved_name))]

      num_dateColumn = len(dateColumn)
      num_integerColumn = len(integerColumn)
      num_objectColumn = len(objectColumn)

      if 'pic' in self.dataframe.columns:
        candidate_visualization.append('imageGrid')
      elif 'coordinate' in self.dataframe.columns:
        candidate_visualization.append('map')
      elif num_dateColumn == 2:
        candidate_visualization.append('timeline')
      else:
        candidate_visualization.append('table')

      return candidate_visualization

  def plot(self):
      """
      Plot visualization with suitable corresponding mode
      """

      candidate_visualization = self.check_property(self.dataframe)

      if self.mode in candidate_visualization:
        if self.mode == 'imageGrid':
          self.imageGrid(self.dataframe)
        elif self.mode == 'timeline':
          self.timeline(self.dataframe)
        else:
          self.simpleTable(self.dataframe)  
      else:
        self.simpleTable(self.dataframe)

  @staticmethod
  def simpleTable(dataframe):
    """
    Generate simple table visualization

    :param dataframe (pandas.Dataframe): data for visualization
    """
    fig = ff.create_table(dataframe)
    fig.show()

  @staticmethod
  def imageGrid(dataframe):
    """
    Generate image grid visualization

    :param dataframe (pandas.Dataframe): data for visualization
    """
    pic = [i for i in dataframe.pic]

    #get label column
    labels = [name for name in dataframe.columns if name != 'uri' and name != 'pic']
    itemLabel = []
    if labels:
      itemLabel = [i for i in dataframe[labels[0]]]
    else:
      itemLabel = [i for i in dataframe.uri]

    plt.figure(figsize=(20,20))
    columns = 4
    for i, url in enumerate(pic):
        plt.subplot(len(pic) / columns + 1, columns, i + 1)
        try:
          image = imread(url)
          plt.title(itemLabel[i])
          plt.imshow(image) #, plt.xticks([]), plt.yticks([])
          plt.axis('off')
        except:
          time.sleep(5)
          image = imread(url)
          plt.title(itemLabel[i])
          plt.imshow(image) #, plt.xticks([]), plt.yticks([])
          plt.axis('off')
  
  @staticmethod
  def timeline(dataframe):
    """
    Generate timeline visualization

    :param dataframe (pandas.Dataframe): data for visualization
    """
    #get label column
    labels = [name for name in dataframe.columns if name != 'uri' and name != 'pic' and dataframe[name].dtypes != 'datetime64[ns]']
    if not labels:
      labels = [name for name in dataframe.columns if name == 'uri']
      
    #get date column
    dateLabels = [name for name in dataframe.columns if dataframe[name].dtypes == 'datetime64[ns]']

    fig = px.timeline(dataframe, x_start=dateLabels[-1], x_end=dateLabels[0], 
                      y=labels[0], color=labels[0])
    fig.update_yaxes(autorange="reversed")
    fig.show()