from setuptools import setup, find_packages

VERSION = '0.0.3' 
DESCRIPTION = "A library for visualizing emotions detected in corpora according to Plutchik's model."
LONG_DESCRIPTION = "PyPlutchik is a library specifically designed for the visualisation of Plutchik’s emotions in texts or in corpora. PyPlutchik draws the Plutchik’s flower with each emotion petal sized after how much that emotion is detected or annotated in the corpus, also representing three degrees of intensity for each of them. PyPlutchik allows users to display also primary, secondary, tertiary and opposite dyads."

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="pyplutchik", 
        version=VERSION,
        author="Alfonso Semeraro",
        author_email="<alfonso.semeraro@gmail.com>",
        url='https://github.com/alfonsosemeraro/pyplutchik',
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=['matplotlib', 'pandas', 'shapely', 'descartes', 'numpy'],        
        keywords=['python', 'dataviz', 'emotions', 'plutchik'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Science/Research",
            "Programming Language :: Python :: 3"
        ]
)