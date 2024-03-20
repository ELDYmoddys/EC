import pandas as pd
from datetime import datetime
from deltalake.writer import write_deltalake

class Logger:
    def create_txn_log(giver_uid, reciever_uid, amount):
        txn_hash = generate_hash(giver_uid)
        timestamp = get_time()
        
        txn_data_list = [(txn_hash, timestamp, giver_uid, reciever_uid, amount)]
        txn_dataframe_to_app = pd.DataFrame(txn_data_list, columns=['txn_hash', 'timestamp', 'giver_uid', 'reciever_uid', 'amount'])

        write_deltalake(r'C:\Users\eldym\OneDrive\Documents\EC_pandas\log.parquet', txn_dataframe_to_app, mode="append")

        return txn_hash

    def read_txn_log(txn_hash):

        df = pd.read_parquet(r'C:\Users\eldym\OneDrive\Documents\EC_pandas\log.parquet')
    
        txn_data = df.loc[df['txn_hash'] == txn_hash]

        if not txn_data.empty:
            return [txn_data['timestamp'], txn_data['giver_uid'], txn_data['reciever_uid'], txn_data['amount']]
        else:
            return False
        
    def fetch_txns(uid, page):

        



def generate_hash(uid):

    return hex(abs(hash(uid, get_time())))

def get_time():

    return int(datetime.timestamp(datetime.now))