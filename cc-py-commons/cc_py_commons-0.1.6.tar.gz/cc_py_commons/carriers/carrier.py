import datetime
import uuid
from dataclasses import dataclass, field
from typing import Optional

from cc_py_commons.carriers.contact import Contact
@dataclass
class Carrier:
  mc: str
  dot: str  
  qualified: bool
  active: bool
  city: str
  state: str
  postcode: str = field(default=None)
  country: str = field(default=None)
  latitude: float = field(default=None)
  longitude: float = field(default=None)
  id: uuid.UUID = field(default=None)
  customer_code: str = field(default=None)
  business_name: str = field(default=None)
  doing_business_as: str = field(default=None)
  address1: str = field(default=None)
  drivers: int = field(default=None)
  active_checked_on: datetime.date = field(default_factory=lambda: datetime.date.today())
  power_units: int = field(default=None)
  drivers: int = field(default=None)
  credit_score: int = field(default=None)
  days_to_pay: int = field(default=None)
  needs_review: bool = field(init=False, repr=False, default=False)
  is_private: bool = field(init=False, repr=False, default=False)
  dispatch_service: bool = field(default=False)
  default_trailer_type: str = field(default=None)
  carrier_last_fmcsa_update: datetime.datetime = field(init=False, repr=False, default=None)
  hazmat: bool = field(default=False)
  hm_flag: bool = field(default=False)
  hazmat_expiration_date: datetime.datetime = field(default=None)
  mcs_150_date: datetime.date = field(default=None)
  mcs_150_mileage: int = field(default=None)
  mcs_150_mileage_year: int = field(default=None)
  fmcsa_date_added: datetime.datetime = field(init=False, repr=False, default=None)
  fmcsa_oic_state: str = field(default=None)
  fmcsa_safety_registration_date: datetime.datetime = field(default=None)
  fmcsa_authority_registration_date: datetime.datetime = field(default=None)
  in_network: bool = field(init=False, repr=False)
  last_reviewed: datetime.date = field(default=None)
  has_teams: bool = field(default=False)
  cargo_insurance_amount: float = field(default=None)
  cargo_insurance_renewal_date: datetime.datetime = field(default=None)
  liability_expiration_date: datetime.datetime = field(default=None)
  workmans_comp_date: datetime.datetime = field(default=None)
  safety_rating_date: datetime.datetime = field(default=None)
  safety_review_date: datetime.datetime = field(default=None)
  customer_count: int = field(default=0)
  contact_count: int = field(default=0)
  not_reached_count: int = field(default=0)
  not_reached_count_first_updated_at: datetime.datetime = field(default=None)
  lane_count: int = field(default=0)
  internal_remarks: str = field(default=None)
  contact: Contact = field(default=Contact())
