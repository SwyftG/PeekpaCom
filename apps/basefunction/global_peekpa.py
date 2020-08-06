from apps.datacenter.models import Code
from apps.basefunction.models import NavbarItem
from django.db.models import F


peekpa_config = {
    'HAS_INIT': False
}


def init_peekpa():
    print("peekpa_init_start")
    init_peekpa_config()
    print("peekpa_init_end")


def get_peekpa_item(name):
    if name in peekpa_config:
        data_list = peekpa_config[name]
        return data_list
    return None


def init_peekpa_config():
    avaliable_code = Code.objects.filter(status=Code.STATUS_NORMAL).all()
    code_list = []
    for item in avaliable_code:
        code_list.append(item)
    peekpa_config["CODE"] = code_list
    available_navitem = NavbarItem.objects.filter(status=NavbarItem.STATUS_NORMAL).all()
    navitem_list = []
    for item in available_navitem:
        navitem_list.append(item)
    peekpa_config["NAVITEM"] = navitem_list


def check_code_session_by(session):
    # TODO 为了测试，这里直接写死返回True，需要判断的时候，可以将代码修改回来
    # if "CODE" in peekpa_config:
    #     for item in peekpa_config["CODE"]:
    #         if session[item.session_name]:
    #             if session[item.session_name] == item.session_uid:
    #                 Code.objects.filter(uid=item.uid).update(visit_num=F('visit_num') + 1)
    #                 return True
    # return False
    return True


def check_url(request):
    if "NAVITEM" in peekpa_config:
        for item in peekpa_config["NAVITEM"]:
            if item.url_path == request.path:
                return True
    return False

def get_code_session(code):
    session_name = None
    session_uid = None
    if "CODE" in peekpa_config:
        code_list = peekpa_config["CODE"]
        if code_list:
            for item in code_list:
                if item.code == code:
                    session_name = item.session_name
                    session_uid = item.session_uid
    return session_name, session_uid