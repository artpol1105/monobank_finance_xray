import os
import time
import requests
from dotenv import load_dotenv

load_dotenv()


class MonoClient:
    def __init__(self):
        self.token = os.getenv("MONOBANK_API_TOKEN")
        self.base_url = "https://api.monobank.ua"
        self.headers = {"X-Token": self.token}

    def get_client_info(self):
        url = f"{self.base_url}/personal/client-info"
        response = requests.get(url, headers=self.headers)

        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()

    def get_statement(self, account_id, time_from, time_to):
        url = f"{self.base_url}/personal/statement/{account_id}/{time_from}/{time_to}"
        response = requests.get(url, headers=self.headers)

        if response.status_code == 200:
            return response.json()
        elif response.status_code == 429:
            print("Rate Limit 429: Wait 60 seconds to make new request")
            return None
        else:
            response.raise_for_status()


if __name__ == "__main__":
    client = MonoClient()
    target_account = os.getenv("MONOBANK_ACCOUNT_ID")

    if not target_account:
        print("Error. Check MONOBANK_ACCOUNT_ID in .env")
    else:
        try:
            print("Checking connection to API")
            info = client.get_client_info()
            print(f"Successful! Token owner: {info.get('name')}")

            time_to = int(time.time())
            time_from = time_to - (7 * 24 * 60 * 60)

            print(f"Statement for account N{target_account} for last week")
            statement = client.get_statement(target_account, time_from, time_to)

            if statement is not None:
                print(f"Get {len(statement)} transactions")
                if statement:
                    print(
                        f"Last transaction: {statement[0].get('description')} -> {statement[0].get('amount') / 100} грн")

        except requests.exceptions.RequestException as e:
            print(f"Error during request: {e}")