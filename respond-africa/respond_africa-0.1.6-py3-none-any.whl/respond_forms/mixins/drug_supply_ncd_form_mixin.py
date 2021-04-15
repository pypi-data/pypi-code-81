from typing import List, Type, Union

from django import forms
from django.forms import ModelForm
from edc_list_data.model_mixins import ListModelMixin

from ..stubs import DrugSupplyNcdFormMixinStub as FormMixinStub
from ..utils import validate_total_days


class DrugSupplyNcdFormMixin:

    list_model_cls: Type[ListModelMixin] = None

    def clean(self: Union[FormMixinStub, ModelForm]) -> dict:
        cleaned_data = super().clean()
        data = dict(self.data.lists())
        rx = self.list_model_cls.objects.filter(id__in=data.get("rx") or [])
        rx_names = [obj.display_name for obj in rx]
        inline_drug_names = self.raise_on_duplicates()

        validate_total_days(self)

        if (
            self.cleaned_data.get("drug")
            and self.cleaned_data.get("drug").display_name not in rx_names
        ):
            treatment = " + ".join(rx_names)
            raise forms.ValidationError(
                f"Invalid. `{self.cleaned_data.get('drug').display_name}` "
                f"not in current treatment of `{treatment}`"
            )

        self.raise_on_missing_drug(rx_names, inline_drug_names)

        return cleaned_data

    def raise_on_duplicates(self: forms.ModelForm) -> list:
        drug_names = []
        total_forms = self.data.get(f"{self.relation_label}_set-TOTAL_FORMS")
        for form_index in range(0, int(total_forms or 0)):
            inline_rx_id = self.data.get(f"{self.relation_label}_set-{form_index}-drug")
            if inline_rx_id:
                rx_obj = self.list_model_cls.objects.get(id=int(inline_rx_id))
                if rx_obj.display_name in drug_names:
                    raise forms.ValidationError("Invalid. Duplicates not allowed")
                drug_names.append(rx_obj.display_name)
        return drug_names

    @staticmethod
    def raise_on_missing_drug(rx_names: List[str], inline_drug_names: List[str]) -> None:
        for display_name in rx_names:
            if display_name not in inline_drug_names:
                raise forms.ValidationError(f"Missing drug. Also expected {display_name}.")
