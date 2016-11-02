# f10.py

# This script should read and aggregate some forex data.

import pandas as pd
from datetime import datetime

f0_df = pd.read_csv('small.csv', names=['pair','ts0','bid','ask'])

f1_df       =  f0_df.copy()[['pair','ts0']]
f1_df['cp'] = (f0_df.bid+f0_df.ask)/2
ts1_l       = [ts[:14] for ts in f1_df.ts0]
ts2_sr      = pd.to_datetime(ts1_l, utc=True)
f1_df['ts'] = [5*60*int(int(ts.strftime("%s"))/5/60) for ts in ts2_sr]
f2_df       = f1_df.copy()[['ts','cp']]
print(f2_df.tail())
f3_df = f2_df.groupby(['ts']).cp.mean()
print(f3_df.head())
print(f3_df.tail())

f3_df.to_csv('eur.csv', float_format='%4.6f', index=False)

'bye'
