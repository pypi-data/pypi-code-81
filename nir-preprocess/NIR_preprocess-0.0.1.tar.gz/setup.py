import setuptools


setuptools.setup(
    name="NIR_preprocess",
    version="0.0.1",
    author="Giverny Robert",
    author_email="giverny.robert@usherbrooke.ca",
    
    packages=["NIR_preprocess"],
    description="Function to evaluate impact of NIR pre-processing techniques on spectral data",
    long_description="Function using multiblock partial least squares to evaluate impact of different pre-processing techniques\
        \n\
        \nDifferent pre-processing techniques tested from RG module:\
        \nbaseline, detrend, EMSC, MSC, SNV, savitzky_golay\
        \n\
        \n MBPLS function from RG module ",
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)