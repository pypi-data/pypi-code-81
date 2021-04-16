from pydantic import BaseModel, ValidationError, validator, AnyHttpUrl
from decimal import Decimal
from typing import List, Optional, Any, Union
from enum import Enum
from datetime import datetime


class MultiCardNamesEnum(str, Enum):
    BRAC_VISA = "brac_visa"
    DBBL_VISA = "dbbl_visa"
    CITY_VISA = "city_visa"
    EBL_VISA = "ebl_visa"
    SBL_VISA = "sbl_visa"
    BRAC_MASTER = "brac_master"
    DBBL_MASTER = "dbbl_master"
    CITY_MASTER = "city_master"
    EBL_MASTER = "ebl_master"
    SBL_MASTER = "sbl_master"
    CITY_AMEX = "city_amex"
    QCASH = "qcash"
    DBBL_NEXUS = "dbbl_nexus"
    BANK_ASIA = "bankasia"
    ABBANK = "abbank"
    IBBL = "ibbl"
    MTBL = "mtbl"
    BKASH = ("bkash",)
    DBBL_MOBILE_BANKING = "dbblmobilebanking"
    CITY = "city"
    UPAY = "upay"
    TAPNPAY = "tapnpay"
    INTERNET_BANK = "internetbank"
    MOBILE_BANK = "mobilebank"
    OTHER_CARD = "othercard"
    VISA_CARD = "visacard"
    MASTER_CARD = "mastercard"
    AMEX_CARD = "amexcard"


class EMIOptionsEnum(int, Enum):
    THREE_MONTHS = 3
    SIX_MONTHS = 6
    NINE_MONTHS = 9


class ShippingMethodEnum(str, Enum):
    YES = "YES"
    NO = "NO"
    COURIER = "COURIER"


class BooleanIntEnum(int, Enum):
    TRUE = 1
    FALSE = 0


class ProductProfileEnum(str, Enum):
    GENERAL = "general"
    PHYSICAL_GOODS = "physical-goods"
    NON_PHYSICAL_GOODS = "non-physical-goods"
    AIRLINE_TICKETS = "airline-tickets"
    TRAVEL_VERTICAL = "travel-vertical"
    TELECOM_VERTICAL = "telecom-vertical"


class CartItem(BaseModel):
    product: str
    quantity: int
    amount: Decimal

    @validator("product")
    def not_more_than_255(cls, v, field):
        if len(v) > 255:
            raise ValueError(f"{field} can't be more than 255 characters")
        return v

    @validator("amount")
    def valid_decimal(cls, v, field):
        val = str(float(v)).split(".")
        if len(val[0]) > 12 or len(val[1]) > 2:
            raise ValueError(f"{field} must have a decimal maximum of (12,2).")
        return v


