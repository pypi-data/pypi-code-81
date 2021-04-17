
import json

from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from djoptimizely.utils.datafile import update_datafile_with_payload
from djoptimizely.utils.webhook import verify_signature


@csrf_exempt
def datafile_webhook(request):
    if not verify_signature(request):
        raise PermissionDenied
    json_data = json.loads(request.body)
    if json_data:
        update_datafile_with_payload(payload=json_data)
    return HttpResponse(json.dumps(json_data), content_type='application/json')
