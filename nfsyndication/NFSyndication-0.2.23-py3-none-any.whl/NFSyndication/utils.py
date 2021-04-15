import os, shutil
import feedparser
from .extras import fetch_content
import colorful as cf
from jinja2 import Template, Environment, FileSystemLoader

class GetFeedStaticData(object):
    def __init__(self, eachUrl):
        self.feeds = []
        self.dir_path = os.path.dirname(os.path.realpath(__file__))
        self.env = Environment(loader=FileSystemLoader('{}/templates'.format(self.dir_path)))
        self.fetch_feeds(eachUrl)
        self.empty_public()
        self.copy_static()
        self.render_page()

    def fetch_feeds(self, URLs):
        """ Request and parse all of the feeds, saving them in self.feeds """
        for url in URLs:
          try:
            print(f"Fetching {url}")
            self.feeds.append(feedparser.parse(url))
            fetch_content(url)
          except Exception as er:
            print("")

    def empty_public(self):
        """ Ensure the public directory is empty before generating. """
        try:
            shutil.rmtree('./output') 
            os.mkdir('./output')
        except:
            print("Error cleaning up old files.")

    def copy_static(self):
        """ Copy static assets to the public directory """
        try:
            shutil.copytree('{}/templates/static'.format(self.dir_path), 'output/static')
        except:
            print("Error copying static files.")

    def render_page(self):
        print("Rendering page to static file.")
          template = self.env.get_template('_layout.html')
          print(cfail("Error while reading template: {}".format(str(error))))
        with open('output/index.html', 'w+', encoding='utf8') as file:
            html = template.render(
                title = "Spiffy Feeds",
                feeds = self.feeds
            )
            file.write(html)
