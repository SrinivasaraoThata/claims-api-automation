import random
from faker import Faker

fake = Faker('en_US')

class DataFactory:

    @staticmethod
    def generate_member():
        first_name = fake.first_name()
        last_name = fake.last_name()
        # Append 6 random digits to username for uniqueness
        unique_digits = f"{random.randint(0, 999999):06d}"
        username = f"{first_name.lower()}{last_name.lower()}{unique_digits}"
        
        # ParaBank Rest API can be picky with characters, use simple alphanumeric password
        password = f"Pass{random.randint(1000, 9999)}"
        
        return {
            "first_name": first_name,
            "last_name": last_name,
            "username": username,
            "password": password,
            "ssn": fake.ssn(),
            "address": fake.street_address(),
            "city": fake.city(),
            "state": fake.state_abbr(),
            "zip_code": fake.zipcode(),
            "phone_number": "555-010-0000"
        }

    @staticmethod
    def generate_transfer_amount():
        return round(random.uniform(10.00, 500.00), 2)

    @staticmethod
    def generate_claim_reference():
        unique_digits = f"{random.randint(0, 99999999):08d}"
        return f"CLM-{unique_digits}"
