import json

import pytest

from unitpay_python_sdk.api import UnitPay


@pytest.fixture
def unitpay_api() -> UnitPay:
    return UnitPay('TEST_KEY', debug=True)


@pytest.fixture
def unitpay_check_data() -> dict:
    test_check_data = '{"method": "check", "params[account]": "test", "params[date]": "2019-06-24 01:49:40", "params[ip]": "2.95.204.154", "params[operator]": "euroset", "params[orderCurrency]": "RUB", "params[orderSum]": "10.00", "params[payerCurrency]": "RUB", "params[payerSum]": "10.00", "params[paymentType]": "cash", "params[profit]": "9.4", "params[projectId]": "12345", "params[signature]": "b1bcb5daf160ae4ef9f97e1d827a2caf8ab65c690fd47d94e17af150220a482f", "params[sum]": "10", "params[test]": "1", "params[unitpayId]": "994"}'
    return json.loads(test_check_data)


@pytest.fixture
def unitpay_check_signature() -> str:
    return 'b1bcb5daf160ae4ef9f97e1d827a2caf8ab65c690fd47d94e17af150220a482f'
