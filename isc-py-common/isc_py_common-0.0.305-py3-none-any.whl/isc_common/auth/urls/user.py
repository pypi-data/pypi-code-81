from django.urls import path

from isc_common.auth.views import user
from isc_common.auth.views.user import User_Add, User_Lookup, User_Info, User_Remove, User_Update, User_UploadPhoto
from isc_common.auth.views.user_download_photo import user_download_photo

urlpatterns = [

    path('User/Fetch/', user.User_Fetch),
    path('User/Photo/', user.User_FetchPhoto),
    path('User/FetchExclBots/', user.User_FetchExclBots),
    path('User/Add', User_Add),
    path('User/Update', User_Update),
    path('User/Remove', User_Remove),
    path('User/Lookup/', User_Lookup),
    path('User/Info/', User_Info),
    path('User/UploadPhoto', User_UploadPhoto),
    path('User/DownloadPhoto/', user_download_photo),
]
