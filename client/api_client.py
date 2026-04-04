import requests


class ParaBankClient:
    BASE_URL = "https://parabank.parasoft.com/parabank/services/bank"

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({"Accept": "application/json"})

    def register(self, first_name, last_name, username, password, ssn):
        url = f"{self.BASE_URL}/register"
        data = {
            "firstName": first_name,
            "lastName": last_name,
            "username": username,
            "password": password,
            "ssn": ssn
        }
        response = self.session.post(url, data=data)
        assert response.status_code == 200, f"Expected status 200, got {response.status_code}. Response: {response.text}"
        return response.json().get("id")

    def login(self, username, password):
        url = f"{self.BASE_URL}/login/{username}/{password}"
        response = self.session.post(url)
        assert response.status_code == 200, f"Expected status 200, got {response.status_code}. Response: {response.text}"
        return response.json().get("id")

    def get_accounts(self, customer_id):
        url = f"{self.BASE_URL}/customers/{customer_id}/accounts"
        response = self.session.get(url)
        assert response.status_code == 200, f"Expected status 200, got {response.status_code}. Response: {response.text}"
        return response.json()

    def get_transactions(self, account_id):
        url = f"{self.BASE_URL}/accounts/{account_id}/transactions"
        response = self.session.get(url)
        assert response.status_code == 200, f"Expected status 200, got {response.status_code}. Response: {response.text}"
        return response.json()

    def transfer(self, from_account, to_account, amount):
        url = f"{self.BASE_URL}/transfer"
        params = {
            "fromAccountId": from_account,
            "toAccountId": to_account,
            "amount": amount
        }
        response = self.session.post(url, params=params)
        assert response.status_code == 200, f"Expected status 200, got {response.status_code}. Response: {response.text}"
        return response

    def get_account(self, account_id):
        url = f"{self.BASE_URL}/accounts/{account_id}"
        response = self.session.get(url)
        assert response.status_code == 200, f"Expected status 200, got {response.status_code}. Response: {response.text}"
        return response.json()
