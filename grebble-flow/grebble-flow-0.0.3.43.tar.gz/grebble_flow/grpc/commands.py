import os
from pathlib import Path

import pkg_resources


def install_proto():
    import grpc_tools.protoc

    proto_include = pkg_resources.resource_filename("grebble_flow", "proto")
    for file in [
        "grebble_flow/grpc/generated/inner/v1/app.proto",
        "grebble_flow/grpc/generated/inner/v1/processor.proto",
    ]:
        grpc_tools.protoc.main(
            [
                "grpc_tools.protoc",
                f"-I {proto_include}",
                f"--proto_path={proto_include}",
                f"--python_out=./",
                f"--grpc_python_out=./",
                f"{file}",
            ]
        )
