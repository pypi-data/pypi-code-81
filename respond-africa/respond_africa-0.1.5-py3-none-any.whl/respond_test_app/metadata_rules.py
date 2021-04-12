from edc_constants.constants import NO, NOT_APPLICABLE, YES
from edc_metadata import NOT_REQUIRED, REQUIRED
from edc_metadata.metadata_rules import CrfRule, CrfRuleGroup, P, register
from respond_model.utils import is_baseline


def func_glucose_baseline_required(visit=None, **kwargs):
    return is_baseline(visit)


def func_glucose_required(visit=None, **kwargs):
    return not is_baseline(visit)


@register()
class ClinicalReviewBaselineRuleGroup(CrfRuleGroup):

    hiv = CrfRule(
        predicate=P("hiv_dx", "eq", YES),
        consequence=REQUIRED,
        alternative=NOT_REQUIRED,
        target_models=["hivinitialreview"],
    )

    dm = CrfRule(
        predicate=P("dm_dx", "eq", YES),
        consequence=REQUIRED,
        alternative=NOT_REQUIRED,
        target_models=["dminitialreview"],
    )

    htn = CrfRule(
        predicate=P("htn_dx", "eq", YES),
        consequence=REQUIRED,
        alternative=NOT_REQUIRED,
        target_models=["htninitialreview"],
    )

    chol = CrfRule(
        predicate=P("chol_dx", "eq", YES),
        consequence=REQUIRED,
        alternative=NOT_REQUIRED,
        target_models=["cholinitialreview"],
    )

    class Meta:
        app_label = "respond_test_app"
        source_model = "respond_test_app.clinicalreviewbaseline"


@register()
class ClinicalReviewRuleGroup(CrfRuleGroup):

    hiv_dx = CrfRule(
        predicate=P("hiv_dx", "eq", YES),
        consequence=REQUIRED,
        alternative=NOT_REQUIRED,
        target_models=["hivinitialreview"],
    )

    dm_dx = CrfRule(
        predicate=P("dm_dx", "eq", YES),
        consequence=REQUIRED,
        alternative=NOT_REQUIRED,
        target_models=["dminitialreview"],
    )

    htn_dx = CrfRule(
        predicate=P("htn_dx", "eq", YES),
        consequence=REQUIRED,
        alternative=NOT_REQUIRED,
        target_models=["htninitialreview"],
    )

    chol_dx = CrfRule(
        predicate=P("chol_dx", "eq", YES),
        consequence=REQUIRED,
        alternative=NOT_REQUIRED,
        target_models=["cholinitialreview"],
    )

    hiv_test = CrfRule(
        predicate=P("hiv_test", "eq", NOT_APPLICABLE),
        consequence=REQUIRED,
        alternative=NOT_REQUIRED,
        target_models=["hivreview"],
    )

    dm_test = CrfRule(
        predicate=P("dm_test", "eq", NOT_APPLICABLE),
        consequence=REQUIRED,
        alternative=NOT_REQUIRED,
        target_models=["dmreview"],
    )

    htn_test = CrfRule(
        predicate=P("htn_test", "eq", NOT_APPLICABLE),
        consequence=REQUIRED,
        alternative=NOT_REQUIRED,
        target_models=["htnreview"],
    )

    chol_test = CrfRule(
        predicate=P("chol_test", "eq", NOT_APPLICABLE),
        consequence=REQUIRED,
        alternative=NOT_REQUIRED,
        target_models=["cholreview"],
    )

    complications = CrfRule(
        predicate=P("complications", "eq", YES),
        consequence=REQUIRED,
        alternative=NOT_REQUIRED,
        target_models=["complicationsfollowup"],
    )

    class Meta:
        app_label = "respond_test_app"
        source_model = "respond_test_app.clinicalreview"


@register()
class MedicationsRuleGroup(CrfRuleGroup):

    refill_hiv = CrfRule(
        predicate=P("refill_hiv", "eq", YES),
        consequence=REQUIRED,
        alternative=NOT_REQUIRED,
        target_models=["drugrefillhiv"],
    )

    refill_dm = CrfRule(
        predicate=P("refill_dm", "eq", YES),
        consequence=REQUIRED,
        alternative=NOT_REQUIRED,
        target_models=["drugrefilldm"],
    )

    refill_htn = CrfRule(
        predicate=P("refill_htn", "eq", YES),
        consequence=REQUIRED,
        alternative=NOT_REQUIRED,
        target_models=["drugrefillhtn"],
    )

    refill_chol = CrfRule(
        predicate=P("refill_chol", "eq", YES),
        consequence=REQUIRED,
        alternative=NOT_REQUIRED,
        target_models=["drugrefillchol"],
    )

    adherence_hiv = CrfRule(
        predicate=P("refill_hiv", "in", [YES, NO]),
        consequence=REQUIRED,
        alternative=NOT_REQUIRED,
        target_models=["hivmedicationadherence"],
    )

    adherence_dm = CrfRule(
        predicate=P("refill_dm", "in", [YES, NO]),
        consequence=REQUIRED,
        alternative=NOT_REQUIRED,
        target_models=["dmmedicationadherence"],
    )

    adherence_htn = CrfRule(
        predicate=P("refill_htn", "in", [YES, NO]),
        consequence=REQUIRED,
        alternative=NOT_REQUIRED,
        target_models=["htnmedicationadherence"],
    )

    adherence_chol = CrfRule(
        predicate=P("refill_chol", "in", [YES, NO]),
        consequence=REQUIRED,
        alternative=NOT_REQUIRED,
        target_models=["cholmedicationadherence"],
    )

    class Meta:
        app_label = "respond_test_app"
        source_model = "respond_test_app.medications"
