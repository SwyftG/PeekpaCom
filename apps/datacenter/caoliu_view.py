from django.views.generic import View
from django.shortcuts import render

from .decorators import peekpa_code_required
from .common_view import get_side_bar_view
from django.utils.decorators import method_decorator
from apps.base.tracking_view import peekpa_tracking


@method_decorator(peekpa_code_required, name='get')
@method_decorator(peekpa_tracking, name='get')
class CaoliuListView(View):

    def get(self, request):
        context = get_side_bar_view()
        return render(request, 'datacenter/caoliu/manage.html', context=context)
