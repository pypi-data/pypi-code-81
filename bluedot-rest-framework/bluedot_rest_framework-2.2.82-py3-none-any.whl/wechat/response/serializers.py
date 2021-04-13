from rest_framework.serializers import CharField, SerializerMethodField
from bluedot_rest_framework.utils.serializers import CustomSerializer
from bluedot_rest_framework.analysis.monitor.models import AnalysisMonitor
from .models import WeChatResponseMaterial, WeChatResponseEvent, WeChatQrcode


class WeChatResponseMaterialSerializer(CustomSerializer):

    class Meta:
        model = WeChatResponseMaterial
        fields = '__all__'


class WeChatResponseEventSerializer(CustomSerializer):
    qrcode_data = SerializerMethodField()
    event_key = CharField(required=False)

    class Meta:
        model = WeChatResponseEvent
        fields = '__all__'

    def get_qrcode_data(self, queryset):
        open_list = []
        user_list = []
        event_key = queryset.event_key
        qrcode_queryset = AnalysisMonitor.objects.filter(
            wechat_event_msg=event_key)
        pv = qrcode_queryset.count()
        for item in qrcode_queryset:
            open_list.append(item.user_openid)
        uv = len(set(open_list))
        subscribe_queryset = qrcode_queryset.filter(
            wechat_event_key='subscribe_scan')
        for item in subscribe_queryset:
            user_list.append(item.user_openid)
        return {
            'pv': pv,
            'uv': uv,
            'subscribe_count': len(set(user_list))
        }


class WeChatQrcodeSerializer(CustomSerializer):

    class Meta:
        model = WeChatQrcode
        fields = '__all__'
