# pct_laglead.py

# This script should compute columns pctlag1 and pctlead from closep.

import pandas as pd

prices_df = pd.read_csv('http://ichart.finance.yahoo.com/table.csv?s=%5EGSPC')
prices_df.columns = ['cdate_s','openp','highp','lowp','closep','volume','adjp']

# I should get 2016 July and two columns:
pred_sr = (prices_df.cdate_s > '2016-07') & (prices_df.cdate_s < '2016-08')
s1_df   = prices_df[pred_sr][['cdate_s','closep']]

# visualize a push-down so top row becomes NaN:
s2_df = s1_df.shift(1)

# visualize a push-up so bottom row becomes NaN:
s3_df = s1_df.shift(-1)

# I should use the shifted rows:
pctlag1 = 100 * (s1_df.closep - s3_df.closep) / s1_df.closep
pctlead = 100 * (s2_df.closep - s1_df.closep) / s2_df.closep

s1_df['pctlag1'] = pctlag1
s1_df['pctlead'] = pctlead

# I should establish a column order which makes sense:
s1_df = s1_df[['cdate_s','closep','pctlag1','pctlead']]

# I should visualize:
print(s1_df)

'bye'
