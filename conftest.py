import pytest
from client.api_client import ParaBankClient
from utils.data_factory import DataFactory

@pytest.fixture(scope="session")
def member_data():
    return DataFactory.generate_member()

@pytest.fixture(scope="session")
def api_session(member_data):
    client = ParaBankClient()
    
    customer_id = client.register(
        first_name=member_data["first_name"],
        last_name=member_data["last_name"],
        username=member_data["username"],
        password=member_data["password"],
        ssn=member_data["ssn"]
    )
    
    assert customer_id is not None, "Registration failed — cannot proceed with tests"
    
    client.login(username=member_data["username"], password=member_data["password"])
    
    accounts = client.get_accounts(customer_id=customer_id)
    assert len(accounts) > 0
    
    client.customer_id = customer_id
    client.account_id = accounts[0]["id"]
    
    yield client
