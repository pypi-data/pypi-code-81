from django.http import Http404

from djoptimizely.services import get_feature_enabled


class OptimizelyFeatureViewMixin:
    """
    A view mixin that checks for variation acces for the current user 
    Returns a 404 is the user does not have access to the variation

    """
    feature_key = None

    def dispatch(self, request, *args, **kwargs):
        if not get_feature_enabled(request, self.feature_key):
            raise Http404
        return super().dispatch(request, *args, **kwargs)
