
from django.conf import settings


if not hasattr(settings, 'KMS'):
    raise NameError("not found KMS config")

kms = settings.KMS

for key in ['access_id', 'access_secret', 'region_id', 'edk']:
    if key not in kms.keys():
        raise KeyError("not found %s in KMS config" % key)


KMS_EDK, KMS_ACCESS_KEY_ID, KMS_ACCESS_KEY_SECRET, KMS_REGION_ID = kms['edk'], kms['access_id'], kms['access_secret'], kms['region_id']





