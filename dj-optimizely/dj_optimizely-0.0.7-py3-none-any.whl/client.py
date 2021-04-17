from optimizely import optimizely

from djoptimizely.utils.datafile import get_datafile


class OptimizelyClient:
    """
    Wrapper that lazy loads optimizely sdk client
    
    """
    _client = None

    def get_client(self):
        if not self._client:
            datafile = get_datafile()
            if datafile:
                self._client = optimizely.Optimizely(
                    datafile=datafile
                )
        return self._client
