""" timed rotating text file """
# pylint: disable=too-many-instance-attributes,too-many-arguments
import os
import re
import time
from datetime import datetime
from io import TextIOWrapper
from stat import ST_MTIME


class TimedRotatingTextFile(TextIOWrapper):
    """ Rotating the text file at certain timed intervals. """

    def __init__(
        self,
        filename,
        when="d",
        interval=1,
        backup_count=0,
        mode="ab+",
        delay=False,
        utc=False,
        **kwargs
    ):
        self.file = open(filename, mode)
        self.filename = filename
        self.when = when.upper()

        self.backup_count = backup_count
        self.mode = mode
        self.delay = delay
        self.utc = utc

        super().__init__(self.file, **kwargs)

        if self.when in ["D", "MIDNIGHT"]:
            self.interval = 60 * 60 * 24  # One day
            self.suffix = "%Y-%m-%d"
            self.regex_match = r"^\d{4}-\d{2}-\d{2}(\.\w+)?$"
        elif self.when == "H":
            self.interval = 60 * 60  # One hour
            self.suffix = "%Y-%m-%d_%H"
            self.regex_match = r"^\d{4}-\d{2}-\d{2}_\d{2}(\.\w+)?$"
        elif self.when == "M":
            self.interval = 60  # one minute
            self.suffix = "%Y-%m-%d_%H-%M"
            self.regex_match = r"^\d{4}-\d{2}-\d{2}_\d{2}-\d{2}(\.\w+)?$"
        else:
            raise ValueError("Invalid rollover interval specified: %s" % self.when)

        self.interval = self.interval * interval  # multiply by units requested
        self.ext_match = re.compile(self.regex_match, re.ASCII)

        file_name = os.fspath(self.filename)
        # keep the absolute path, otherwise derived classes which use this
        # may come a cropper when the current directory changes
        self.base_file_name = os.path.abspath(file_name)
        if os.path.exists(self.base_file_name):
            modified_time = os.stat(self.base_file_name)[ST_MTIME]
        else:
            modified_time = int(time.time())

        self.rollover_at = self.compute_rollover(modified_time)

    def compute_rollover(self, current_time):
        """ Work out the rollover time based on the specified time. """
        result = current_time + self.interval
        if self.when == "MIDNIGHT":
            rotate_ts = 24 * 60 * 60
            if self.utc:
                struct_time = time.gmtime(current_time)
            else:
                struct_time = time.localtime(current_time)
            current_hour = struct_time[3]
            current_minute = struct_time[4]
            current_second = struct_time[5]

            rotate_time = rotate_ts - ((current_hour * 60 + current_minute) * 60 + current_second)

            if rotate_time < 0:
                rotate_time += 24 * 60 * 60
            result = current_time + rotate_time
        return result

    def should_rollover(self):
        """ Determine if rollover shoud occur. """
        current_time = int(time.time())
        if current_time >= self.rollover_at:
            return 1
        return 0

    def get_files_to_delete(self):
        """ Determine the files to delete when rolling over. """
        dir_name, base_name = os.path.split(self.base_file_name)
        files_name = os.listdir(dir_name)
        result = []
        prefix = base_name + "."
        prefix_len = len(prefix)
        for filename in files_name:
            if filename[:prefix_len] == prefix:
                suffix = filename[prefix_len:]
                if self.ext_match.match(suffix):
                    result.append(os.path.join(dir_name, filename))
        if len(result) < self.backup_count:
            return []
        result.sort()
        return result[: len(result) - self.backup_count]

    def do_rollover(self):
        """ do a rollover; in this case, a date/time stamp is appended to the filename
        when the rollover happens.  However, you want the file to be named for the
        start of the interval, not the current time.  If there is a backup count,
        then we have to get a list of matching filenames, sort them and remove
        the one with the oldest suffix. """
        current_time = int((time.time()))
        dst_now = time.localtime(current_time)[-1]
        timed = self.rollover_at - self.interval
        if self.utc:
            time_tuple = time.gmtime(timed)
        else:
            time_tuple = time.localtime(timed)
            dst_then = time_tuple[-1]
            if dst_now != dst_then:
                addend = 3600 if dst_now else -3600
                time_tuple = time.localtime(timed + addend)
        dfn = self.base_file_name + "." + time.strftime(self.suffix, time_tuple)
        if os.path.exists(dfn):
            os.remove(dfn)
        if os.path.exists(self.base_file_name):
            os.rename(self.base_file_name, dfn)
        if self.backup_count > 0:
            for file_path in self.get_files_to_delete():
                os.remove(file_path)
        if not self.delay:
            open(self.base_file_name, self.mode)
        new_rollover_at = self.compute_rollover(current_time)
        while new_rollover_at <= current_time:
            new_rollover_at = new_rollover_at + self.interval
        if self.when == "MIDNIGHT" and not self.utc:
            dst_at_rollover = time.localtime(new_rollover_at)[-1]
            if dst_now != dst_at_rollover:
                addend = -3600 if not dst_now else 3600
                new_rollover_at += addend
        self.rollover_at = new_rollover_at

    def write(self, line):
        if self.should_rollover():
            self.do_rollover()
        return super().write(line)

    def close(self):
        super().close()
        self.file.close()


################
# MAIN SECTION #
################
if __name__ == "__main__":
    i = 0
    with TimedRotatingTextFile("/tmp/tmp.log", when="MIDNIGHT", backup_count=5) as filepath:
        while i < 120:
            filepath.write(str(datetime.now().microsecond) + "\n")
            i += 1
