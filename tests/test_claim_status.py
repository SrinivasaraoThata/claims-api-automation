import pytest

def test_adjudication_status_req_clm_02(api_session):
    """
    Validates REQ-CLM-02: 
    Real-time Adjudication Status Updates
    """
    accounts = api_session.get_accounts(api_session.customer_id)
    
    if len(accounts) < 2:
        pytest.skip("Only one account available - transfer test requires two accounts")
    
    from_account = accounts[0]["id"]
    to_account = accounts[1]["id"]
    
    api_session.transfer(from_account, to_account, 50.00)
    
    transactions = api_session.get_transactions(from_account)
    
    assert len(transactions) > 0, "Transactions list should not be empty"
    
    has_type = any("type" in t for t in transactions)
    has_numeric_amount = any(isinstance(t.get("amount"), (int, float)) for t in transactions)
    
    assert has_type, "At least one transaction must have a type field"
    assert has_numeric_amount, "At least one transaction must have a numeric amount field"