class PaymentInitPostData(BaseModel):

    # Basic Fields
    total_amount: Decimal
    currency: str
    tran_id: str
    product_category: str
    success_url: AnyHttpUrl
    fail_url: AnyHttpUrl
    cancel_url: AnyHttpUrl

    # EMI Fields
    emi_option: BooleanIntEnum = BooleanIntEnum.FALSE

    # Customer Information
    cus_name: str
    cus_email: str
    cus_add1: str
    cus_city: str
    cus_country: str
    cus_phone: str

    # Shipping Method
    shipping_method: ShippingMethodEnum = ShippingMethodEnum.YES
    num_of_item: int

    # Product Information
    product_name: str
    product_category: str
    product_profile: ProductProfileEnum

    # Basic Fields Optional
    ipn_url: Optional[str]
    multi_card_name: Optional[MultiCardNamesEnum]
    allowed_bin: Optional[str]

    # EMI Optional
    emi_max_inst_option: Optional[EMIOptionsEnum]
    emi_selected_inst: Optional[EMIOptionsEnum]
    emi_allow_only: Optional[int]

    # Customer Optional
    cus_add2: Optional[str]
    cus_postcode: Optional[str]
    cus_state: Optional[str]
    cus_fax: Optional[str]

    # Shipping Method Optional
    ship_name: Optional[str]
    ship_add1: Optional[str]
    ship_add2: Optional[str]
    ship_city: Optional[str]
    ship_postcode: Optional[str]
    ship_country: Optional[str]
    ship_phone: Optional[str]
    ship_state: Optional[str]

    # Product Information Optional
    hours_till_departure: Optional[str]
    flight_type: Optional[str]
    pnr: Optional[str]
    journey_from_to: Optional[str]
    third_party_booking: Optional[str]
    hotel_name: Optional[str]
    length_of_stay: Optional[str]
    check_in_time: Optional[str]
    hotel_city: Optional[str]
    product_type: Optional[str]
    topup_number: Optional[str]
    country_topup: Optional[str]
    cart: Optional[List[CartItem]]
    product_amount: Optional[Decimal]
    vat: Optional[Decimal]
    discount_amount: Optional[Decimal]
    convenience_fee: Optional[Decimal]

    # Additional Optional
    value_a: Optional[str]
    value_b: Optional[str]
    value_c: Optional[str]
    value_d: Optional[str]

    class Config:
        arbitrary_types_allowed = True

    @validator(
        "currency",
    )
    def not_more_than_three(cls, v, field):
        if len(v) > 3:
            raise ValueError(f"{field} can't be more than 3 characters")
        return v

    @validator(
        "tran_id",
        "cus_postcode",
        "hours_till_departure",
        "length_of_stay",
        "check_in_time",
        "product_type",
        "country_topup",
    )
    def not_more_than_thirty(cls, v, field):
        if len(v) > 30:
            raise ValueError(f"{field} can't be more than 30 characters")
        return v

    @validator(
        "product_category",
        "cus_name",
        "cus_email",
        "cus_add1",
        "cus_add2",
        "cus_city",
        "cus_state",
        "cus_country",
        "ship_name",
        "ship_add1",
        "ship_add2",
        "ship_city",
        "ship_state",
        "ship_country",
        "ship_postcode",
        "pnr",
        "hotel_city",
    )
    def not_more_than_fifty(cls, v, field):
        if len(v) > 50:
            raise ValueError(f"{field} can't be more than 50 characters")
        return v

    @validator("product_profile", "product_category")
    def not_more_than_fifty(cls, v, field):
        if len(v) > 100:
            raise ValueError(f"{field} can't be more than 100 characters")
        return v

    @validator("topup_number")
    def not_more_than_hundred_fifty(cls, v, field):
        if len(v) > 150:
            raise ValueError(f"{field} can't be more than 150 characters")
        return v

    @validator(
        "success_url",
        "fail_url",
        "cancel_url",
        "ipn_url",
        "allowed_bin",
        "product_name",
        "journey_from_to",
        "hotel_name",
        "value_a",
        "value_b",
        "value_c",
        "value_d",
    )
    def not_more_than_255(cls, v, field):
        if len(v) > 255:
            raise ValueError(f"{field} can't be more than 255 characters")
        return v

    @validator(
        "total_amount",
        "product_amount",
        "vat",
        "discount_amount",
        "convenience_fee",
    )
    def valid_decimal(cls, v, field):
        val = str(float(v)).split(".")
        if len(val[0]) > 10 or len(val[1]) > 2:
            raise ValueError(f"{field} must have a decimal maximum of (10,2).")
        return v

    @validator("emi_allow_only", always=True)
    def valid_emi_allow_only(cls, v, values, field):
        emi = False
        if "emi_option" in values and values["emi_option"] == BooleanIntEnum.TRUE:
            emi = True
        if not emi and v == 1:
            raise ValidationError("emi_option should be enabled to use this field")
        return v

    @validator("num_of_item")
    def validate_num_of_item(cls, v):
        if v > 99 or v < 0:
            raise ValueError(
                "num_of_item should be of maximum two digits and a positive integer."
            )
        return v

    @validator(
        "ship_name",
        "ship_add1",
        "ship_city",
        "ship_postcode",
        "ship_country",
        always=True,
    )
    def validate_based_on_shipping_method(cls, v, field, values):
        shipping = values["shipping_method"] == ShippingMethodEnum.YES
        if shipping and not v:
            raise ValueError(
                f"{field} should be provided if shipping_method set to 'YES'"
            )
        if not shipping and v:
            raise ValueError(
                f"{field} should be omitted if shipping_method not set to 'YES'"
            )
        return v

    @validator(
        "hours_till_departure",
        "flight_type",
        "pnr",
        "journey_from_to",
        "third_party_booking",
    )
    def mandatory_if_airline_tickets(cls, v, field, values):
        if values["product_profile"] == ProductProfileEnum.AIRLINE_TICKETS and not v:
            raise ValueError(
                f"{field} is required if product_profile is {ProductProfileEnum.AIRLINE_TICKETS}"
            )
        if values["product_profile"] != ProductProfileEnum.AIRLINE_TICKETS and v:
            raise ValueError(
                f"{field} should be omitted if product_profile is {ProductProfileEnum.AIRLINE_TICKETS}"
            )
        return v

    @validator(
        "hotel_name",
        "length_of_stay",
        "check_in_time",
        "hotel_city",
    )
    def mandatory_if_travel_vertical(cls, v, field, values):
        if values["product_profile"] == ProductProfileEnum.TRAVEL_VERTICAL and not v:
            raise ValueError(
                f"{field} is required if product_profile is {ProductProfileEnum.TRAVEL_VERTICAL}"
            )
        if values["product_profile"] != ProductProfileEnum.TRAVEL_VERTICAL and v:
            raise ValueError(
                f"{field} should be omitted if product_profile is {ProductProfileEnum.TRAVEL_VERTICAL}"
            )
        return v

    @validator(
        "product_type",
        "topup_number",
        "country_topup",
    )
    def mandatory_if_telecom_vertical(cls, v, field, values):
        if values["product_profile"] == ProductProfileEnum.TELECOM_VERTICAL and not v:
            raise ValueError(
                f"{field} is required if product_profile is {ProductProfileEnum.TELECOM_VERTICAL}"
            )
        if values["product_profile"] != ProductProfileEnum.TRAVEL_VERTICAL and v:
            raise ValueError(
                f"{field} should be omitted if product_profile is {ProductProfileEnum.TELECOM_VERTICAL}"
            )
        return v

    @validator("cart")
    def check_cart_items(cls, v):
        for item in v:
            v.validate()
        return v


