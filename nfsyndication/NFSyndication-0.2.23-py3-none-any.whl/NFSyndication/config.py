#!/usr/bin/python 
import sys
import logging
import colorful as cf
from jinja2 import Template, Environment, FileSystemLoader
from jinja2.exceptions import *
from feedparser import parse as parseURL
import json
import os
import shutil

cfail = cf.bold_red

def init():
  logging.info("Fetching...")
  try:
    from . import nfs_main
  except Exception as e:
    exception = cfail(
                  "Error while parsing: {exceptname}: {errmessage}".format(exceptname=str(e.__class__.__name__), errmessage=e)
                   )
    print(exception)
    sys.exit(1)
  except KeyboardInterrupt:
    print('Session terminated. Operation aborted by the user.')
    
class GetFeedDataPerConfiguration(object):
    def __init__(self, eachUrl, tempPath, emdF, fPath, outputPath, templFileLocation, outPath, pageTitle, outJSON=False, jsonFile=None):
        """ Request and parse all of the feeds, saving them in self.feeds"""
        self.outJSON = outJSON
        self.feeds = []
        self.outputP = os.path.join(emdF,os.path.sep).replace(os.path.sep, '{}/'.format(emdF))
        #self.dir_path = os.path.dirname(os.path.realpath(__file__))
        self.env = Environment(loader=FileSystemLoader(tempPath))
        self.fetch_feeds(eachUrl)
        self.empty_public(emdF)
        self.copy_static(fPath, outputPath)
        self.render_page(templFileLocation, outPath, pageTitle)
        if bool(outJSON) == True and type(jsonFile)==str:
         """ Ensure that the file would be written in JSON format"""
         self.outputJson(jsonFile, self.feeds)
         print('Renering JSON')
        elif bool(outJSON) == True and not jsonFile:
         print(cfail("Missing or undefined argument: jsonFile"))
         sys.exit(1)
        elif bool(outJSON) == True and not type(jsonFile)==str:
         print(
            cfail('Error: must be string type, not {}'.format(type(jsonFile)))
            )
         sys.exit(1)
        
    def fetch_feeds(self, URLs):
        """ Request and parse all of the feeds, saving them in self.feeds """
        from .extras import fetch_content
        for url in URLs:
          try:
            print(f"Fetching {url}")
            self.feedURL = parseURL(url)
            self.feeds.append(self.feedURL)
            fetch_content(url)
          except Exception as er:
            print('Error while looking for URL feed: {}'.format(er) )
            
    def empty_public(self, sf):
        """ Ensure the public directory is empty before generating. """
        try:
          shutil.rmtree(sf)          
          os.mkdir(sf)
        except:
            print(cfail(f"Error cleaning up old files."))

    def copy_static(self, fPath, outputPath):
        """ Copy static assets to the public directory """
        try:
            shutil.copytree('{}'.format(fPath), '{}'.format(os.path.join(self.outputP,outputPath)))
        except:
            print(cfail(f"Error copying static files."))

    def render_page(self, templFileLocation, outputPath, pageTitle):
       print("Rendering page to static file.")
       try:
          template = self.env.get_template(templFileLocation)
       except (TemplateSyntaxError, TemplateNotFound, UndefinedError, TemplateAssertionError) as error:
          print(cfail("Error while reading template: {}".format(str(error))))
          sys.exit(1)
       with open('{}'.format(os.path.join(self.outputP,outputPath)), 'w+', encoding='utf8') as file:
           try:
            html = template.render(
                title = '{}'.format(pageTitle),
                feeds = self.feeds
            )
            file.write(html)
           except UnboundLocalError:
             print(cfail('Error while writing output file: {}'.format(outputPath)))
             sys.exit(1)
            
    def outputJson(self, trh, jsonInput):
         try:
           with open(os.path.join(self.outputP,'{}.json'.format(trh)), 'w', encoding='utf8') as jsonF:
             self.jsonFile = jsonF
             json.dump(jsonInput, jsonF, ensure_ascii=False, indent=4)
         except TypeError:
             print('Error: {} at {hrefURL}'.format(self.feedURL.bozo_exception,hrefURL=self.feedURL.href)) 
             del self.feedURL             
           