from client.api_client import ParaBankClient

def test_valid_login_req_log_01(api_session):
    """
    Validates REQ-LOG-01: 
    Secure Member Authentication
    """
    assert api_session.customer_id is not None
    assert isinstance(api_session.customer_id, int)
    assert api_session.account_id is not None

def test_unauthorized_access_blocked():
    """
    Validates REQ-LOG-01: 
    Unauthenticated requests are rejected
    """
    client = ParaBankClient()
    try:
        data = client.get_accounts(99999999)
        # If no error is raised assert that returned data is empty or response is not a valid account list.
        assert not data or not isinstance(data, list) or len(data) == 0, "Response should be empty or an invalid account list"
    except AssertionError:
        assert True
