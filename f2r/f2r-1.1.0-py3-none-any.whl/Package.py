import re
import os

from . import config
from .helpers import parseRecipeHeader
from .Module import Module
from .Defaults import Defaults


class Package:

    def __init__(self, name, version):
        self.name = name
        self.path = os.path.join(config.ali_prefix, 'alidist', name.lower() + '.sh')

        parsed = parseRecipeHeader(self.path)
        self.requires = parsed['requires'] if 'requires' in parsed.keys() else []
        # self.tag = parsed['tag'] TODO: prefer tag over version
        self.module_version = version
        self.module_dep_versions = Module(name).deps_as_dict(version)
        self.defaults = Defaults()

    def deps(self):
        """ List of deps with already applied arch and defaults filters """
        filtered = []
        # Filter on arch
        for dep in self.requires:
            filter = dep.split(':')
            if len(filter) == 2:
                x = re.match(filter[1], config.architecture)
                if x and filter[0]:
                    filtered.append(filter[0])
            else:
                filtered.append(dep)
        # Filter on disable from defaults
        if self.defaults is not None:
            return [x for x in filtered if x not in self.defaults.disable]
        return filtered

    def deps_with_versions(self):
        """ In addition to list of dependencies it provides correct versions from modulefile """
        dict = {}
        deps = self.deps()
        for dep in deps:
            if dep in self.module_dep_versions.keys():
                dict[dep] = self.module_dep_versions[dep]
            else:
                dict[dep] = 'from_system'  # TODO: rename dep into system RPM name
        return dict

    def get_extra_deps(self):
        """ Provide extran deps list coming from alidist recipe """
        with open(self.path) as recipe:
            content = recipe.read()
            found = re.search(r'cat ' + re.escape('> $INSTALLROOT/.rpm-extra-deps <<') + 'EoF\n.*?EoF', content, re.DOTALL)
            if found is not None:
                return found.group().split('\n')[1:-1]
        return []
