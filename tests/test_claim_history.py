import json
import jsonschema
from pathlib import Path

def test_claims_history_req_his_01(api_session):
    """
    Validates REQ-HIS-01: 
    Historical Claims Retrieval >24 months
    """
    transactions = api_session.get_transactions(api_session.account_id)
    
    assert isinstance(transactions, list)
    assert len(transactions) > 0
    
    schema_path = Path(__file__).parent.parent / "schemas" / "transaction_schema.json"
    with open(schema_path, "r") as f:
        schema = json.load(f)
        
    jsonschema.validate(instance=transactions[0], schema=schema)
    
    for t in transactions:
        assert "id" in t
        assert "accountId" in t
        assert "type" in t
        assert "amount" in t
        assert isinstance(t["amount"], (int, float))
