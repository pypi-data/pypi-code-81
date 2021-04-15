from ehelply_python_sdk.services.service_schemas import *


class GetProjectResponse(HTTPResponse):
    uuid: str
    name: str
    created_at: str
    current_spend: int  # Dollar formats represented by a x10000000 integer. Precision to the millonth
    max_spend: int  # Dollar formats represented by a x10000000 integer. Precision to the millonth
    is_spend_maxed: bool
    status: Optional[str] = None


class UpdateProject(BaseModel):
    max_spend: int  # Dollar formats represented by a x10000000 integer. Precision to the millonth


class UpdateProjectResponse(HTTPResponse):
    uuid: str
    name: str
    created_at: str
    current_spend: int  # Dollar formats represented by a x10000000 integer. Precision to the millonth
    max_spend: int  # Dollar formats represented by a x10000000 integer. Precision to the millonth
    is_spend_maxed: bool
    group_m_p: str  # Group UUID that joins members to partition/project
    group_p_c: str  # Group UUID that joins partition/project to eHelply Cloud


class SearchProjectItem(BaseModel):
    uuid: str
    name: str
    created_at: str
    current_spend: int  # Dollar formats represented by a x10000000 integer. Precision to the millonth
    max_spend: int  # Dollar formats represented by a x10000000 integer. Precision to the millonth
    is_spend_maxed: bool


class UsageTypeUnitPrice(BaseModel):
    min_quantity: int  # Quantity formats represented by a x10000000 integer. Precision to the millonth
    max_quantity: int  # Quantity formats represented by a x10000000 integer. Precision to the millonth
    unit_price: int  # Dollar formats represented by a x10000000 integer. Precision to the millonth


class SearchUsageTypeItem(BaseModel):
    key: str
    name: str
    summary: str
    category: str
    service: str
    unit_prices: List[UsageTypeUnitPrice]


class UsageItem(BaseModel):
    uuid: str
    project_uuid: str
    usage_key: str
    year: int
    month: int
    quantity: int  # Quantity formats represented by a x10000000 integer. Precision to the millonth
    estimated_cost: int  # Dollar formats represented by a x10000000 integer. Precision to the millonth
    updated_at: str


class GetUsageResponse(HTTPResponse):
    usage: List[UsageItem]

    def __init__(self, *args, **data: Any) -> None:
        usage: List[UsageItem] = []

        for arg_usage in args:
            usage.append(UsageItem(**arg_usage))

        super().__init__(*args, **data, usage=usage)
