from unitpay_python_sdk import UnitPay
from django.views import View
from django.conf import settings
from django.http import HttpResponse


def get_ip(response):
    directional = response.META.get('HTTP_X_FORWARDED_FOR')
    if directional:
        IP = directional.split(',')[0]
    else:
        IP = response.META.get('REMOTE_ADDR')
    return IP


class PaymentView(View):
    def get(self, request, *args, **kwargs):
        api = UnitPay("Private key", debug=settings.DEBUG)

        if request.GET.get('method') == 'check':
            if api.check_handler_request(request.GET, get_ip(request)):
                # Успешно проверили order
                return HttpResponse(api.get_success_handler_response('Запрос успешно обработан'))

        if request.GET.get('method') == 'pay':
            if api.check_handler_request(request.GET, get_ip(request)):
                # Успешный платеж
                return HttpResponse(api.get_success_handler_response('Pay Success'))

        if request.GET.get('method') == 'error':
            if api.check_handler_request(request.GET, get_ip(request)):
                # Ошибка, после ошибки может быть успешный платеж
                return HttpResponse(api.get_success_handler_response('Error logged'))

        if request.GET.get('method') == 'refund':
            if api.check_handler_request(request.GET, get_ip(request)):
                # refund
                return HttpResponse(api.get_success_handler_response('Order canceled'))

        return HttpResponse(api.get_error_handler_response('BadMethod'))
