import os
import time
from dotenv import load_dotenv
from src.api_client import MonoClient
from src.processor import DataProcessor
from src.database import SessionLocal, Transaction
from src.config import mcc_dict
from datetime import datetime

load_dotenv()

def run_etl():
    print("Starting ETL Pipeline")

    client = MonoClient()
    account_id = os.getenv("MONOBANK_ACCOUNT_ID")
    processor = DataProcessor()

    current_time_to = int(time.time())
    months_to_fetch = 1

    for i in range(months_to_fetch):
        current_time_from = current_time_to - (30 * 24 * 60 * 60)

        date_from = datetime.fromtimestamp(current_time_from).strftime('%Y-%m-%d')
        date_to = datetime.fromtimestamp(current_time_to).strftime('%Y-%m-%d')
        print(f"Fetching transactions from Monobank API from {date_from} to {date_to}")

        try:
            raw_data = client.get_statement(account_id, current_time_from, current_time_to)

            if not raw_data:
                print("No transactions found in this period.")
            else:
                df = processor.clean_transactions(raw_data)
                df['category'] = df['mcc'].apply(lambda x: mcc_dict.get(x, f'Other (Code: {x})'))

                session = SessionLocal()
                try:
                    new_records_count = 0
                    for _, row in df.iterrows():
                        txn = Transaction(
                            id=row['id'],
                            time=row['time'],
                            description=row['description'],
                            mcc=row['mcc'],
                            amount=row['amount'],
                            balance=row['balance'],
                            cashbackAmount=row['cashbackAmount'],
                            category=row['category']
                        )
                        session.merge(txn)
                        new_records_count += 1

                    session.commit()
                    print(f"{new_records_count} records saved to PostgreSQL.")
                except Exception as e:
                    session.rollback()
                    print(f"Saving error: {e}")
                finally:
                    session.close()

        except Exception as api_err:
            print(f"API error {api_err}")

        current_time_to = current_time_from

        if i < months_to_fetch - 1:
            print("Waiting 61 seconds for Monobank API to complete.")
            time.sleep(61)

    print("\nMassive loading finished")


if __name__ == "__main__":
    run_etl()