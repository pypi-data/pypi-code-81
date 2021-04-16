"""
This module contains defined blocks. Any block shall inherit from `Block`.
"""

import logging
from collections import defaultdict

from femap_neutral_parser.blocks._base import Block

# =============================================================================
# FEMAP : (FEMAP vectorID, MYSTRAN title, MYSTRAN vectorID)
# =============================================================================
MYSTRAN2FEMAP = {
    "RSS translation": ("Total Translation", 1),
    "T1  translation": ("T1 Translation", 2),
    "T2  translation": ("T2 Translation", 3),
    "T3  translation": ("T3 Translation", 4),
    "RSS rotation": ("Total Rotation", 5),
    "R1  rotation": ("R1 Rotation", 6),
    "R2  rotation": ("R2 Rotation", 7),
    "R3  rotation": ("R3 Rotation", 8),
    "RSS applied force": ("Total Applied Force", 41),
    "T1  applied force": ("T1 Applied Force", 42),
    "T2  applied force": ("T2 Applied Force", 43),
    "T3  applied force": ("T3 Applied Force", 44),
    "RSS applied moment": ("Total Applied Moment", 45),
    "R1  applied moment": ("R1 Applied Moment", 46),
    "R2  applied moment": ("R2 Applied Moment", 47),
    "R3  applied moment": ("R3 Applied Moment", 48),
    "RSS SPC force": ("Total Constraint Force", 51),
    "T1  SPC force": ("T1 Constraint Force", 52),
    "T2  SPC force": ("T2 Constraint Force", 53),
    "T3  SPC force": ("T3 Constraint Force", 54),
    "RSS SPC moment": ("Total Constraint Moment", 55),
    "R1  SPC moment": ("R1 Constraint Moment", 56),
    "R2  SPC moment": ("R2 Constraint Moment", 57),
    "R3  SPC moment": ("R3 Constraint Moment", 58),
    None: ("Elem C2 R3 GPMoment", 85015),
    "BAR EndA Plane1 Moment": ("Bar EndA Plane1 Moment", 3000),
    "BAR EndA Plane2 Moment": ("Bar EndA Plane2 Moment", 3001),
    "BAR EndB Plane1 Moment": ("Bar EndB Plane1 Moment", 3002),
    "BAR EndB Plane2 Moment": ("Bar EndB Plane2 Moment", 3003),
    "BAR EndA Pl1 Shear Force": ("Bar EndA Pl1 Shear Force", 3004),
    "BAR EndA Pl2 Shear Force": ("Bar EndA Pl2 Shear Force", 3005),
    "BAR EndA Axial Force": ("Bar EndA Axial Force", 3008),
    "BAR EndA Torque": ("Bar EndA Torque", 3010),
    "BAR EndA Pt1 Comb Stress": ("Bar EndA Pt1 Bend Stress", 3075),
    "BAR EndA Pt2 Comb Stress": ("Bar EndA Pt2 Bend Stress", 3076),
    "BAR EndA Pt3 Comb Stress": ("Bar EndA Pt3 Bend Stress", 3077),
    "BAR EndA Pt4 Comb Stress": ("Bar EndA Pt4 Bend Stress", 3078),
    "BAR EndB Pt1 Comb Stress": ("Bar EndB Pt1 Bend Stress", 3083),
    "BAR EndB Pt2 Comb Stress": ("Bar EndB Pt2 Bend Stress", 3084),
    "BAR EndB Pt3 Comb Stress": ("Bar EndB Pt3 Bend Stress", 3085),
    "BAR EndB Pt4 Comb Stress": ("Bar EndB Pt4 Bend Stress", 3086),
    "BAR EndA Max Stress": ("Bar EndA Max Comb Stress", 3109),
    "BAR EndA Min Stress": ("Bar EndA Min Comb Stress", 3110),
    "BAR EndB Max Stress": ("Bar EndB Max Comb Stress", 3111),
    "BAR EndB Min Stress": ("Bar EndB Min Comb Stress", 3112),
}
# =============================================================================
# Block B451
# =============================================================================


