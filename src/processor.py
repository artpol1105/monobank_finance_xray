import pandas as pd
from src.api_client import MonoClient
import os
import time


class DataProcessor:
    def __init__(self):
        pass

    def clean_transactions(self, raw_data):
        if not raw_data:
            return pd.DataFrame()

        df = pd.DataFrame(raw_data)

        if 'time' in df.columns:
            df['time'] = pd.to_datetime(df['time'], unit='s')

        money_columns = ['amount', 'operationAmount', 'cashbackAmount', 'balance']
        for col in money_columns:
            if col in df.columns:
                df[col] = df[col] / 100.0

        columns_to_keep = ['id', 'time', 'description', 'mcc', 'amount', 'balance', 'cashbackAmount']

        existing_columns = [col for col in columns_to_keep if col in df.columns]

        df = df[existing_columns]

        return df


if __name__ == "__main__":
    target_account = os.getenv("MONOBANK_ACCOUNT_ID")

    if target_account:
        client = MonoClient()

        time_to = int(time.time())
        time_from = time_to - (10 * 24 * 60 * 60)

        print("Extracting raw data")
        raw_statement = client.get_statement(target_account, time_from, time_to)

        if raw_statement:
            processor = DataProcessor()
            df = processor.clean_transactions(raw_statement)

            print("\nTransformed DataFrame")
            print(df.head())
            print("\nData types in columns:")
            print(df.dtypes)