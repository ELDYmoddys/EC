import pandas as pd
import numpy as np

from pyarrow import feather

###             id                    bal          blocks
exampledfdata = [(395368734732189696, 2312.000001, 1245),
                 (843448897737064448, 1241.0, 0)]



exampledf = pd.DataFrame(exampledfdata, columns=['uid', 'balance', 'blocks'])

exampledf.to_feather('users.feather')

## read balance:

read_df = pd.read_feather('users.feather')

print(read_df)
print(read_df['balance'].sum())

read_df = read_df.set_index('uid')
fella = read_df.loc[395368734732189696]

print(fella['balance'])
