import json

class ConfigDefault:

    @staticmethod
    def get_default():
        return '''{
  "default": {
    "mysql": {
      "host": "127.0.0.1",
      "port": 3306,
      "user": "root",
      "pass": "root"
    },
    "mongodb": {
      "host": "127.0.0.1:27017",
      "port": 27017,
      "user": "",
      "pass": ""
    },
    "redis": {
      "host": "127.0.0.1",
      "port": 6379,
      "db": 5
    },
    "slack": {
      "slack_token": "",
      "default_channel": "#reports"
    },
    "database": "storage",
    "meta_db": "meta",
    "logger_name": "",
    "use_sqlite": false,
    "use_mongo_db": true,
    "images_path": "G:/data/download_images",
    "html_path": "G:/data/html",
    "database_path": "G:/data/database",
    "user_path": "C:/Users/Will"
  },
  "dev": {
    "env": "dev",
    "google_sheet_credentials": "C:/Users/Will/Desktop/code/ai_/dist/config/credentials/credentials_will.json",
    "google_sheet_tokens": "C:/Users/Will/Desktop/code/ai_/dist/config/credentials/token_will.pickle",
    "mysql": {
      "host": "127.0.0.1",
      "port": 3306,
      "user": "root",
      "pass": "root"
    },
    "mongodb": {
      "host": "127.0.0.1:27017",
      "port": 27017,
      "user": "",
      "pass": ""
    },
    "redis": {
      "host": "127.0.0.1",
      "port": 6378,
      "db": 5
    },
    "other_db": {
      "mysql": {
        "host": "192.168.0.2",
        "port": 3306,
        "user": "root1",
        "pass": "root"
      },
      "mongodb": {
        "host": "192.168.0.2:27017",
        "port": 27017,
        "user": "",
        "pass": ""
      },
     "redis": {
        "host": "192.168.0.2",
        "port": 6379,
        "db": 5
      },
      "app_path": "/home/will/tmp/ai_",
      "images_path": "Z:/download_images",
      "html_path": "Z:/html"
    }
  },
  "stag": {
    "env": "stag",
    "images_path": "/home/will/code/ai_/dist/download_images",
    "html_path": "/home/will/code/ai_/dist/html",
    "database_path": "/home/will/code/ai_/dist/database",
    "user_path": "/home/will/code/",
      "mysql": {
      "host": "192.168.0.1",
      "port": 3306,
      "user": "root",
      "pass": "root"
    },
    "mongodb": {
      "host": "192.168.0.2:27017",
      "port": 27017,
      "user": "",
      "pass": ""
    },
    "redis": {
      "host": "192.168.0.149",
      "port": 6378,
      "db": 5
    },
    "other_db": {
      "mysql": {
        "host": "192.168.0.2",
        "port": 3306,
        "user": "root",
        "pass": "root"
      },
      "mongodb": {
        "host": "192.168.0.2:27017",
        "port": 27017,
        "user": "",
        "pass": ""
      },
      "redis": {
        "host": "192.168.0.2",
        "port": 6378,
        "db": 5
      }
    }
  },
  "prod": {
    "env": "prod",
    "images_path": "/mnt/sdb/data/data/download_images",
    "html_path": "/mnt/sdb/data/data/_html",
    "database_path": "/mnt/sdb/data/database",
    "user_path": "/home/will/code/",
    "other_db": {
      "mysql": {
        "host": "192.168.0.1",
        "port": 3306,
        "user": "root",
        "pass": "root"
      },
      "mongodb": {
        "host": "192.168.0.1:27017",
        "port": 27017,
        "user": "",
        "pass": ""
      },
      "redis": {
        "host": "192.168.0.1",
        "port": 6378,
        "db": 5
      }
    }
  },
  "mac": {
    "env": "mac",
    "html_path": "/Users/will/Desktop/code/ai_/dist/_html",
    "google_sheet_credentials": "/Users/will/Desktop/code/ai_/dist/config/credentials/credentials_will.json",
    "google_sheet_tokens": "/Users/will/Desktop/code/ai_/dist/config/credentials/token_will.pickle"
  }
}'''

    @staticmethod
    def generate_config(file):
        data = ConfigDefault.get_default()
        text_file = open(file, 'w')
        n = text_file.write(data)
        text_file.close()
        print(f'INFO: Generated file: {file}')

    @staticmethod
    def get_app_config():
        data = ConfigDefault.get_default()
        c = json.loads(data)

        return c

if __name__ == '__main__':
    print(ConfigDefault.get_app_config())