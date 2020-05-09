from django.http import JsonResponse

class HttpCode(object):
    ok = 200
    paramserror = 400   #参数错误
    unauth = 401    #没有授权
    methoderror = 405   # 方法错误POST/GET
    servererror = 500

#{'code':400, 'message':'', 'data':{}}
def result(code=HttpCode.ok, message="", data=None, kwargs=None):
    json_dict={"code": code, "message": message, "data": data}
    if kwargs and isinstance(kwargs, dict) and kwargs.keys():
        json_dict.update(kwargs)
    return JsonResponse(json_dict)

def params_error(message="", data=None):
    return result(code=HttpCode.paramserror, message=message, data=data)

def unauth(message="", data=None):
    return result(code=HttpCode.unauth, message=message, data=data)

def method_error(message="", data=None):
    return result(code=HttpCode.methoderror, message=message, data=data)

def server_error(message="", data=None):
    return result(code=HttpCode.servererror, message=message, data=data)

def ok():
    return result()