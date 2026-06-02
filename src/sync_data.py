import os
import time
from dotenv import load_dotenv
from src.api_client import MonoClient
from src.processor import DataProcessor
from src.database import SessionLocal, Transaction

load_dotenv()

MCC_DICT = mcc_dict = {
    5912: 'Pharmacies',
    5122: 'Drugs & Pharmacies',
    5812: 'Restaurants / Cafes',
    5814: 'Fast Food',
    5411: 'Supermarkets / Groceries',
    5462: 'Bakeries',
    5499: 'Markets / Specialty Foods',
    5441: 'Candy / Confectionery',
    5811: 'Caterers',
    7832: 'Cinemas',
    7941: 'Sports / Recreation',
    5641: 'Children\'s Apparel',
    5651: 'Family Clothing',
    5691: 'Apparel Stores',
    5661: 'Shoe Stores',
    5697: 'Tailoring / Alterations',
    5977: 'Cosmetics',
    5211: 'Building Materials',
    5942: 'Bookstores',
    5995: 'Pet Stores',
    5541: 'Gas Stations',
    8099: 'Medical Services',
    5311: 'Department Stores',
    5200: 'Home Goods',
    5399: 'Miscellaneous Goods',
    4812: 'Telecom Equipment / Phones',
    5300: 'Wholesale',
    5310: 'Discount Stores',
    5722: 'Household Appliances',
    4111: 'Transport / Tickets',
    4829: 'Money Transfers',
    4814: 'Telecommunication Services',
    4112: 'Passenger Railways / Trains',
    5945: 'Toys, Games & Hobbies',
    7399: 'Business & Online Services'
}


def run_etl():
    print("Starting ETL Pipeline")

    client = MonoClient()
    account_id = os.getenv("MONOBANK_ACCOUNT_ID")

    time_to = int(time.time())
    time_from = time_to - (30 * 24 * 60 * 60)

    print(f"Fetching transactions from Monobank API")
    raw_data = client.get_statement(account_id, time_from, time_to)

    processor = DataProcessor()
    df = processor.clean_transactions(raw_data)

    df['category'] = df['mcc'].apply(lambda x: MCC_DICT.get(x, f'Other (Code: {x})'))

    print(f"Processed {len(df)} transactions. Saving to database")

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
        print(f"Successfully synchronized {new_records_count} records with PostgreSQL!")

    except Exception as e:
        session.rollback()
        print(f"Error during database save: {e}")
    finally:
        session.close()


if __name__ == "__main__":
    run_etl()