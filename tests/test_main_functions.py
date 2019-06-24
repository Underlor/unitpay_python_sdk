from unitpay_python_sdk.exceptions import EmptyParams, BadIP, EmptyMethod, EmptySignature, BadSignature, \
    UnsupportedMethod
from unitpay_python_sdk.utils import parse_params


def test_unitpay_get_signature(unitpay_api, unitpay_check_data, unitpay_check_signature):
    """
        Тест метода получения сигнатуры словаря с методом
    """
    params = parse_params(unitpay_check_data)
    method = unitpay_check_data['method']
    signature = unitpay_api.get_signature(params, method)
    assert signature == unitpay_check_signature


def test_unitpay_check_handler_request(unitpay_api, unitpay_check_data):
    """
        Тест метода проверки запроса
    """
    result = unitpay_api.check_handler_request(unitpay_check_data, ip='127.0.0.1')
    assert result


def test_unitpay_check_handler_request_empty_params(unitpay_api, unitpay_check_data):
    """
        Тест метода проверки запроса пустые параметры
    """

    try:
        result = unitpay_api.check_handler_request({}, ip='127.0.0.1')
        assert not result
    except Exception as e:
        assert isinstance(e, EmptyParams)


def test_unitpay_check_handler_request_bad_ip(unitpay_api, unitpay_check_data):
    """
        Тест метода проверки запроса адрес не в списке разрешенных
    """

    try:
        result = unitpay_api.check_handler_request(unitpay_check_data, ip='127.0.0.0')
        assert not result
    except Exception as e:
        assert isinstance(e, BadIP)


def test_unitpay_check_handler_request_empty_method(unitpay_api, unitpay_check_data):
    """
        Тест метода проверки запроса не передан метод
    """

    del unitpay_check_data['method']
    try:
        result = unitpay_api.check_handler_request(unitpay_check_data, ip='127.0.0.1')
        assert not result
    except Exception as e:
        assert isinstance(e, EmptyMethod)


def test_unitpay_check_handler_request_empty_signature(unitpay_api, unitpay_check_data):
    """
        Тест метода проверки запроса не передана подпись
    """

    del unitpay_check_data['params[signature]']
    try:
        result = unitpay_api.check_handler_request(unitpay_check_data, ip='127.0.0.1')
        assert not result
    except Exception as e:
        assert isinstance(e, EmptySignature)


def test_unitpay_check_handler_request_bad_signature(unitpay_api, unitpay_check_data):
    """
        Тест метода проверки запроса невеная подпись
    """

    unitpay_check_data['params[signature]'] = '123'
    try:
        result = unitpay_api.check_handler_request(unitpay_check_data, ip='127.0.0.1')
        assert not result
    except Exception as e:
        assert isinstance(e, BadSignature)


def test_unitpay_check_handler_request_unsupported_method(unitpay_api, unitpay_check_data):
    """
        Тест метода проверки запроса неподдерживаемый метод
    """

    unitpay_check_data['method'] = '123'
    try:
        result = unitpay_api.check_handler_request(unitpay_check_data, ip='127.0.0.1')
        assert not result
    except Exception as e:
        assert isinstance(e, UnsupportedMethod)
