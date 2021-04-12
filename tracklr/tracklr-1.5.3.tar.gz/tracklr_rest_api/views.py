# -*- coding: utf-8 -*-
# vim: set expandtab tabstop=4 shiftwidth=4:
import re
import logging

from django.http import Http404

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView

from tracklr import Tracklr
from tracklr_rest_api.serializers import LsStringSerializer
from tracklr_rest_api.serializers import LsDecimalSerializer

logger = logging.getLogger(__name__)


class LsView(ListAPIView):
    """Return list of events for the given set of input parameters.
    """
    serializer_class = LsStringSerializer

    # def get(self, request, format=None):
    def get_queryset(self):

        # Select group
        selected_group = None
        group = self.request.query_params.get("group", "")
        if group == "hashtag":
            selected_group = "#"
        elif group == "at":
            selected_group = "@"
        elif group == "dollar":
            selected_group = "\$"
            self.serializer_class = LsDecimalSerializer
        elif group == "percentage":
            selected_group = "%"
            self.serializer_class = LsDecimalSerializer
        else:
            selected_group = None

        # Select calendar
        selected_calendar = None
        calendar = self.request.query_params.get("calendar", "")
        pattern = re.compile(r"^([0-9A-Za-z-_.]{1,32})$")
        matches = pattern.findall(calendar)
        if matches:
            selected_calendar = f"{matches[0]}"
        else:
            selected_calendar = None

        # Select date
        selected_date = None
        date = self.request.query_params.get("date", "")
        if date is not None:
            pattern = re.compile(r"^([0-9]{1,4})$")
            matches = pattern.findall(date)
            if matches:
                selected_date = f"{matches[0]}"
            else:
                pattern = re.compile(r"^([0-9]{1,4})-([0-9]{1,2})$")
                matches = pattern.findall(date)
                if matches:
                    selected_date = f"{matches[0][0]}-{matches[0][1]}"
                else:
                    pattern = re.compile(r"([0-9]{1,4})-([0-9]{1,2})-([0-9]{1,2})")
                    matches = pattern.findall(date)
                    if matches:
                        selected_date = f"{matches[0][0]}-{matches[0][1]}-{matches[0][2]}"

        # Select include
        selected_include = None
        include = self.request.query_params.get("include", "")
        pattern = re.compile(r"([0-9A-Za-z]{1,32})+")
        matches = pattern.findall(include)
        if matches:
            selected_include = matches
        else:
            selected_include = None

        # Select exclude
        selected_exclude = None
        exclude = self.request.query_params.get("exclude", "")
        pattern = re.compile(r"([0-9A-Za-z]{1,32})+")
        matches = pattern.findall(exclude)
        if matches:
            selected_exclude = matches
        else:
            selected_exclude = None

        t = Tracklr()

        logger.info(
            f"get report: "
            f"{selected_group} "
            f"{selected_calendar} "
            f"{selected_date} "
            f"{selected_include} "
            f"{selected_exclude}"
        )

        items = []

        try:
            report = t.get_report(
                selected_group,
                selected_calendar,
                selected_date,
                selected_include,
                selected_exclude,
            )
        except RuntimeError:
            return items

        for event in report:

            item = {
                "date": event[0],
                "summary": event[1],
                "description": event[2],
                "hours": event[3],
            }

            if selected_group is not None:
                group_data = []
                for g in event[4]:
                    group_data.append({"group": g})
                item["group"] = group_data
            items.append(item)

            #if selected_group in ["dollar", "percentage"]:
            #    items.append(LsStringSerializer(item).data)
            #    items.append(LsStringSerializer(item).data)

        return items
        # return Response(items)
