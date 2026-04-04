import json
import jsonschema
from pathlib import Path

def test_claim_submission_req_clm_01(api_session):
    """
    Validates REQ-CLM-01: 
    Claim Submission & Validation
    """
    accounts = api_session.get_accounts(api_session.customer_id)
    assert len(accounts) > 0
    
    account = api_session.get_account(api_session.account_id)
    
    assert "id" in account
    assert "customerId" in account
    assert "type" in account
    assert "balance" in account
    
    schema_path = Path(__file__).parent.parent / "schemas" / "account_schema.json"
    with open(schema_path, "r") as f:
        schema = json.load(f)
        
    jsonschema.validate(instance=account, schema=schema)
    
    assert isinstance(account["balance"], (int, float))
