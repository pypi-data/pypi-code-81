import subprocess
import os
import re
from utils.message import Message


class Git(object):

    def __init__(self, user, key):
        self.project_path = os.environ["working_path"]
        self.user = user
        self.key = key
        self.message = Message("Update git operation logs")

    def _execute_git_command(self, cmd):
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        (std_output, _) = process.communicate()
        ret = process.poll()
        self.message.add_message("Execute: {}\n Logs:{}".format(cmd, std_output.decode("utf-8")))
        return std_output, ret

    def hard_reset(self):
        cmd = "cd {} && git reset --hard".format(self.project_path)
        std_output, ret = self._execute_git_command(cmd)
        return std_output, ret

    def get_project_link(self):
        cmd = "cd {} && git remote -v".format(self.project_path)
        std_output, ret = self._execute_git_command(cmd)
        links = re.findall("(http.*?\.git)", std_output.decode("utf-8"))
        link = links[0] if links else None
        return link

    def pull(self):
        std_output, ret = "", -1
        link = self.get_project_link()
        if link is not None:
            authentication = "//{}:{}@".format(self.user, self.key)
            link = link.replace("//", authentication)
            cmd = "cd {} && git pull {}".format(self.project_path, link)
            std_output, ret = self._execute_git_command(cmd)
        return std_output, ret

    def update_latest_code(self):
        std_output, ret = self.hard_reset()
        if ret == 0 :
            self.message.add_message("Git hard reset succeed")
            std_output, ret = self.pull()
        else:
            self.message.add_message("Git hard reset Failed, skip git pull ")

        return self.message.message, ret
