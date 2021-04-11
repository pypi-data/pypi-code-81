import distro
import logging
import os, sys
import subprocess

class run_bash(subprocess.Popen):
    def __init__(self, args, shell=True, stdin=None, stdout=open('/var/log/packageManager.log', 'wb'), stderr=subprocess.STDOUT, executable='/bin/bash', cwd=None):
        subprocess.Popen.__init__(self, args=args, shell=shell, stdin=stdin, stdout=stdout, stderr=stderr, executable=executable, cwd=cwd)

class PackageNotFoundError(Exception):
    pass

class CredentialNotRootOrSudoError(Exception):
    pass

class packageManager:
    _logger = logging.getLogger(__name__)
    _distro: tuple
    _packageManager: str

    def __init__(self):
        self._check_uid()
        self._distro = distro.linux_distribution(full_distribution_name=False)
        if (self._distro[0] in ('debian', 'ubuntu')):
            self._packageManager = "apt"
        elif (self._distro[0] in ('fedora', 'cenots')):
            if (self._distro[0] == 'fedora') and ( int(self._distro[1]) >= 22 ):
                self._packageManager = "dnf"
            else:
                self._packageManager = 'yum'
        else:
            self._logger.error("Failed to detect PackageManager for OS " + self._distro[0] + " " + self._distro[1])

    def _check_uid(self):
        if not (os.geteuid() == 0):
            if not 'SUDO_UID' in os.environ.keys():
                raise CredentialNotRootOrSudoError("This program requires super user priv.")

    def _install(self, package):
        self._logger.info('Installing package ' + package)
        if(self._packageManager=='apt'):
            process = run_bash('dpkg -s ' + package)
            process.communicate()[0]
            if (process.returncode):
                process = run_bash('DEBIAN_FRONTEND=noninteractive apt-get -qq install ' + package)
            else:
                self._logger.warning('Already installed ' + package)
                return
        elif (self._packageManager=='dnf'):
            process = run_bash('dnf --assumeyes --quiet install ' + package)
        elif (self._packageManager=='yum'):
            process = run_bash('yum install ' + package)
        process.communicate()[0]
        if process.returncode != 0:
            self._logger.critical('Install failed for package ' + package)
            raise PackageNotFoundError('Install failed for package ' + package + 'code ' + str(process.returncode))

    def install(self, packages):
        if isinstance(packages, str):
            self._install(packages)
        elif isinstance(packages, list):
            for p in packages:
                self._install(p)
        else:
            self._logger.error('Argument type is not string or list. No install!')
            raise TypeError('Argument type is not string or list. No install!')

    def update(self):
        if(self._packageManager=='apt'):
            process = run_bash('DEBIAN_FRONTEND=noninteractive apt-get update')
        elif (self._packageManager=='dnf'):
            process = run_bash('dnf --assumeyes --quiet  upgrade --refresh')
        elif (self._packageManager=='yum'):
            process = run_bash('yum update')
        process.communicate()[0]

    def upgrade(self):
        if(self._packageManager=='apt'):
            process = run_bash('DEBIAN_FRONTEND=noninteractive apt-get upgrade -qq ')
        elif (self._packageManager=='dnf'):
            process = run_bash('dnf  --assumeyes --quiet  upgrade')
        elif (self._packageManager=='yum'):
            process = run_bash('yum upgrade')
        if (process.wait()):
            self._logger.error('System upgrade failed ')

    def system_upgrade(self):
        self.update()
        if (self._packageManager=='dnf'):
            self.install('dnf-plugin-system-upgrade')
            process = run_bash('dnf system-upgrade')
            if (process.wait()):
                self._logger.error('System upgrade failed ')
        self.upgrade()

if __name__ == "__main__":
    exit('Can not be run directly')
