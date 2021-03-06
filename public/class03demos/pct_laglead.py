"""
pct_laglead.py

This script should compute columns pctlag1 and pctlead from closep.
"""

import pandas as pd

prices_df = pd.read_csv('http://ml4.us/csv/GSPC.csv')
prices_df.columns = ['cdate_s','openp','highp','lowp','closep','adjp','volume']

# I should get 2016 July and two columns:
pred_sr = (prices_df.cdate_s > '2016-07') & (prices_df.cdate_s < '2016-08')
s1_df   = prices_df[pred_sr][['cdate_s','closep']]

pctlead = 100 * (s1_df.closep.shift(-1) - s1_df.closep) / s1_df.closep
pctlag1 = 100 * (s1_df.closep - s1_df.closep.shift(1)) / s1_df.closep.shift(1)

s1_df['pctlag1'] = pctlag1
s1_df['pctlead'] = pctlead

# I should visualize:
print(s1_df)

'bye'
