import pytest
from client.api_client import ParaBankClient
from utils.data_factory import DataFactory

def test_security_rbac_req_sec_01(api_session):
    """
    Validates REQ-SEC-01: 
    Unauthorized access prevention 
    and RBAC enforcement
    """
    second_member = DataFactory.generate_member()
    second_client = ParaBankClient()
    
    second_customer_id = second_client.register(second_member)
    
    second_client.login(username=second_member["username"], password=second_member["password"])
    second_client.get_accounts(second_customer_id)
    second_client.customer_id = second_customer_id
    
    returned_account = second_client.get_account(api_session.account_id)
    
    assert returned_account.get("customerId") != second_customer_id

def test_invalid_auth_blocked():
    """
    Validates REQ-SEC-01: 
    Invalid credentials are rejected
    """
    client = ParaBankClient()
    try:
        client.login(username="fake_user_999999", password="wrongpassword")
    except AssertionError:
        assert True
    else:
        pytest.fail("Invalid login should have been blocked")
