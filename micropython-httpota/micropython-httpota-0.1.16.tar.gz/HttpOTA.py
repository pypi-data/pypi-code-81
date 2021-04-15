import os
import time
import urequests as requests
import ujson as json
import utarfile

"""
"ota": {
    "base_url": "https://somewhere.com/",
    "check_frequency": 30
}
"""

class StubLogger:
    def debug(self, message):
        pass

    def info(self, message):
        pass

    def warning(self, message):
        pass

    def error(self, message):
        pass

    def critical(self, message):
        pass



class HttpOTA:
    def __init__(self, device_name, ota_config, **kwargs):
        if 'logger' in kwargs:
            self.logger = kwargs['logger']
        else:
            self.logger = StubLogger()

        if len(device_name) == 0:
            self.logger.error("Device name not configured")
            raise Exception("Device name not configured")

        self.device_name = device_name

        if not 'base_url' in ota_config:
            self.logger.error("OTA Base URL not configured")
            raise Exception("OTA Base URL not configured")
        else:
            self.base_url = ota_config['base_url']

        if not 'check_frequency' in ota_config:
            self.logger.info("OTA check frequency not configured, assuming 300s")
            self.check_frequency = 300
        else:
            self.check_frequency = ota_config['check_frequency']

    def format_time(self, some_time_thing):
        if type(some_time_thing) == int:
            some_time_thing = time.gmtime(some_time_thing)

        # 2021-04-15T03:06:25Z
        return "%04u-%02u-%02uT%02u:%02u:%02uZ" % some_time_thing[0:6]


    def update(self, **kwargs):
        self.load_local_manifest()
        self.logger.debug("local manifest: %s" % json.dumps(self.manifest))

        if 'force' in kwargs:
            force = kwargs['force'] == True
        else:
            force = False

        if 'automatic_reset' in kwargs:
            automatic_reset = False
        else:
            automatic_reset = True


        now = time.mktime(time.gmtime())
        since_last_check = now - self.manifest['last_update_check']
        next_scheduled_update = self.manifest['last_update_check'] + self.check_frequency

        status = {
            "updated": False,
            "need_reset": False,
            "success": False
        }

        if force:
            self.logger.warning("Forced update check")
            status = self.check_and_update()
        elif now > (next_scheduled_update):
            self.logger.info("Running scheduled update: %s > %s" % (self.format_time(now), self.format_time(next_scheduled_update)))
            status = self.check_and_update()
        else:
            self.logger.info("Skipping check: %s < %s" % (self.format_time(now), self.format_time(next_scheduled_update)))

        if status['success']:
            if status['updated']:
                if status['need_reset']:
                    if automatic_reset:
                        self.logger.warning("Reset requested and automatic_reset = True - Resetting")
                        machine.soft_reset()
                    else:
                        self.logger.warning("Reset requested and automatic_reset = False - Luck")
        else:
            self.logger.warning("Update failed")

    def check_and_update(self):
        status = {
            "updated": False,
            "need_reset": False,
            "success": False
        }

        self.logger.debug("remote manifest url: %s" % self.remote_manifest_url())

        self.get_remote_manifest()
        if not self.remote_manifest:
            self.logger.warning("Problems getting remote manifest")
            return status

        if self.versions_differ():
            try:
                self.download_and_write_update()
                status['success'] = True
                status['need_reset'] = True
            except:
                status['success'] = False
        else:
            self.logger.info("no update required")
            status['success'] = True
            status['need_reset'] = False

        if status['success']:
            self.commit_manifest()

        return status

    def next_package_url(self):
        return self.remote_manifest['package_url']

    def download_and_write_update(self):
        self.logger.debug("Updating from: %s" % self.next_package_url())

        self.download_and_save_package(self.next_package_url())
        self.extract_files()

        self.logger.debug("deleting package.tar")
        os.remove("package.tar")

    def download_and_save_package(self, path):
        self.logger.debug("Source: %s" % path)
        fp = open('package.tar', 'wb')
        bytes = fp.write(requests.get(path).content)
        fp.close()
        self.logger.debug("Wrote %s bytes" % bytes)

    def extract_files(self):
        tf = utarfile.TarFile('package.tar')

        bytes_written = 0
        extracted_files = []

        for i in tf:
            if i.type == utarfile.DIRTYPE:
                self.logger.debug("mkdir: %s" % i.name)
                try:
                    os.mkdir(i.name)
                except:
                    pass
            else:

                try:
                    self.logger.debug("deleting: %s" % i.name)
                    os.remove(i.name)
                except:
                    pass

                f = tf.extractfile(i)
                contents = f.read()

                self.logger.info("writing: %s" % i.name)
                fp = open(i.name, 'wb')
                bytes = fp.write(contents)
                fp.close()
                self.logger.debug("Wrote %s bytes to %s" % (bytes, i.name))
                extracted_files.append(i.name)
                bytes_written = bytes_written + bytes

        self.logger.info("extracted files: %s" % extracted_files)


    def commit_manifest(self):
        self.manifest = self.remote_manifest
        self.manifest['last_update_check'] = time.mktime(time.gmtime())

        with open("manifest.json", 'w') as new_manifest_fp:
            json.dump(self.remote_manifest, new_manifest_fp)
            self.logger.info("wrote new manifest")
            self.logger.debug(self.manifest)

    def versions_differ(self):
        if self.manifest['version'] != self.remote_manifest['version']:
            self.logger.warning("should update: %s vs %s" % (self.manifest['version'], self.remote_manifest['version']))
            return True
        else:
            return False

    def remote_manifest_url(self):
        return "".join([self.base_url, self.device_name, ".json"])

    def get_remote_manifest(self):
        try:
            self.remote_manifest = requests.get(self.remote_manifest_url()).json()
        except ValueError as error:
            self.logger.warning("Got invalid JSON")
            self.remote_manifest = False

    def load_local_manifest(self):
        self.manifest = {}
        if 'manifest.json' in os.listdir():
            with open('manifest.json', 'r') as current_manifest_fp:
                try:
                    self.manifest = json.load(current_manifest_fp)
                except:
                    self.logger.critical("Error in reading local manifest.json")
                    pass
        else:
            self.logger.error("No manifest.json found")

        if 'version' not in self.manifest:
            self.logger.debug("Manifest did not contain $.version, set to None")
            self.manifest['version'] = None

        if 'last_update_check' not in self.manifest:
            self.manifest['last_update_check'] = 0
            self.logger.debug("Manifest did not contain $.last_update_check, set to 0")
