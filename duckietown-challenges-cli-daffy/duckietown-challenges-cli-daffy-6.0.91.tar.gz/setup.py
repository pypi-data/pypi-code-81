from setuptools import find_packages, setup


def get_version(filename):
    import ast

    version = None
    with open(filename) as f:
        for line in f:
            if line.startswith("__version__"):
                version = ast.parse(line).body[0].value.s
                break
        else:
            raise ValueError("No version found in %r." % filename)
    if version is None:
        raise ValueError(filename)
    return version


line = "daffy"

install_requires = [
    "termcolor",
    "decorator",
    "PyYAML",
    "python-dateutil",
    "numpy",
    "zuper-commons-z6>=6.1.6",
    "zuper-ipce-z6>=6",
    "configparser",
    "paramiko",  # docker ssh
    "pur",  # not needed for code but for aido
    f"duckietown-build-utils-{line}>=6.0.14",
    f"duckietown-docker-utils-{line}",
    f"duckietown-challenges-{line}",
    # f"duckietown-docker-utils-{line}>=6.0.0",
    f"duckietown-challenges-runner-{line}>=6.2.2",
]

version = get_version(filename="src/duckietown_challenges_cli/__init__.py")

setup(
    name=f"duckietown-challenges-cli-{line}",
    version=version,
    download_url="http://github.com/duckietown/duckietown-challenges-cli/tarball/%s" % version,
    package_dir={"": "src"},
    packages=find_packages("src"),
    install_requires=install_requires,
    tests_require=[],
    # This avoids creating the egg file, which is a zip file, which makes our data
    # inaccessible by dir_from_package_name()
    zip_safe=False,
    # without this, the stuff is included but not installed
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "dt-challenges-make-readme-definitions  = duckietown_challenges_cli:make_readmes_main",
            "dt-challenges-make-readme-templates  = duckietown_challenges_cli:make_readmes_templates_main",
            "dt-challenges-cli = duckietown_challenges_cli:dt_challenges_cli_main",
            "dt-build_utils-cli = duckietown_challenges_cli:dt_build_utils_cli_main",
        ]
    },
)
