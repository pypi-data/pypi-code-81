import os
import re
import logging
import sys

from . import config
from .helpers import parseYamlDict
from .helpers import runSubprocess

class Fpm:
  """ Class to handle fpm invocations """
  def __init__(self):
    self.buildDir = os.path.join(config.ali_prefix, 'sw', config.architecture)
    self.forceBuild = ['--force'] if config.force_build else []
    self.packagePrefix = "o2-"
    self.targetDir = config.target_rpm_dir
    self.skipDeps = ['openmp', 'VecGeom']  # as sometimes there's mismatch between "requires" deps and modulefile

    # Check fpm
    if not config.dry_run:
      runSubprocess(['/bin/which', 'fpm'])

    # Create output dir
    if not os.path.exists(self.targetDir):
      os.makedirs(self.targetDir)

    arch_split = config.architecture.split('_')
    self.architecture = arch_split[1].replace('-', '_')
    self.release_suffix = arch_split[0]

    self.runtimeDepsDict = parseYamlDict(os.path.join(config.work_dir, 'runtime.' + self.release_suffix + '.yaml'))

  def run(self, name, version, deps, extra_deps, RPMS_GENERATED):
    """ Prepares arguments and executes fpm """
    fullVersion = version
    # split version and revision
    version_split = version.split('-')
    # split in case of vX.Y.Z-R
    # don't split if e.g. latest-o2-dataflow
    if len(version_split) == 2:
      version = version_split[0]
      iterationArg = ['--iteration', version_split[1] + '.' + self.release_suffix]
    else:
      iterationArg = ['--iteration', self.release_suffix]

    # prep dir arguments
    # `=.` is necessary so that the complete source dir path
    # is not replicated and the target dir consists of only
    # prefix + package name + dir
    package_dir = self.buildDir + "/" + name + "/" + fullVersion + "/"
    subdirs = ['bin', 'lib', 'lib64', 'etc', 'include', 'bin-safe', 'libexec', 'WebDID']
    paths = []
    for subdir in subdirs:
      if os.path.exists(package_dir + subdir):
        paths.append(package_dir + subdir + '=.')

    # Handle extra_deps
    extra_deps = [v for dep in extra_deps for v in ('--depends', dep)]

    fpmCommand = ['fpm',
      '-s', 'dir',
      '-t', 'rpm',
      '--log', 'warn',
      *self.translateDepsToArgs(deps),
      *extra_deps,
      *self.forceBuild,
      '-p', self.targetDir,
      '--architecture', self.architecture,
      '--prefix', '/opt/o2/',
      '-n', self.packagePrefix + name,
      '--version', version,
      *iterationArg,
      '--rpm-auto-add-directories',
      '--template-scripts',
      '--after-install', os.path.join(config.work_dir, 'after_install_template.sh'),
      '--after-remove', os.path.join(config.work_dir, 'after_remove_template.sh'),
      '--exclude=*/modulefiles', '--exclude=*/profile.d',
      *paths]

    if not config.dry_run:
      ret = runSubprocess(fpmCommand, failOnError=False)
      if not ret:
          logging.warn('Generation of the RPM skipped')
      else:
          # try to parse the generated RPM path from the fpm output
          match = re.search(':path=>\"(.*)\"}', ret)
          generatedRpmPath = match.group(1) if match else ''
          RPMS_GENERATED.append(generatedRpmPath)
    else:
      print(*fpmCommand)
      return ''

  def translateDepsToArgs(self, deps):
    """ Prepares dependency arguments for fpm """
    depsArg = []
    for depName, depVersion in deps.items():
      if depName not in self.skipDeps:
        if (depVersion != "from_system"):
          depsArg.extend(['--depends', self.packagePrefix + depName + ' >= ' + depVersion])
        else:  # coming from system, get name from dict
          if depName not in self.runtimeDepsDict:
            logging.critical('Could not find system dependency: %s \nDoes it suppose to come from aliBuild?' % (depName))
            sys.exit(1)
          for dep in self.runtimeDepsDict.get(depName):
            depsArg.extend(['--depends', dep])
    return depsArg
