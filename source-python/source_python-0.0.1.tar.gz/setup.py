import setuptools

setuptools.setup(
	name="source_python",
	version="0.0.1",
	author="Source-Python-Dev-Team",
	description="Source.Python is an open-source project that uses boost::python to allow scripters to interact with Valve's Source-engine.",
	url="https://github.com/Source-Python-Dev-Team/Source.Python",
	packages=setuptools.find_packages(),
	python_requires='>=3.6',
)