class ResponseStatusEnum(str, Enum):
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"


class Gateway(BaseModel):
    name: str
    type: str
    logo: Optional[str]
    gw: Optional[str]
    r_flag: Optional[str]
    redirectGatewayURL: Optional[str]


class PaymentInitResponse(BaseModel):
    status: ResponseStatusEnum
    failedreason: Optional[str]
    sessionkey: Optional[str]
    gw: Optional[Any]
    redirectGatewayURL: Optional[str]
    directPaymentURLBank: Optional[str]
    directPaymentURLCard: Optional[str]
    directPaymentURL: Optional[str]
    redirectGatewayURLFailed: Optional[str]
    GatewayPageURL: Optional[str]
    storeBanner: Optional[str]
    storeLogo: Optional[str]
    desc: Optional[List[Gateway]]

    class Config:
        arbitrary_types_allowed = True

    @validator("failedreason", "GatewayPageURL", "storeBanner", "storeLogo")
    def not_more_than_255(cls, v, field):
        if len(v) > 255:
            raise ValueError(f"{field} can't be more than 255 characters")
        return v

    @validator("sessionkey")
    def not_more_than_50(cls, v, field):
        if len(v) > 50:
            raise ValueError(f"{field} can't be more than 50 characters")
        return v

    @validator("failedreason", always=True)
    def validate_failed_reason(cls, v, field, values):
        print(values)
        if values["status"] == ResponseStatusEnum.FAILED and not v:
            raise ValidationError("failedreason must be provided if the request fails.")
        return v

    @validator("sessionkey", "gw", "GatewayPageURL", "desc")
    def validate_based_on_success(cls, v, field, values):
        if values["status"] == ResponseStatusEnum.SUCCESS and not v:
            raise ValidationError(f"{field} must be provided if the request succeeds.")
        return v


class IPNOrderStatusEnum(str, Enum):
    VALID = "VALID"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"
    UNATTEMPTED = "UNATTEMPTED"
    EXPIRED = "EXPIRED"


class OrderStatusEnum(str, Enum):
    VALID = "VALID"
    VALIDATED = "VALIDATED"
    INVALID_TRANSACTION = "INVALID_TRANSACTION"


class CardBrandEnum(str, Enum):
    VISA = "VISA"
    MASTER = "MASTER"
    AMEX = "AMEX"
    IB = "IB"
    MOBILE_BANKING = "MOBILE BANKING"


