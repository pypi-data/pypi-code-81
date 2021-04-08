from .exceptions import PythonPackageLeakage


print('This is a placeholder for an internal library. Yet, this was isntalled from a public index.')
print('install with either a full scm path or system path. e.g.:\n')
print('pip install git+ssh://git@github.com:utahstate/bannercommon#egg=bannercommon\n')
print('OR\n')
print('pip install ../../bannercommon\n')

raise(PythonPackageLeakage("This isn't the package you are looking for..."))
