""" setup """
import pprint
import setuptools


def file_content(file_name: str) -> str:
    """ returning content of the file specified by file_name arg as string.

    :param file_name:   file name to load into a string.
    :return:            file content string.
    """
    with open(file_name) as file_handle:
        return file_handle.read()


if __name__ == "__main__":
    portion_license = "OSI Approved :: GNU General Public License v3 or later (GPLv3+)"
    setup_kwargs = dict(
        name='de_core',              # pip install name (not the import package name)
        version='0.0.20',
        author="Andi Ecker",
        author_email="aecker2@gmail.com",
        description="de_core portion of python development environment namespace package",
        license=portion_license,
        long_description=file_content("README.md"),
        long_description_content_type="text/markdown",
        url="https://gitlab.com/degroup/de_core",
        # don't needed for native/implicit namespace packages: namespace_packages=[namespace_name],
        # packages=setuptools.find_packages(),
        packages=setuptools.find_namespace_packages(include=['de']),  # find namespace portions
        python_requires=">=3.6",
        classifiers=[
            "Development Status :: 1 - Planning",
            "Natural Language :: English",
            "Operating System :: OS Independent",
            "Programming Language :: Python",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.6",
            "License :: " + portion_license,
            "Operating System :: OS Independent",
            "Topic :: Software Development :: Libraries",
        ],
        keywords=[
            'productivity',
            'environment',
            'configuration',
            'development',
        ]
    )
    print("#  EXECUTING SETUPTOOLS SETUP #################################")
    print(pprint.pformat(setup_kwargs, indent=3, width=75, compact=True))
    setuptools.setup(**setup_kwargs)
    print("#  FINISHED SETUPTOOLS SETUP  #################################")
