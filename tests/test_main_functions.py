import pytest

from unitpay_python_sdk.exceptions import EmptyParams, BadIP, EmptyMethod, EmptySignature, BadSignature, \
    UnsupportedMethod


def test_unitpay_get_signature(unitpay_api, unitpay_check_data, unitpay_check_signature):
    """
        Тест метода получения сигнатуры словаря с методом
    """
    params = unitpay_api.parse_params(unitpay_check_data)
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
    with pytest.raises(EmptyParams):
        unitpay_api.check_handler_request({}, ip='127.0.0.1')


def test_unitpay_check_handler_request_bad_ip(unitpay_api, unitpay_check_data):
    """
        Тест метода проверки запроса адрес не в списке разрешенных
    """
    with pytest.raises(BadIP):
        unitpay_api.check_handler_request(unitpay_check_data, ip='127.0.0.0')


def test_unitpay_check_handler_request_empty_method(unitpay_api, unitpay_check_data):
    """
        Тест метода проверки запроса не передан метод
    """

    del unitpay_check_data['method']
    with pytest.raises(EmptyMethod):
        unitpay_api.check_handler_request(unitpay_check_data, ip='127.0.0.1')


def test_unitpay_check_handler_request_empty_signature(unitpay_api, unitpay_check_data):
    """
        Тест метода проверки запроса не передана подпись
    """

    del unitpay_check_data['params[signature]']
    with pytest.raises(EmptySignature):
        unitpay_api.check_handler_request(unitpay_check_data, ip='127.0.0.1')


def test_unitpay_check_handler_request_bad_signature(unitpay_api, unitpay_check_data):
    """
        Тест метода проверки запроса невеная подпись
    """

    unitpay_check_data['params[signature]'] = '123'
    with pytest.raises(BadSignature):
        unitpay_api.check_handler_request(unitpay_check_data, ip='127.0.0.1')


def test_unitpay_check_handler_request_unsupported_method(unitpay_api, unitpay_check_data):
    """
        Тест метода проверки запроса неподдерживаемый метод
    """

    unitpay_check_data['method'] = '123'
    with pytest.raises(UnsupportedMethod):
        unitpay_api.check_handler_request(unitpay_check_data, ip='127.0.0.1')
