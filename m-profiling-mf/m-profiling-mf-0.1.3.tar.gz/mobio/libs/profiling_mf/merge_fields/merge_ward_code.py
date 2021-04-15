from mobio.libs.profiling_mf.common_helper import CommonHelper
from mobio.libs.profiling_mf.merge_fields.base_merge import BaseMerge, MergeListGroup


class MergeWardCode(BaseMerge):
    def serialize_data(
        self,
        suggest_data,
        profile_data,
        set_suggest_fields,
        set_unique_suggest_values,
        field_key,
        field_property,
        display_type,
        translate_key,
        predict=None,
    ):
        suggest = False
        if profile_data is not None and field_key not in set_suggest_fields:
            suggest = True
            set_suggest_fields.add(field_key)

        field_value = self.__build_value__(
            value=profile_data.get("id") if profile_data is not None else None,
            suggest=suggest,
            predict=predict,
        )
        suggest_data[field_key] = self.build_merge_data(
            translate_key=translate_key,
            field_property=field_property,
            display_type=display_type,
            displayable=True,
            editable=True,
            mergeable=True,
            order=1,
            group=MergeListGroup.DEMOGRAPHIC,
            value=field_value,
        )

    def set_filter_value(self, suggest_filter_data, profile_data):
        pass

    def serialize_origin_data(
        self,
        suggest_data,
        origin_data,
        set_suggest_fields,
        set_unique_suggest_values,
        field_key,
        field_property,
        display_type,
        translate_key,
    ):
        suggest = True if field_key not in set_suggest_fields and origin_data else False
        field_value = self.__build_value__(value=origin_data, suggest=suggest)
        if suggest:
            set_suggest_fields.add(field_key)
        suggest_data[field_key] = self.build_merge_data(
            translate_key=translate_key,
            field_property=field_property,
            display_type=display_type,
            displayable=True,
            editable=True,
            mergeable=True,
            order=1,
            group=MergeListGroup.DEMOGRAPHIC,
            value=field_value,
        )

    def merge_data(self, target_data, source_data, field_key, is_master_data=False):
        if source_data:
            suggest = source_data.get("field_value").get("suggest")
            value = source_data.get("field_value").get("value")
            if suggest and value is not None:
                try:
                    ward_code = int(value)
                except Exception as ex:
                    print(
                        "merge_data: df_get_ward_data_by_id ERROR: {}".format(ex)
                    )
                    ward_code = -1
                # ward_data = next((x.value for x in WardEnum if x.value.code == ward_code), None)
                # if ward_data:
                #     target_data[
                #         field_key
                #     ] = CommonHelper.create_simple_data_type(
                #             _id=ward_data.code, _name=ward_data.name
                #         )


if __name__ == "__main__":
    ward_code_test = {
        "display_type": "single_line",
        "displayable": True,
        "editable": True,
        "field_property": 14,
        "field_value": {
            "changeable": True,
            "suggest": False,
            "value": {"id": "1", "value": "hanoi"},
        },
        "group": "demographic",
        "mergeable": True,
        "order": 1,
        "tooltip_i18n": None,
        "translate_key": "i18n_label_wards",
    }
    result = MergeWardCode().validate_merge(data=ward_code_test)
    print(result)
