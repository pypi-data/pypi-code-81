from qpimage.meta import MetaDict, DATA_DEF, OTHER_DEF


OTHER_DEF_FL = OTHER_DEF.copy()
OTHER_DEF_FL["flimage version"] = "flimage software version used"
OTHER_DEF_FL.pop("sim index")
OTHER_KEYS_FL = sorted(OTHER_DEF_FL.keys())

DATA_DEF_FL = DATA_DEF.copy()
DATA_DEF_FL.pop("wavelength")
DATA_DEF_FL.pop("medium index")
DATA_KEYS_FL = sorted(DATA_DEF_FL.keys())

#: valid :class:`flimage.core.FLImage` meta data keys
META_KEYS_FL = DATA_KEYS_FL + OTHER_KEYS_FL


class FLMetaDict(MetaDict):
    valid_keys = META_KEYS_FL
