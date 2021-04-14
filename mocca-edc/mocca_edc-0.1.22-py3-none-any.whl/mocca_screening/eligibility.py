from typing import Optional, Protocol

from edc_constants.constants import NO, NOT_APPLICABLE, YES
from edc_screening.screening_eligibility import ScreeningEligibility

from .stubs import SubjectScreeningModelStub


class Stub(Protocol):
    model_obj: SubjectScreeningModelStub


class MoccaScreeningEligibility(ScreeningEligibility):
    @property
    def eligible(self: Stub):
        """Returns True or False."""
        eligible = False
        if self.model_obj.unsuitable_for_study == YES:
            eligible = False
        elif (
            self.model_obj.mocca_register
            and self.model_obj.pregnant in [NO, NOT_APPLICABLE]
            and self.model_obj.care == YES
            and self.model_obj.requires_acute_care == NO
            and self.model_obj.willing_to_consent == YES
        ):
            eligible = True
        return eligible

    @property
    def reasons_ineligible(self: Stub) -> Optional[dict]:
        """Returns a dictionary of reasons ineligible."""
        reasons_ineligible = None
        if not self.model_obj.eligible:
            reasons_ineligible = {}
            if self.model_obj.unsuitable_for_study == YES:
                reasons_ineligible.update(unsuitable_for_study="Subject unsuitable")
            if self.model_obj.care != YES:
                reasons_ineligible.update(not_in_care="Not in care")
            if self.model_obj.pregnant not in [NO, NOT_APPLICABLE]:
                reasons_ineligible.update(pregnant="Pregnant (unconfirmed)")
            if self.model_obj.requires_acute_care != NO:
                reasons_ineligible.update(requires_acute_care="Requires acute care")
            if self.model_obj.willing_to_consent != YES:
                reasons_ineligible.update(unwilling_to_consent="Not willing to consent")
        return reasons_ineligible
