from django.utils import timezone
from django .db .models import F

from apps.basefunction.models import UserIP, VisitNumber, DayNumber


def peekpa_tracking(func):
    def wrapper(request, *args, **kwargs):
        tacking_info(request)
        return func(request, *args, **kwargs)
    return wrapper


def tacking_info(request):
    update_visit_number()
    update_user_ip(request)
    update_day_visit_number()


def update_visit_number():
    count_nums = VisitNumber.objects.filter(id=1)
    if count_nums:
        count_nums = count_nums[0]
        count_nums.count = F('count') + 1
    else:
        count_nums = VisitNumber()
        count_nums.count = 1
    count_nums.save()


def update_user_ip(request):
    if 'HTTP_X_FORWARDED_FOR' in request.META:  # 获取 ip
        client_ip = request.META['HTTP_X_FORWARDED_FOR']
        client_ip = client_ip.split(",")[0]  # 所以这里是真实的 ip
    else:
        client_ip = request.META['REMOTE_ADDR']  # 这里获得代理 ip
    userIP_item = UserIP()
    userIP_item.ip_address = client_ip
    userIP_item.ip_location = "TBA"
    userIP_item.end_point = request.path
    userIP_item.day = timezone.now().date()
    userIP_item.save()


def update_day_visit_number():
    date = timezone.now().date()
    today = DayNumber.objects.filter(day=date)
    if today:
        temp = today[0]
        temp.count += 1
    else:
        temp = DayNumber()
        temp.dayTime = date
        temp.count = 1
    temp.save()
