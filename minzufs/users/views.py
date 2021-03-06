from users.models import UserProfile


# 设置返回数据的格式
def jwt_response_payload_handler(token, user: UserProfile = None, request=None):
    """
    自定义jwt认证成功返回数据
    :param token: 本次登录成功后返回的jwt
    :param user: 本次登录成功后，从数据库中查询到的用户模型信息
    :param request: 本次客户端的请求对象
    :return:
    """
    return {
        'id': user.id,
        'token': token,
        'username': user.username,
    }
