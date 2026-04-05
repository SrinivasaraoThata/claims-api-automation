import requests


class ParaBankClient:
    BASE_URL = "https://parabank.parasoft.com/parabank/services/bank"

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({"Accept": "application/json"})

    def register(self, member_data):
        # Establish session first
        reg_url = "https://parabank.parasoft.com/parabank/register.htm"
        self.session.get(reg_url)
        
        payload = {
            "customer.firstName": member_data["first_name"],
            "customer.lastName": member_data["last_name"],
            "customer.address.street": member_data["address"],
            "customer.address.city": member_data["city"],
            "customer.address.state": member_data["state"],
            "customer.address.zipCode": member_data["zip_code"],
            "customer.phoneNumber": member_data["phone_number"],
            "customer.ssn": member_data["ssn"],
            "customer.username": member_data["username"],
            "customer.password": member_data["password"],
            "repeatedPassword": member_data["password"]
        }
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        response = self.session.post(reg_url, data=payload, headers=headers)
        assert response.status_code in [200, 302], f"Expected status 200 or 302, got {response.status_code}. Response: {response.text}"
        
        # Check for successful registration message in response body
        if "Your account was created successfully" not in response.text:
            # Print full response text for debugging
            # print(f"DEBUG: Registration response: {response.text}") # Trace this in log
            pass
        
        # Add a short delay to ensure ParaBank backend persists the new user before REST login
        import time
        time.sleep(1)
        
        return self.login(member_data["username"], member_data["password"])

    def login(self, username, password):
        from urllib.parse import quote
        import time
        # Ensure credentials are clean of whitespace
        username = username.strip()
        password = password.strip()
        url = f"{self.BASE_URL}/login/{quote(username)}/{quote(password)}"
        
        # ParaBank REST API sync latency can be unpredictable.
        # We use a robust retry mechanism (up to 10 seconds of attempts).
        for attempt in range(10):
            response = self.session.get(url)
            if response.status_code == 200:
                try:
                    data = response.json()
                    customer_id = data.get("id")
                    if customer_id:
                        return customer_id
                except:
                    pass # Continue to retry if JSON is invalid
            
            if attempt < 9:
                time.sleep(1)
            
        assert response.status_code == 200, f"Login failed for {username} after retries. Expected 200, got {response.status_code}. Response: {response.text}"
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

    def create_account(self, customer_id, from_account_id):
        url = f"{self.BASE_URL}/createAccount"
        params = {
            "customerId": customer_id,
            "newAccountType": 1,
            "fromAccountId": from_account_id
        }
        response = self.session.post(url, params=params)
        assert response.status_code == 200
        return response.json()
