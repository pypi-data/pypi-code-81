from edc_visit_schedule import FormsCollection, Requisition
from respond_labs.panels import (
    blood_glucose_panel,
    blood_glucose_poc_panel,
    hba1c_panel,
    hba1c_poc_panel,
)

from mocca_labs import chemistry_lipids_panel

requisitions_prn = FormsCollection(
    Requisition(show_order=10, panel=chemistry_lipids_panel, required=True, additional=False),
    Requisition(show_order=20, panel=blood_glucose_panel, required=True, additional=False),
    Requisition(show_order=30, panel=blood_glucose_poc_panel, required=True, additional=False),
    Requisition(show_order=40, panel=hba1c_poc_panel, required=True, additional=False),
    Requisition(show_order=50, panel=hba1c_panel, required=True, additional=False),
    name="requisitions_prn",
)

requisitions_d1 = FormsCollection(
    Requisition(show_order=10, panel=chemistry_lipids_panel, required=True, additional=False),
    name="requisitions_day1",
)
requisitions_all = FormsCollection(
    Requisition(show_order=10, panel=chemistry_lipids_panel, required=False, additional=False),
    Requisition(
        show_order=30, panel=blood_glucose_poc_panel, required=False, additional=False
    ),
    name="requisitions_all",
)
