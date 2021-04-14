from datetime import timedelta
from django.utils import timezone
from django.conf import settings
from django.db import connection,models
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework import viewsets
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter,OrderingFilter
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from .permissions import DjangoModelPermissions
from .authentication import ExpiringTokenAuthentication
from rest_framework.views import APIView
from .serializer import User,User_Serializer
import json
from django_restful_response import Restful_Response
from .models import OperationLog
# from asset.views_ud import Restful_Response





# Create your views here.
class ExpiringObtainAuthToken(ObtainAuthToken):
    """
    登录获取token
    """
    def post(self, request, *args, **kwargs):  
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            login_succeed=True
        except:
            login_succeed=False
        if login_succeed:
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            #如果超过设置的3天的，那么更新token并重新获取token
            if timezone.now() > (token.created + timedelta(seconds=settings.SESSION_COOKIE_AGE)):
                Token.objects.filter(user=user).update(key=Token.generate_key(), created=timezone.now())
                token=Token.objects.get(user=user)
            return Response({'token':token.key},status=status.HTTP_200_OK) 
        else:
            # 如果错误返回401
            return Response({'token':""},status=status.HTTP_401_UNAUTHORIZED) 

obtain_auth_token = ExpiringObtainAuthToken.as_view()


class User_Set(viewsets.ModelViewSet):
    authentication_classes = [ExpiringTokenAuthentication, SessionAuthentication,BasicAuthentication]
    permission_classes = [DjangoModelPermissions]
    filter_backends = (SearchFilter, DjangoFilterBackend)
    queryset = User.objects.all()
    serializer_class = User_Serializer
    search_fields = ["username","first_name"]
    filterset_fields = []
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)



class User_Right_Set(APIView):
    authentication_classes = [ExpiringTokenAuthentication, SessionAuthentication,BasicAuthentication]
    def get(self, request, format=None):
        condition_list=[f"""v1.username='{request.user.username}' """]
        if "app_label" in request.GET and bool(request.GET["app_label"]):
            condition_list.append(f"""v4.app_label='{request.GET["app_label"]}'""")
        if "model" in request.GET and bool(request.GET["model"]):
            condition_list.append(f"""v4.model='{request.GET["model"]}'""")
        sql_str=f"""  SELECT v3.name,v4.model,v3.codename
  FROM [dbo].[auth_user] v1
  inner join [dbo].[auth_user_user_permissions] v2 on v1.id=v2.user_id
  inner join [dbo].[auth_permission] v3 on v2.permission_id=v3.id
  inner join [dbo].[django_content_type] v4 on v3.content_type_id=v4.id                 
  where {"and ".join(condition_list)}
  union 
  SELECT v3.name,v4.model,v3.codename
  FROM [dbo].[auth_user] v1
  inner join [dbo].[auth_user_groups] v1g on v1.id=v1g.user_id
  inner join [dbo].[auth_group_permissions] v2 on v1g.group_id=v2.group_id
  inner join [dbo].[auth_permission] v3 on v2.permission_id=v3.id
  inner join [dbo].[django_content_type] v4 on v3.content_type_id=v4.id
  where {"and ".join(condition_list)}
  union 
  select v3.name,v4.model,v3.codename
  from [dbo].[auth_user] v1
  inner join [dbo].[auth_permission] v3 on 1=1
  inner join [dbo].[django_content_type] v4 on v3.content_type_id=v4.id
  where {"and ".join(condition_list)} and v1.is_superuser=1
        """
        with connection.cursor() as cursor:
            cursor.execute(sql_str)
            data_list= [row[2] for row in cursor.fetchall()]
        return Response(data_list)

def api_view_logger(permission=None,is_log=True):
    def wrapper(func):
        def deco(*args, **kwargs):
            if permission is None or args[1].user.has_perm(permission):
                # 真正执行函数的地方
                error_code=""
                try:
                    return func(*args, **kwargs)
                except Exception as error:
                    error_code=str(error)
                    return Restful_Response({"message":error_code},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                finally:
                    if bool(is_log) or bool(error_code):
                        try:
                            qual_name=getattr(args[0],"__dict__")["basename"]+'.'+getattr(args[0],"__dict__")["action"]
                            path_url=getattr(getattr(args[0],"__dict__")["request"],"path")
                        except:
                            path_url=""
                            qual_name=func.__qualname__
                        log_obj = OperationLog(path_url=path_url,qual_name=qual_name,user_id=args[1].user.username,opeart_contect=json.dumps(dict(args[1].data)),error_code=error_code)
                        log_obj.save()
            else:
                return Restful_Response({"message":"验证失败"},status=status.HTTP_401_UNAUTHORIZED)       
        return deco
    return wrapper