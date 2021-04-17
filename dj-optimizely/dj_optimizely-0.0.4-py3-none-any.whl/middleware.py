from optimizely import optimizely

from djoptimizely.client import OptimizelyClient
from djoptimizely.utils.datafile import update_datafile_for_current_env


def optimizely_middleware(get_response):
    # On server start fetch the current datafile as specified in settings
    update_datafile_for_current_env()

    def middleware(request):
        request.optimizely_client = OptimizelyClient()
        response = get_response(request)
        return response

    return middleware
