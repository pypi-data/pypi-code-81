# Copyright (C) 2019 Majormode.  All rights reserved.
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

from majormode.perseus.constant.sort_order import SortOrder
from majormode.perseus.constant.http import HttpMethod
from majormode.perseus.service.base_http_handler import HttpRequest
from majormode.perseus.service.base_http_handler import HttpRequestHandler
from majormode.perseus.service.base_http_handler import http_request
from majormode.perseus.service.notification.notification_service import NotificationService


class NotificationServiceHttpRequestHandler(HttpRequestHandler):
    @http_request(r'/notification',
                  http_method=HttpMethod.GET,
                  authentication_required=False)
    def get_notifications(self, request):
        recipient_id = request.get_argument(
            'recipient_id',
            data_type=HttpRequest.ArgumentDataType.string,
            is_required=False)

        end_time = request.get_argument(
            'end_time',
            data_type=HttpRequest.ArgumentDataType.timestamp,
            is_required=False)

        include_read = request.get_argument(
            'include_read',
            data_type=HttpRequest.ArgumentDataType.boolean,
            is_required=False,
            default_value=False)

        limit = request.get_argument(
            'limit',
            data_type=HttpRequest.ArgumentDataType.integer,
            is_required=False,
            default_value=NotificationService.DEFAULT_LIMIT)

        mark_read = request.get_argument(
            'mark_read',
            data_type=HttpRequest.ArgumentDataType.boolean,
            is_required=False,
            default_value=True)

        offset = request.get_argument(
            'offset',
            data_type=HttpRequest.ArgumentDataType.integer,
            is_required=False,
            default_value=0)

        sort_order = request.get_argument(
            'sort_order',
            data_type=HttpRequest.ArgumentDataType.enumeration,
            enumeration=SortOrder,
            is_required=False,
            default_value=SortOrder.ascending)

        start_time = request.get_argument(
            'start_time',
            data_type=HttpRequest.ArgumentDataType.timestamp,
            is_required=False)

        notification_types = request.get_argument(
            'types',
            data_type=HttpRequest.ArgumentDataType.list,
            item_data_type=HttpRequest.ArgumentDataType.string,
            is_required=False)

        return NotificationService().get_notifications(
            request.app_id, recipient_id or request.account_id,
            start_time=start_time, end_time=end_time,
            notification_types=notification_types,
            offset=offset, limit=limit,
            include_read=include_read,
            mark_read=mark_read,
            sort_order=sort_order)

    @http_request(r'/notification',
                  http_method=HttpMethod.PUT,
                  authentication_required=True)
    def mark_notifications(self, request):
        notification_ids = request.get_argument(
            'ids',
            data_type=HttpRequest.ArgumentDataType.list,
            item_data_type=HttpRequest.ArgumentDataType.uuid,
            is_required=True)

        mark_read = request.get_argument(
            'mark_read',
            data_type=HttpRequest.ArgumentDataType.boolean,
            is_required=False,
            default_value=True)

        return NotificationService().mark_notifications(
            request.app_id, request.account_id,
            notification_ids, mark_read)

    @http_request(r'^/notification/registration$',
                  http_method=HttpMethod.POST,
                  authentication_required=False,
                  signature_required=True)
    def register_device(self, request):
        device_id = request.get_argument(
            'device_id',
            data_type=HttpRequest.ArgumentDataType.string,
            is_required=True)

        device_platform = request.get_argument(
            'device_platform',
            data_type=HttpRequest.ArgumentDataType.enumeration,
            enumeration=NotificationService.DevicePlatform,
            is_required=True)

        device_token = request.get_argument(
            'device_token',
            data_type=HttpRequest.ArgumentDataType.hexadecimal,
            is_required=True)

        locale = request.get_argument(
            'locale',
            data_type=HttpRequest.ArgumentDataType.locale,
            is_required=False)

        topics = request.get_argument(
            'topics',
            data_type=HttpRequest.ArgumentDataType.list,
            item_data_type=HttpRequest.ArgumentDataType.string,
            is_required=False)

        utc_offset = request.get_argument(
            'utc_offset',
            data_type=HttpRequest.ArgumentDataType.integer,
            is_required=False)

        NotificationService().register_device(
            request.app_id,
            device_id,
            device_token,
            device_platform,
            account_id=request.session and request.session.account_id,
            locale=locale,
            topics=topics,
            utc_offset=utc_offset)

    @http_request(r'^/notification/registration$',
                  http_method=HttpMethod.DELETE,
                  authentication_required=False,
                  signature_required=True)
    def unregister_device(self, request):
        device_id = request.get_argument(
            'device_id',
            data_type=HttpRequest.ArgumentDataType.string,
            is_required=True)

        NotificationService().unregister_device(
            request.app_id, device_id,
            account_id=request.account_id)