class B451(Block):
    """
    >>> txt = '''       1,   10001,       1
    ... RSS translation
    ...      0.000000E+00,     1.602912E+00,     1.602912E+00,
    ...    10002,   10003,   10004,       0,       0,       0,       0,       0,       0,       0,
    ...        0,       0,       0,       0,       0,       0,       0,       0,       0,       0,
    ...        1,      12,       1,       7,
    ...        1,       1,       1
    ...        1,     0.000000E+00,
    ...        2,     1.870816E-01,
    ...        3,     0.000000E+00,
    ...        4,     7.011176E-02,
    ...       -1,     0.          ,
    ... '''
    >>> b = B451(version=9.3)
    >>> b.parse(txt)
    >>> from pprint import pprint as pp
    >>> import pprint; pprint.pprint(b.data)
    [{'abs_max': 1.602912,
     'calc_warn': True,
     'cent_total': True,
     'comp_dir': 1,
     'component_vec': [10002.0, 10003.0, 10004.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
     'ent_type': 7,
     'id_max': 12,
     'id_min': 1,
     'max_val': 1.602912,
     'min_val': 0.0,
     'out_type': 1,
     'record': array([(1, 0.        ), (2, 0.1870816 ), (3, 0.        ), (4, 0.07011176)],
          dtype=[('entityID', '<i8'), ('value', '<f8')]),
     'setID': 1,
     'title': 'RSS translation',
     'vecID': 10001}]
    """

    NAME = "output_vectors"
    RECORDS = [
        [
            {"field": "setID", "coerce": int},
            {"field": "vecID", "coerce": int},
            {"field": "_", "coerce": int},
        ],  # 1
        [
            {"field": "title"},
        ],  # 2
        [
            {"field": "min_val", "coerce": float},  # 3
            {"field": "max_val", "coerce": float},
            {"field": "abs_max", "coerce": float},
        ],
        [  # 4 comp[0..9]
            {"field": "component_vec", "coerce": float, "single_line_array": 9},
        ],
        [  # 5 comp[10..19]
            {"field": "_", "coerce": float, "single_line_array": 9},
        ],
        [  # 6
            {"field": "doubled_sided_contour", "coerce": int, "v+": "10.0"},
        ],
        [  # 7
            {"field": "id_min", "coerce": int},
            {"field": "id_max", "coerce": int},
            {"field": "out_type", "coerce": int},
            {"field": "ent_type", "coerce": int},
        ],
        [  # 8
            {"field": "calc_warn", "coerce": bool},
            {"field": "comp_dir", "coerce": int, "v+": "4.1"},
            {"field": "cent_total", "coerce": bool},
        ],
        [  # 1 record for each entry, plus last record
            {
                "multi_line_array": True,
                "field": "record",
                "fields": ("entityID", "value"),
                "coerce": (int, float),
            },
        ],
    ]

    def digest(self):
        agg = defaultdict(dict)
        for data in self.data:
            # -----------------------------------------------------------------
            # affect appropriate columns headers
            ent_type = {7: "nodeID", 8: "eltID"}[data.pop("ent_type")]
            out_type = {
                0: "value",
                1: "disp",
                2: "accel",
                3: "force",
                4: "stress",
                5: "strain",
                6: "temp",
            }.get(data.pop("out_type"), "user")
            # -----------------------------------------------------------------
            # modify MYSTRAN titles and setIDs
            title = data.pop("title")
            title, vecID = MYSTRAN2FEMAP.get(title, (title, data["vecID"]))
            data["vecID"] = vecID
            agg[title][data.pop("setID")] = data
            data["record"].dtype.names = (ent_type, title)
        return dict(agg)


if __name__ == "__main__":
    import doctest

    doctest.testmod(optionflags=doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE)
    # import sys
    # filepath =sys.argv[1]
