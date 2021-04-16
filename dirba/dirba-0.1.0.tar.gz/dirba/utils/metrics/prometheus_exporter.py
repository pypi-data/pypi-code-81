import fastapi
from aiomisc.service.asgi import ASGIHTTPService
from prometheus_client import make_asgi_app


class PrometheusExporter(ASGIHTTPService):
    """
    Сервис для экспорта метрик.

    Все метрики доступны на /metrics.


    Сам по себе данный сервис бесполезен, его задача - раздача метрик для их сохранения в prometheus.
    Сами метрики должны собираться посредством инструментария библиотеки **prometheus_client**
    """

    async def create_asgi_app(self):
        app = fastapi.FastAPI(openapi_url=None)
        app.mount('/metrics', make_asgi_app())

        return app
