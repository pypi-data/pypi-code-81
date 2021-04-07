# Databricks notebook source
# To upload this file to the cloud, save this shortcut in your .bash_profile: /*
# update_dscoe_utils {
# databricks workspace export_dir /Shared/dscoe_utils /Users/petermyers/Desktop/dscoe_utils
# gsutil cp /Users/petermyers/Desktop/utils/utils.py gs://dscoe-utils
# }

import pandas as pd
def initialize_databases():
    spark.sql("create database back_room")
    spark.sql("create database front_room")

def view_back_room():
    spark.sql("use back_room")
    display(spark.sql("show tables"))
    
def view_front_room():
    spark.sql("use front_room")  
    display(spark.sql("show tables"))
    
def run_a_notebook(path="/Shared/utils/test", arguments={}):
  dbutils.notebook.run(path, timeout_seconds=86400, arguments=arguments)
    

# COMMAND ----------

