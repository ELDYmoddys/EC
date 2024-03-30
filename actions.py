import pandas as pd
from main import DECIMALS
from logger import Logger
from deltalake.writer import write_deltalake

class Actions:
    def create_user(uid: int):

        new_user = [(uid, float(f'0.' + '0'*DECIMALS), 0)]
        df = pd.DataFrame(new_user, columns=['uid', 'balance', 'blocks'])
        write_deltalake(r'user_info.parquet', df, mode="append")

        return
        
    def fetch_balance(uid: int):

        df = read_bals()
        data = df.loc[df['uid'] == uid]

        if not data.empty:
            return data['balance'][0], data['blocks'][0]
        else:
            return False
    
    def transaction(giver: int, reciever: int, amount: float):

        if Actions.fetch_balance(reciever) is not False:
            pass # WIP!

        return txn_hash, fail_case




def read_bals():

    df = pd.read_parquet(r'user_info.parquet')

    return df