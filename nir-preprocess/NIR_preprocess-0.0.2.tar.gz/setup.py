import setuptools


setuptools.setup(
    name="NIR_preprocess",
    version="0.0.2",
    author="Giverny Robert",
    author_email="giverny.robert@usherbrooke.ca",
    
    packages=["NIR_preprocess"],
    description="Function to evaluate impact of NIR pre-processing techniques on spectral data",
    long_description="\nFunction compare_preprocessing can be used on any NIR spectral data if Y values are available.\
        \nY can include one or several variables.\
        \n\
        \nFunction evaluates impact of different pre-processing techniques and combinations using multiblock partial least squares (MBPLS). Each block in MBPLS is a pre-processed spectral data.\
        \n\
        \nDifferent pre-processing techniques evaluated:\
        \n- baseline\
        \n- de-trend\
        \n- EMSC\
        \n- MSC\
        \n- SNV\
        \n- Savitzky Golay derivatives (different polynomial and derivatives orders can be tested as well as the size of the moving window)\
        \n\
        \nBlocks in MBPLS include:\
        \n- pre-processing techniques and combinations (several techniques applied to same data)\
        \n- original spectral data (starting point)\
        \n- 20 blocks of random noise called false signals (reference for destroyed information)\
        \n\
        \nAnalyst can choose to only compare scatter corrections techniques or only derivatives or both. It is also possible to set the number of pre-processing techniques which can be applied to one same data. By default, only a single pre-processing technique and a combination of 2 are tested. NB: EMSC and MSC can not be applied together\
        \n\
        \nFor MBPLS, analyst can choose:\
        \n- number of principal components\
        \n- to autoscale or center each block\
        \n- to autoscale or center Y\
        \n\
        \nBlocks are represented in superloading plots.\
        \nModel performances (adjusted R2, RMSECV) and variable importance on projection (VIP) are calculated for each block by cross validation. Number of random picks for cross validation and number of lines predicted in each cross validation can be set by the analyst. Effective rank for each block is calculated as well.\
        \n\
        \n# CALL FUNCTION\
        \ncombination, datasets, datasets0, R2_all, R2adj_all, RMSECV_all, VIP_all, Ef_all, Wt = compare_preprocessing(X0, y)\
        \n\
        \n# INPUT ARGUMENTS\
        \n1. X0 (n x k) data to test pre-processing techniques on\
        \n2. y (n x m) property under-study\
        \n\
        \n# OPTIONAL INPUT ARGUMENTS\
        \nnbPC: number of principal components for PLS in the mbPLS decomposition (default value=2)\
        \nnb_comb: maximum number of pre-processing techniques applied on same data (default value=2)\
        \nauto_x: autoscale data after applying pre-processing technique if auto_x=1, if not data centered (default value=1)\
        \nauto_y: autoscale variables to predict if auto_y=1, if not centered (default value=1)\
        \nnb: number of random picks for cross validation\
        \nCVnb: number of samples predicted in each cross validation\
        \nonly_sg: only test Savitzky-Golay if only_sg=1 (default value=0)\
        \nsvg_order: Savitzky-Golay polynomials orders to test\
        \nsvg_deriv: Savitzky-Golay derivatives orders to test\
        \nsvg_window: Savitzky-Golay window sizes to test\
        \nsg_op: test only Savitzky-Golay pretreatments with the same order of polynomial and derivative if sg_op=0 (default value=0)\
        \n\
        \n# OUTPUT\
        \n1. combination: Pre-processing options tested\
        \n2. datasets: data X0 after each pre-processing option and autoscaled or centered\
        \n3. datasets0: data X0 after each pre-processing option\
        \n4. R2_all: R2 values for each y variable predicted for each pre-processing technique tested (block)\
        \n5. R2adj_all: Adjusted for each y variable predicted for each pre-processing technique tested (block)\
        \n6. RMSECV_all: Root mean square error by cross validation for each y variable predicted for each pre-processing technique tested (block)\
        \n7. VIP_all: PLS variable importance in projection for each y variable predicted for each pre-processing technique tested (block)\
        \n8. W: Superloadings from MBPLS\
        \n\
        \n# EXAMPLES\
        \nTwo full examples, along with datasets are provided in folder 'tests' of 'Download Files'. Please refer to 'NIR_preprocess_example.pdf' for full details\
        \n- Example 1: Artificial dataset\
        \n- Example 2: Corn dataset\
        \n\
        \n# COMPATIBILITY\
        \n\compare_preprocessing tested on Python 3.8 using the following modules:\
        \n\- numpy 1.19.2\
        \n\- matplotlib 3.3.2\
        \n\- copy\
        \n\- itertools\
        \n\- RG 0.0.66 (available from Pypi at: https://pypi.org/project/RG/)",
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)