class RiskLevelEnum(int, Enum):
    HIGH = 1
    LOW = 0


class BaseOrderResponse(BaseModel):

    tran_date: datetime
    tran_id: str
    val_id: str
    amount: Decimal
    store_amount: Decimal
    card_type: str
    card_no: str
    currency: str
    bank_tran_id: str
    card_issuer: str
    card_brand: CardBrandEnum
    card_issuer_country: str
    card_issuer_country_code: str
    currency_type: str
    currency_amount: Decimal
    risk_level: RiskLevelEnum
    risk_title: str

    value_a: Optional[str]
    value_b: Optional[str]
    value_c: Optional[str]
    value_d: Optional[str]

    @validator(
        "card_issuer_country_code",
    )
    def not_more_than_two(cls, v, field):
        if len(v) > 2:
            raise ValueError(f"{field} can't be more than 2 characters")
        return v

    @validator(
        "currency_type",
    )
    def not_more_than_three(cls, v, field):
        if len(v) > 3:
            raise ValueError(f"{field} can't be more than 3 characters")
        return v

    @validator("tran_id", "card_brand")
    def not_more_than_thirty(cls, v, field):
        if len(v) > 30:
            raise ValueError(f"{field} can't be more than 30 characters")
        return v

    @validator(
        "val_id", "card_type", "card_issuer", "card_issuer_country", "risk_title"
    )
    def not_more_than_fifty(cls, v, field):
        if len(v) > 50:
            raise ValueError(f"{field} can't be more than 50 characters")
        return v

    @validator("card_no", "bank_tran_id")
    def not_more_than_eighty(cls, v, field):
        if len(v) > 80:
            raise ValueError(f"{field} can't be more than 80 characters")
        return v

    @validator(
        "value_a",
        "value_b",
        "value_c",
        "value_d",
    )
    def not_more_than_255(cls, v, field):
        if len(v) > 255:
            raise ValueError(f"{field} can't be more than 255 characters")
        return v

    @validator(
        "amount",
        "store_amount",
        "currency_amount",
    )
    def valid_decimal(cls, v, field):
        val = str(float(v)).split(".")
        if len(val[0]) > 10 or len(val[1]) > 2:
            raise ValueError(f"{field} must have a decimal maximum of (10,2).")
        return v


class IPNResponse(BaseOrderResponse):
    status: IPNOrderStatusEnum
    verify_sign: str
    verify_key: str

    @validator("verify_sign")
    def not_more_than_255_2(cls, v, field):
        if len(v) > 255:
            raise ValueError(f"{field} can't be more than 255 characters")
        return v


class OrderValidationPostData(BaseModel):
    val_id: str
    format: Optional[str]
    v: Optional[int]

    @validator("val_id")
    def not_more_than_fifty(cls, v, field):
        if len(v) > 50:
            raise ValueError(f"{field} can't be more than 50 characters")
        return v

    @validator("format")
    def not_more_than_10(cls, v, field):
        if len(v) > 10:
            raise ValueError(f"{field} can't be more than 10 characters")
        return v

    @validator("v")
    def validate_v(cls, v):
        if v < 0 or v > 9:
            raise ValueError("v must be an one digit positive integer")


class OrderValidationResponse(BaseOrderResponse):
    status: OrderStatusEnum
    emi_instalment: EMIOptionsEnum
    emi_amount: Decimal
    discount_amount: Decimal
    discount_percentage: Decimal
    discount_remarks: str

    @validator(
        "emi_amount",
        "discount_amount",
        "discount_percentage",
    )
    def valid_decimal_2(cls, v, field):
        val = str(float(v)).split(".")
        if len(val[0]) > 10 or len(val[1]) > 2:
            raise ValueError(f"{field} must have a decimal maximum of (10,2).")
        return v

    @validator("discount_remarks")
    def not_more_than_255_2(cls, v, field):
        if len(v) > 255:
            raise ValueError(f"{field} can't be more than 255 characters")
        return v


class Credential(BaseModel):
    store_id: str
    store_passwd: str
    sandbox: bool = False


class APIResponse(BaseModel):
    raw_data: Any
    status_code: int
    response: Optional[Union[OrderValidationResponse, IPNResponse, PaymentInitResponse]]

    class Config:
        arbitrary_types_allowed = True
