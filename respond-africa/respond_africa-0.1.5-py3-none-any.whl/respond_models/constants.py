from django.conf import settings
from edc_constants.constants import CHOL, DM, HIV, HTN

DIABETES_CLINIC = "diabetes_clinic"
HIV_CLINIC = "hiv_clinic"
HYPERTENSION_CLINIC = "hypertension_clinic"
MORE_THAN_HALF = "more_than_half"
NCD_CLINIC = "ncd_clinic"
NEARLY_EVERYDAY = "nearly_everyday"
NOT_AT_ALL = "not_at_all"
SEQUENTIAL = "sequential"
SEVERAL_DAYS = "several_days"
SYSTEMATIC = "systematic"
CONDITION_ABBREVIATIONS = map(str.lower, [HIV, HTN, DM, CHOL])
BLOOD_RESULTS_EGFR_ACTION = "abnormal-blood-results-egfr"
BLOOD_RESULTS_FBC_ACTION = "abnormal-blood-results-fbc"
BLOOD_RESULTS_GLU_ACTION = "abnormal-blood-results-glu"
BLOOD_RESULTS_HBA1C_ACTION = "abnormal-blood-results-hba1c"
BLOOD_RESULTS_LIPID_ACTION = "abnormal-blood-results-lipid"
BLOOD_RESULTS_LFT_ACTION = "abnormal-blood-results-lft"
BLOOD_RESULTS_RFT_ACTION = "abnormal-blood-results-rft"
RESPOND_DIAGNOSIS_LABELS = getattr(settings, "RESPOND_DIAGNOSIS_LABELS", None)
