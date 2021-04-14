from ldap3 import Connection, ServerPool
from django.conf import settings

def ldap_auth(username, password):
    """
    ldap验证,服务器池setting中设置
    """
    # ladp的服务器池
    ldap_server_pool = ServerPool(settings.LDAP_SERVER_POOL)
    # ad用户处理
    if "/" in username:
        ad_user = username
    elif "@" in username:
        ad_user = username
    else:
        # 如果不符合域用户格式，自动添加域名
        ad_user = f"""{username}@{settings.AD_DOMAIN_NAME}"""
    # 尝试链接域控
    conn = Connection(ldap_server_pool, user=ad_user, password=password,
                      check_names=True, lazy=False, raise_exceptions=False)
    conn.open()
    conn.bind(read_server_info=False)

    is_pass= True if conn.result["result"]==0 else False
    conn.unbind()
    return is_pass

if __name__ == "__main__":
    username = input("请输入用户名:")
    password = input("请输入密码:")
    print(ldap_auth(username, password))
    input("请输入任意键退出:")
