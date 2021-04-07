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
        event_key = queryset.event_key
        qrcode_queryset = AnalysisMonitor.objects.filter(
            wechat_event_msg=event_key)
        pv = qrcode_queryset.count()
        for item in qrcode_queryset:
            open_list.append(item.user_openid)
        uv = len(set(open_list))
        subscribe_count = qrcode_queryset.filter(
            wechat_event_key='subscribe_scan').count()
        return {
            'pv': pv,
            'uv': uv,
            'subscribe_count': subscribe_count
        }


class WeChatQrcodeSerializer(CustomSerializer):

    class Meta:
        model = WeChatQrcode
        fields = '__all__'
