#!/usr/bin/env python
# vim: set fileencoding=utf-8 :

from setuptools import setup, dist

dist.Distribution(dict(setup_requires=["bob.extension"]))

from bob.extension.utils import load_requirements, find_packages

install_requires = load_requirements()

setup(
    name="bob.bio.vein",
    version=open("version.txt").read().rstrip(),
    description="Vein Recognition Library",
    url="https://gitlab.idiap.ch/bob/bob.bio.vein",
    license="GPLv3",
    author="Andre Anjos,Pedro Tome",
    author_email="andre.anjos@idiap.ch,pedro.tome@idiap.ch",
    keywords="bob, biometric recognition, evaluation, vein",
    long_description=open("README.rst").read(),
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=install_requires,
    entry_points={
        "bob.bio.config": [
            # protocols (must be specified before the database in the cmd)
            # verafinger
            "Nom = bob.bio.vein.config.database.protocol_verafinger.nom",
            "Cropped-Nom = bob.bio.vein.config.database.protocol_verafinger.cropped_nom",
            "Full = bob.bio.vein.config.database.protocol_verafinger.full",
            "Cropped-Full = bob.bio.vein.config.database.protocol_verafinger.cropped_full",
            # utfvp
            "nom = bob.bio.vein.config.database.protocol_utfvp.nom",
            "full = bob.bio.vein.config.database.protocol_utfvp.full",
            "1vsall = bob.bio.vein.config.database.protocol_utfvp.one_vs_all",
            # fv3d
            "central = bob.bio.vein.config.database.protocol_fv3d.central",
            "left = bob.bio.vein.config.database.protocol_fv3d.left",
            "right = bob.bio.vein.config.database.protocol_fv3d.right",
            "stitched = bob.bio.vein.config.database.protocol_fv3d.stitched",
            # putvein
            "wrist-LR-1 = bob.bio.vein.config.database.protocol_putvein.wrist_lr_1",
            "wrist-LR-4 = bob.bio.vein.config.database.protocol_putvein.wrist_lr_4",
            "palm-LR-1 = bob.bio.vein.config.database.protocol_putvein.palm_lr_1",
            "palm-LR-4 = bob.bio.vein.config.database.protocol_putvein.palm_lr_4",
            # legacy databases
            "verafinger = bob.bio.vein.config.database.verafinger",
            "utfvp = bob.bio.vein.config.database.utfvp",
            "fv3d = bob.bio.vein.config.database.fv3d",
            "putvein = bob.bio.vein.config.database.putvein",
            # legacy baselines
            "mc = bob.bio.vein.config.maximum_curvature",
            "rlt = bob.bio.vein.config.repeated_line_tracking",
            "wld = bob.bio.vein.config.wide_line_detector",
        ],
        "bob.bio.database": [
            "verafinger = bob.bio.vein.config.database.verafinger:database",
            "utfvp = bob.bio.vein.config.database.utfvp:database",
            "fv3d = bob.bio.vein.config.database.fv3d:database",
            "putvein = bob.bio.vein.config.database.putvein:database",
        ],
        "bob.bio.pipeline": [
            "wld = bob.bio.vein.config.wide_line_detector:pipeline",
            "mc = bob.bio.vein.config.maximum_curvature:pipeline",
            "rlt = bob.bio.vein.config.repeated_line_tracking:pipeline",
        ],
        "console_scripts": [
            "bob_bio_vein_compare_rois.py = bob.bio.vein.script.compare_rois:main",
            "bob_bio_vein_view_sample.py = bob.bio.vein.script.view_sample:main",
            "bob_bio_vein_blame.py = bob.bio.vein.script.blame:main",
            "bob_bio_vein_markdet.py = bob.bio.vein.script.markdet:main",
            "bob_bio_vein_watershed_mask.py = bob.bio.vein.script.watershed_mask:main",
        ],
    },
    classifiers=[
        "Framework :: Bob",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Natural Language :: English",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
