# Databricks notebook source
# update_dscoe_utils() {
#   current_path=`pwd`
#   current_folder=${current_path##*/}
#   # pip install --upgrade setuptools
#   # pip install --upgrade twine
#   mkdir /Users/petermyers/Desktop/dscoe_utils/
#   py_commons_env
#   rm /Users/petermyers/Desktop/dscoe_utils/dscoe_utils.py
#   databricks workspace export_dir /Shared/dscoe_utils /Users/petermyers/Desktop/dscoe_utils/dscoe_utils
#   touch /Users/petermyers/Desktop/dscoe_utils/__init__.py
#   cd /Users/petermyers/Desktop/dscoe_utils/
#   git_push update
#   Rm -rf dist
#   Echo ""
#   Echo ""
#   Echo "Go to GitHub and make a new release: https://github.com/Peter-32/dscoe_utils/releases"
#   Echo "Just fill out the tag as something like v_02"
#   Echo "copy the tar.gz as a link and place it in the setup script"
#   Echo "update the setup.py to use the new version number"
#   Echo "Then run build_py"
#   Echo "Lastly run deploy_py"
#   Echo "username and password are: peterm3232"
#   Echo "fefiwo431rFWQEF432@ijsaf"
# }
def initialize_databases(spark):
    spark.sql("create database back_room")
    spark.sql("create database front_room")

def view_back_room(spark):
    spark.sql("use back_room")
    display(spark.sql("show tables"))
    
def view_front_room(spark):
    spark.sql("use front_room")  
    display(spark.sql("show tables"))
    
def run_a_notebook(dbutils, path="/Shared/utils/test", arguments={}):
  dbutils.notebook.run(path, timeout_seconds=86400, arguments=arguments)
    

# COMMAND ----------

