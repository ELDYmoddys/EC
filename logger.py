import pandas as pd
from datetime import datetime
from deltalake.writer import write_deltalake

class Logger:
    def create_txn_log(giver_uid: int, reciever_uid: list, amount: list):

        txn_hash = generate_hash(giver_uid)
        timestamp = get_time()
        
        txn_data_list = [(txn_hash, timestamp, giver_uid, reciever_uid, amount)]
        txn_dataframe_to_app = pd.DataFrame(txn_data_list, columns=['txn_hash', 'timestamp', 'giver_uid', 'reciever_uid', 'amount'])

        write_logs(txn_dataframe_to_app)

        return txn_hash

    def read_txn_log(txn_hash: str):

        df = read_logs()
    
        txn_data = df.loc[df['txn_hash'] == txn_hash]

        if not txn_data.empty:
            return txn_data
        else:
            return False
        
    def fetch_txns(uid: int, page: int):

        df = read_logs()

        df = df.loc[df[f'giver_uid'] == uid][page*10-10:page*10]

        return df['txn_hash'].tolist()


def generate_hash(uid: int):

    tup = uid, get_time()

    return hex(abs(hash(tup)))

def get_time():

    time = int(datetime.timestamp(datetime.now()))

    return time

def read_logs():

    df = pd.read_parquet(r'txn_log.parquet')

    return df

def write_logs(df):

    write_deltalake(r'txn_log.parquet', df, mode="append")

    return
