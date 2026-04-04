import requests


class ParaBankClient:
    BASE_URL = "https://parabank.parasoft.com/parabank/services/bank"

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({"Accept": "application/json"})

    def register(self, first_name, last_name, username, password, ssn):
        # Establish session first
        reg_url = "https://parabank.parasoft.com/parabank/register.htm"
        self.session.get(reg_url)
        
        payload = {
            "customer.firstName": first_name,
            "customer.lastName": last_name,
            "customer.address.street": "123 Test St",
            "customer.address.city": "Boston",
            "customer.address.state": "MA",
            "customer.address.zipCode": "02101",
            "customer.phoneNumber": "555-0100",
            "customer.ssn": ssn,
            "customer.username": username,
            "customer.password": password,
            "repeatedPassword": password
        }
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
        }
        response = self.session.post(reg_url, data=payload, headers=headers)
        assert response.status_code in [200, 302], f"Expected status 200 or 302, got {response.status_code}. Response: {response.text}"
        
        # After successful registration, use the login method to get the customer_id
        return self.login(username, password)

    def login(self, username, password):
        from urllib.parse import quote
        url = f"{self.BASE_URL}/login/{quote(username)}/{quote(password)}"
        response = self.session.get(url)
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
