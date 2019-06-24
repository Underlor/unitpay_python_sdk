import copy
import hashlib
import json
import re
import urllib.parse
from urllib.request import urlopen

from unitpay_python_sdk.exceptions import EmptyParams, BadIP, EmptyMethod, EmptySignature, BadSignature, \
    UnsupportedMethod
from unitpay_python_sdk.utils import remove_signature, dict_to_sorted_kv_list, value_list_from_kv_list, \
    insert_url_encode


class UnitPay:
    form_url = 'https://unitpay.ru/pay/'
    api_url = 'https://unitpay.ru/api'

    supported_unitpay_methods = ['initPayment', 'getPayment']
    required_unitpay_methods_params = {'initPayment': ['desc', 'account', 'sum'], 'getPayment': ['paymentId']}
    supported_partner_methods = ['check', 'pay', 'error']

    supported_unitpay_ip = [
        '31.186.100.49',
        '178.132.203.105',
        '52.29.152.23',
        '52.19.56.234',
    ]

    def __init__(self, secret_key, debug=False):
        self.secret_key = secret_key

        if debug:
            self.supported_unitpay_ip.append('127.0.0.1')

    def form(self, public_key, summ, account, desc, currency='RUB', locale='ru'):
        params = dict(
            account=account,
            currency=currency,
            desc=desc,
            sum=summ
        )
        params['signature'] = self.get_signature(params)
        params['locale'] = locale

        return self.form_url + public_key + '?' + urllib.parse.urlencode(params)

    @staticmethod
    def parse_params(s):
        # TODO Need rewrite
        params = {}
        for v in s:
            if re.search('params', v):
                p = v[len('params['):-1]
                params[p] = s[v]
        return params

    def get_signature(self, params, method=None):
        params = copy.copy(params)

        params = remove_signature(params)
        params = dict_to_sorted_kv_list(params)
        params.append([0, self.secret_key])

        if method:
            params.insert(0, ['method', method])

        params = value_list_from_kv_list(params)

        params_string = '{up}'.join(params).encode('utf-8')

        return hashlib.sha256(params_string).hexdigest()

    def check_handler_request(self, request_params: dict, ip):
        params = self.parse_params(request_params)

        if not params:
            raise EmptyParams()

        if ip not in self.supported_unitpay_ip:
            raise BadIP()

        if 'method' not in request_params:
            raise EmptyMethod()
        method = request_params['method']

        if method not in self.supported_partner_methods:
            raise UnsupportedMethod()

        if 'signature' not in params:
            raise EmptySignature()

        signature = self.get_signature(params, method)
        if params['signature'] != signature:
            raise BadSignature()

        return True

    @staticmethod
    def get_error_handler_response(message):
        return json.dumps({'error': {'message': message}})

    @staticmethod
    def get_success_handler_response(message):
        return json.dumps({'result': {'message': message}})

    def api(self, method, params=None):
        if params is None:
            params = {}
        if method not in self.supported_unitpay_methods:
            raise Exception('Method is not supported')
        for rParam in self.required_unitpay_methods_params[method]:
            if rParam not in params:
                raise Exception('Param ' + rParam + ' is null')
        params['secretKey'] = self.secret_key
        request_url = self.api_url + '?method=' + method + '&' + insert_url_encode('params', params)
        response = urlopen(request_url)
        data = response.read().decode('utf-8')
        jsons = json.loads(data)
        return jsons
