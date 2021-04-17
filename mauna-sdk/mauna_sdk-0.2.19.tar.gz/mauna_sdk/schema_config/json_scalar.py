from gql_client.compiler.renderer_dataclasses import CustomScalar
from typing import Dict

custom_scalars: Dict[str, CustomScalar] = {
    "JSON": CustomScalar(
        name="JSON",
        type=dict,
    ),
}