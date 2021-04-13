import random
import xlwt
import datetime
import json
from io import BytesIO
from django.http import HttpResponse
from rest_framework.decorators import action
from rest_framework import status
from django.conf import settings
from rest_framework.response import Response
from bluedot_rest_framework.utils.viewsets import CustomModelViewSet, AllView
from bluedot_rest_framework.wechat import App
from django_redis import get_redis_connection
from bluedot_rest_framework.analysis.monitor.models import AnalysisMonitor
from .models import WeChatResponseMaterial, WeChatResponseEvent
from ..models import WeChatUser, WeChatUserOpenid
from .serializers import WeChatResponseMaterialSerializer, WeChatResponseEventSerializer
from .. import OfficialAccount


class WeChatResponseMaterialView(CustomModelViewSet, AllView):
    model_class = WeChatResponseMaterial
    serializer_class = WeChatResponseMaterialSerializer

    filterset_fields = {
        "material_type": {"field_type": "int", "lookup_expr": ""},
        "title": {"field_type": "string", "lookup_expr": "__icontains"},
    }


class WeChatResponseEventView(CustomModelViewSet):
    model_class = WeChatResponseEvent
    serializer_class = WeChatResponseEventSerializer

    filterset_fields = {
        "event_type": {"field_type": "int", "lookup_expr": ""},
        "title": {"field_type": "string", "lookup_expr": "__icontains"},
    }

    def create(self, request, *args, **kwargs):
        if request.data["event_type"] == 2:
            event_key = str(random.uniform(1, 10))
            result = App(request.data["appid"]).qrcode.create(
                {
                    "action_name": "QR_LIMIT_STR_SCENE",
                    "action_info": {
                        "scene": {"scene_str": event_key},
                    },
                }
            )
            request.data["qrcode_ticket"] = result["ticket"]
            request.data["qrcode_url"] = result["url"]
            request.data["event_key"] = event_key
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    @action(detail=False, methods=["get"], url_path="data_down", url_name="data_down")
    def data_down(self, request, *args, **kwargs):
        start_date = request.query_params.get("startime", None)
        end_date = request.query_params.get("endtime", None)
        start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")
        end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d")
        tomorrow = end_date + datetime.timedelta(1)
        ws = xlwt.Workbook(encoding="UTF-8")
        w = ws.add_sheet(u"Sheet1")
        colums_indexs = ["码值", "pv", "uv", "新关注人数", "openid", "nick_name"]
        old_list = []
        num = 0
        for index_name in colums_indexs:
            w.write(0, num, index_name)
            num += 1
        excel_row = 1
        queryset = WeChatResponseEvent.objects.filter(
            event_type=2)
        for item in queryset:
            curse = True
            open_list = []
            user_list = []
            event_key = item.event_key

            title = item.title
            qrcode_queryset = AnalysisMonitor.objects.filter(
                wechat_event_msg=event_key,
                created__gte=start_date,
                created__lte=tomorrow,
            )
            pv = qrcode_queryset.count()
            for i in qrcode_queryset:
                open_list.append(i.user_openid)
            uv = len(set(open_list))
            subscribe_queryset = qrcode_queryset.filter(
                wechat_event_key="subscribe_scan"
            )
            for k in subscribe_queryset:
                user_list.append(k.user_openid)
            w.write(excel_row, 0, title)
            w.write(excel_row, 1, pv)
            w.write(excel_row, 2, uv)
            w.write(excel_row, 3, len(set(user_list)))
            for user in set(open_list):
                wechat_queryset = WeChatUserOpenid.objects.filter(
                    openid=user).first()
                if wechat_queryset:
                    curse = False
                    wechat_id = wechat_queryset.wechat_id
                    nick_name = (
                        WeChatUser.objects.filter(
                            pk=wechat_id).first().nick_name
                    )
                    w.write(excel_row, 4, user)
                    w.write(excel_row, 5, nick_name)
                    excel_row += 1
            for user in set(user_list):
                curse = False
                openid = user
                wechat_queryset = WeChatUserOpenid.objects.filter(
                    openid=openid).first()
                if wechat_queryset:
                    wechat_id = wechat_queryset.wechat_id
                    nick_name = (
                        WeChatUser.objects.filter(
                            pk=wechat_id).first().nick_name
                    )
                    w.write(excel_row, 4, openid)
                    w.write(excel_row, 5, nick_name)
                    excel_row += 1
            excel_row += 1
            if curse == False:
                excel_row -= 1
        sio = BytesIO()
        ws.save(sio)
        sio.seek(0)
        response = HttpResponse(
            sio.getvalue(), content_type="application/octet-stream")
        return response

    @action(
        detail=False,
        methods=["get"],
        url_path="get_user",
        url_name="get_user",
        permission_classes=[],
    )
    def get_user(self, request, *args, **kwargs):
        queryset = AnalysisMonitor.objects.filter(
            wechat_event_key="subscribe_scan")
        for item in queryset:
            open_queryset = WeChatUserOpenid.objects.filter(
                openid=item.user_openid).first
            if not open_queryset:
                user_data = OfficialAccount.user.get(item.user_openid)
                if "nickname" in user_data:
                    user_dict = {
                        "unionid": "",
                        "nick_name": user_data["nickname"],
                        "avatar_url": user_data["headimgurl"],
                        "gender": user_data["sex"],
                        "province": user_data["province"],
                        "city": user_data["city"],
                        "country": user_data["country"],
                        "language": user_data["language"],
                    }
                    user_queryset = WeChatUser.objects.create(**user_dict)
                    openid_data = {
                        "wechat_id": user_queryset.id,
                        "appid": settings.BLUEDOT_REST_FRAMEWORK["wechat"][
                            "offiaccount"
                        ]["APPID"],
                        "openid": item.user_openid,
                        "subscribe": user_data["subscribe"],
                    }
                    WeChatUserOpenid.objects.create(**openid_data)
        return Response("success")

    @action(
        detail=False,
        methods=["get"],
        url_path="delete_user",
        url_name="delete_user",
        permission_classes=[],
    )
    def delete_user(self, request, *args, **kwargs):
        open_list = []
        id_list = []
        wechat_list = []
        queryset = WeChatUserOpenid.objects.all()
        for item in queryset:
            if item.openid not in open_list:
                open_list.append(item.openid)
                id_list.append(item.id)
                wechat_list.append(item.wechat_id)
        WeChatUserOpenid.objects.exclude(id__in=id_list).delete()
        WeChatUser.objects.exclude(id__in=wechat_list).delete()
        return Response('success')
