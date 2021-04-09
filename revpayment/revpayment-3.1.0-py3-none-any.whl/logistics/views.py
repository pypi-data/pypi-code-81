from rest_framework import response, views

from revpayment.logistics import LogisticsSDK
from revpayment.models import RedirectState
from revpayment.settings import api_settings

order_class = api_settings.ORDER_CLASS
verify_method = api_settings.VERIFY_METHOD
# Create your views here.


class LogisticCallBack(views.APIView):
    permission_classes = ()

    def post(self, request):
        data = request.data
        state = self.request.query_params.get("state")
        state = RedirectState.objects.get(state=state)
        order = order_class.objects.get(id=state.order_id)
        sdk = LogisticsSDK(order=order)
        sdk.callback(data)
        return response.Response("1", 200)


class SelectCVS(views.APIView):
    permission_classes = ()

    def get(self, request):
        token = request.query_params.get("token")
        logistic_provider = request.query_params.get("logistic_provider", "ecpay")
        logistic_subtype = request.query_params.get("logistic_subtype", "UNIMARTC2C")
        payment_type = request.query_params.get("payment_type", "ecpay")
        payment_subtype = request.query_params.get("payment_subtype", "default")
        collection = payment_subtype == "cvs_cod"
        profile = verify_method(token)
        state = RedirectState.objects.create(
            payment_type=payment_type, payment_subtype=payment_subtype, buyer=profile
        )
        sdk = LogisticsSDK(logistic_provider=logistic_provider)
        resp = sdk.cvs_map(logistic_subtype, state, collection)
        return resp


class CVSCallback(views.APIView):
    permission_classes = ()

    def post(self, request):
        state = RedirectState.objects.get(state=request.query_params.get("state"))
        sdk = LogisticsSDK()
        return sdk.cvs_callback(request.data.dict(), state.buyer)
