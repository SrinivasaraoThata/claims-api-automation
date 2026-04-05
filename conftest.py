import pytest
from client.api_client import ParaBankClient
from utils.data_factory import DataFactory

@pytest.fixture(scope="session")
def member_data():
    return DataFactory.generate_member()

@pytest.fixture(scope="session")
def api_session(member_data):
    client = ParaBankClient()
    
    customer_id = client.register(member_data)
    
    assert customer_id is not None, "Registration failed — cannot proceed with tests"
    
    client.login(username=member_data["username"], password=member_data["password"])
    
    accounts = client.get_accounts(customer_id=customer_id)
    assert len(accounts) > 0
    
    # If only 1 account exists, create a second one for transfer/history tests
    if len(accounts) < 2:
        client.create_account(customer_id, accounts[0]["id"])
        # Refresh accounts list
        accounts = client.get_accounts(customer_id=customer_id)
        
    # Seed transfer of 50.00 to ensure transaction history for tests
    first_acc = accounts[0]["id"]
    second_acc = accounts[1]["id"]
    client.transfer(first_acc, second_acc, 50.00)
    
    # Store IDs for reuse in test suite
    client.customer_id = customer_id
    client.account_id = first_acc
    client.second_account_id = second_acc
    
    # Allow ParaBank backend to process the transaction history
    import time
    time.sleep(1)
    
    yield client
