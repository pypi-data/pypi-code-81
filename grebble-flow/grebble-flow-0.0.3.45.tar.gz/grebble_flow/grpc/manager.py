import logging
from concurrent import futures

import grpc
from grebble_flow.grpc.generated.inner.v1 import processor_pb2_grpc, app_pb2_grpc
from grebble_flow.grpc.service.app import AppService
from grebble_flow.grpc.service.processor import ProcessorService


def start_server(port):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    processor_pb2_grpc.add_ProcessorServicer_to_server(ProcessorService(), server)
    app_pb2_grpc.add_ExternalAppServicer_to_server(AppService(), server)
    server.add_insecure_port(f"[::]:{port}")
    server.start()
    logging.info("Server started")
    server.wait_for_termination()
