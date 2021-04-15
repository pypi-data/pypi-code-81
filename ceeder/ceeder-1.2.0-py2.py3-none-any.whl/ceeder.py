import sys
import os
import logging
import json

import falcon

from abc import ABC, abstractmethod


def version_from_env():
    vers = os.getenv("APP_VERSION")
    return vers if vers else "latest"


class HealthResource:
    """HealthResource supplies a simple Falcon health-check class."""

    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200  # This is the default status
        resp.media = {"status": "ok"}


class Annotator(ABC):
    """Annotator is a falcon-based "analytic".

    Implementations must implement one method:

    on_post(request, response)
    """

    @abstractmethod
    def on_post(self, req, resp):
        pass

    def create(
        self,
        health_endpoint="/api/v1/health",
        health_impl=HealthResource(),
        post_endpoint="/api/v1/annotate/cdr",
    ):
        """Create returns a falcon API object, which can be used immediately to
        provide Falcon-based functionality."""

        app = falcon.API()
        app.add_route(health_endpoint, health_impl)
        app.add_route(post_endpoint, self)
        return app


class TagAnnotator(Annotator):
    """TagAnnotator takes in a function that produces CDR annotation tags.

    It uses this function in the on_post method in order to more easily
    create a tag analytic by handling the web/framework parts. As a result,
    in order to implement a new tag analytic, one just needs to pass in
    an annotate_function that produces the right CDR tag output.
    """

    def __init__(
        self,
        annotate_function,
        label,
        annotator_type="tags",
        version=version_from_env(),
    ):
        self.annotate_function = annotate_function
        self.label = label
        self.annotator_type = annotator_type
        self.version = version

    def on_post(self, req, resp):
        request_json = req.media
        txt = request_json["extracted_text"]
        logging.debug("incoming text: {}".format(txt))
        output = {}
        content, code = self.annotate_function(txt)
        output["content"] = content
        output["type"] = self.annotator_type
        output["label"] = self.label
        output["version"] = self.version

        resp.media = output
        if code:
            resp.status = code


class FacetAnnotator(Annotator):
    """FacetAnnotator takes in a function that produces CDR annotation
    in the faceted format.

    It uses this function in the on_post method in order to more easily
    create a tag analytic by handling the web/framework parts. As a result,
    in order to implement a new tag analytic, one just needs to pass in
    an annotate_function that produces the right CDR tag output.
    """

    def __init__(
        self,
        annotate_function,
        label,
        annotator_type="facets",
        annotator_class="derived",
        version=version_from_env(),
    ):
        self.annotate_function = annotate_function
        self.label = label
        self.annotator_type = annotator_type
        self.annotator_class = annotator_class
        self.version = version

    def on_post(self, req, resp):
        request_json = req.media
        output = {}
        content, code = self.annotate_function(request_json)
        output["content"] = content
        output["type"] = self.annotator_type
        output["class"] = self.annotator_class
        output["label"] = self.label
        output["version"] = self.version

        resp.media = output
        if code:
            resp.status = code
