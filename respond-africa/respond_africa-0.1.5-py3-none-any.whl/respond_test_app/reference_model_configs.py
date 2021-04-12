from edc_reference import site_reference_configs

site_reference_configs.register_from_visit_schedule(
    visit_models={"edc_appointment.appointment": "respond_test_app.subjectvisit"}
)

configs = {
    "respond_test_app.clinicalreviewbaseline": [
        "hiv_test",
        "dm_test",
        "htn_test",
        "chol_test",
        "hiv_dx",
        "dm_dx",
        "htn_dx",
        "chol_dx",
    ],
    "respond_test_app.clinicalreview": [
        "hiv_test",
        "dm_test",
        "htn_test",
        "chol_test",
        "hiv_dx",
        "dm_dx",
        "htn_dx",
        "chol_dx",
        "complications",
    ],
    "respond_test_app.medications": ["refill_hiv", "refill_dm", "refill_htn", "refill_chol"],
}

for reference_name, fields in configs.items():
    site_reference_configs.add_fields_to_config(name=reference_name, fields=fields)
