from edc_lab import RequisitionPanel
from respond_labs.processing_profiles import chemistry_processing

chemistry_lipids_panel = RequisitionPanel(
    name="chemistry",
    verbose_name="Chemistry: Lipids Profile",
    abbreviation="CHEM",
    processing_profile=chemistry_processing,
)
