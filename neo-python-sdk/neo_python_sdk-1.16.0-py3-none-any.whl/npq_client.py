from nats.aio.client import Client as NATS
import json
import os
import ssl
import base64
import logging
from sentry_sdk import capture_exception


async def init(loop):
    self = NpqClient()
    disable_autoconnect = os.getenv("NPQ_DISABLE_AUTOCONNECT", False)
    if not disable_autoconnect:
        await self.connect(loop)
    return self


class NpqClient(NATS):
    def __init__(self):
        super().__init__()
        log_format = "%(asctime)-15s[NSX][%(levelname)s] %(message)s"

        logging.basicConfig(format=log_format, level=logging.DEBUG)
        self.logger = logging.getLogger("nsx")

        self.npq_host = os.getenv("NPQ_HOST", "127.0.0.1")
        self.npq_pass = os.getenv("NPQ_PASS", "local")
        self.npq_port = os.getenv("NPQ_PORT", "4222")
        self.npq_user = os.getenv("NPQ_USER", "neo")
        self.npq_name = os.getenv("NPQ_NAME", None)
        self.sentry_dsn = os.getenv("SENTRY_DSN")

    async def connect(self, loop):
        nats_url = f"nats://{self.npq_host}:{self.npq_port}"
        self.logger.info(f"Connecting to {nats_url}")

        ca_cert = os.getenv("NPQ_CA")
        client_cert = os.getenv("NPQ_CERT")
        client_key = os.getenv("NPQ_CERT_KEY")

        if ca_cert != None and client_cert != None and client_key != None:
            ca = open("ca.pem", "w")
            ca.write(base64.b64decode(ca_cert))
            key = open("key.pem", "w")
            key.write(base64.b64decode(client_key))
            cert = open("client.pem", "w")
            cert.write(base64.b64decode(client_cert))

            ssl_ctx = ssl.ssl.create_default_context(purpose=ssl.Purpose.SERVER_AUTH)
            ssl_ctx.load_verify_locations("ca.pem")
            ssl_ctx.load_cert_chain(certfile="client.pem", keyfile="key.pem")

            await super().connect(
                nats_url,
                user=self.npq_user,
                name=self.npq_name,
                password=self.npq_pass,
                io_loop=loop,
                tls=ssl_ctx,
            )
        else:
            await super().connect(
                nats_url,
                user=self.npq_user,
                name=self.npq_name,
                password=self.npq_pass,
                io_loop=loop,
            )
        self.logger.info(f"Connected to {nats_url}")

    async def process(self, queue, processor):
        async def process_handler(msg):
            subject = msg.subject
            reply = msg.reply
            payload = json.loads(msg.data.decode())
            self.logger.info(f"Received a message on '{subject}'")
            try:
                result = await processor(payload)
            except Exception as e:
                capture_exception(e)
            await self.publish(reply, json.dumps(result).encode())

        await super().subscribe(queue, cb=process_handler)
        self.logger.info(f"Subscribed to {queue}")

    async def create(self, queue, particle={}, options={"timeout": 15000}):
        try:
            result = await super().request(
                queue, json.dumps(particle).encode(), timeout=options["timeout"]
            )
        except Exception as e:
            capture_exception(e)
        return json.loads(result.data.decode())

    async def capture_exception(self, e):
        capture_exception(e)
