#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Tue 27 Sep 2016 16:48:16 CEST

"""Huang's Wide-Line Detector and Miura Matching baseline

References:

1. [HDLTL10]_
2. [TV13]_
3. [TVM14]_

"""
import tempfile
import os

from bob.bio.base.transformers import PreprocessorTransformer
from bob.bio.base.transformers import ExtractorTransformer
from bob.bio.base.pipelines.vanilla_biometrics import (
    VanillaBiometricsPipeline,
    BioAlgorithmLegacy,
)
from sklearn.pipeline import make_pipeline
from bob.pipelines import wrap

from bob.bio.vein.preprocessor import (
    NoCrop,
    TomesLeeMask,
    HuangNormalization,
    NoFilter,
    Preprocessor,
)

from bob.bio.vein.extractor import WideLineDetector
from bob.bio.vein.algorithm import MiuraMatch

"""Baseline updated with the wrapper for the pipelines package"""

"""Sub-directory where temporary files are saved"""
sub_directory = "wld"
default_temp = (
    os.path.join("/idiap", "temp", os.environ["USER"])
    if "USER" in os.environ
    else "~/temp"
)

if os.path.exists(default_temp):
    legacy_temp_dir = os.path.join(default_temp, "bob_bio_base_tmp", sub_directory)
else:
    # if /idiap/temp/<USER> does not exist, use /tmp/tmpxxxxxxxx
    legacy_temp_dir = tempfile.TemporaryDirectory().name

"""Preprocessing using gray-level based finger cropping and no post-processing
"""
preprocessor = PreprocessorTransformer(
    Preprocessor(
        crop=NoCrop(),
        mask=TomesLeeMask(),
        normalize=HuangNormalization(),
        filter=NoFilter(),
    )
)

"""Features are the output of the maximum curvature algorithm, as described on
[HDLTL10]_.

Defaults taken from [TV13]_.
"""
extractor = ExtractorTransformer(WideLineDetector())


"""Miura-matching algorithm with specific settings for search displacement

Defaults taken from [TV13]_.
"""
# Notice the values of ch and cw are different than those from the
# repeated-line tracking **and** maximum curvature baselines.
biometric_algorithm = BioAlgorithmLegacy(
    MiuraMatch(ch=18, cw=28), base_dir=legacy_temp_dir
)

transformer = make_pipeline(wrap(["sample"], preprocessor), wrap(["sample"], extractor))
pipeline = VanillaBiometricsPipeline(transformer, biometric_algorithm)
