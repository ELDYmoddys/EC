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

        txn_hash = None

        giver_info = Actions.fetch_balance(giver)
        reciever_info = Actions.fetch_balance(reciever)

        if giver_info is not False and reciever_info is not False:
            if float(f'0.' + '0'*(DECIMALS-1) + '1'): # checks if the amount is within the minimum threshold
                if giver_info[0] >= amount:
                    try: 
                        df = read_bals()
                        df.loc[df['uid'] == giver]['balance'] -= amount
                        df.loc[df['uid'] == reciever]['balance'] += amount
                        write_bals(df)
                    except:
                        fail_case = 'error_modify'
                    else:
                        txn_hash = Logger.create_txn_log()               
                else:
                    fail_case = 'bal_too_low'
            else:
                fail_case = 'invalid_amt'
        else:
            if giver_info is False:
                fail_case = 'no_bal_self'
            elif reciever_info is False:
                fail_case = 'no_bal_reciever'
            else:
                fail_case = 'no_bals'

        return txn_hash, fail_case

def read_bals(): # gets balance data

    df = pd.read_parquet(r'user_info.parquet')

    return df

def write_bals(df): # takes dataframe and overwrites the balance info

    write_deltalake(r'user_info.parquet', df, mode="overwrite")

    return