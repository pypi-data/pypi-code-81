#pylint: skip-file
import sys
import os

# This is the directory of the source code that the web app will run from
sys.path.append("/home/phaesler/src/datacube/wms")

# The location of the datcube config file.
os.environ["DATACUBE_CONFIG_PATH"] = "/home/phaesler/.datacube.conf.local"

# AWS Keys - do not commit!
os.environ["AWS_ACCESS_KEY_ID"] = "AKIAIRHPOTIL5V5J5Y5A"
os.environ["AWS_SECRET_ACCESS_KEY"] = "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"

from datacube_ows.ogc import app
application = app
