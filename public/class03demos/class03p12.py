"""
class03p12.py

This script should calculate RMSE of straight line between first and last prices of 2016.
"""

import pandas as pd
import numpy  as np

csvfile   = 'http://spy611.herokuapp.com/csv/allpredictions.csv'
cp_df     = pd.read_csv(csvfile).sort_values(['cdate'])
cp2016_sr = (cp_df.cdate > '2016') & (cp_df.cdate < '2017')
cp2016_df = cp_df[['cdate','cp']][cp2016_sr]
x1x0_i    = len(cp2016_df)
y1y0_f    = cp2016_df.iloc[-1].cp-cp2016_df.iloc[0].cp
m_f       = y1y0_f / x1x0_i
b_f       = cp2016_df.iloc[0].cp
# My equation for straight line:
def yval(x_in):
    return m_f * x_in + b_f
# I should collect points to plot straight line:
yvals_l = [ yval(x_i) for x_i in range(len(cp2016_df))]
# Add the points to the DataFrame:
cp2016_df['sl'] = yvals_l

# Goog: In Pandas how to combine columns?
# I should square the difference of each error:
sqdiffe = (cp2016_df.cp - cp2016_df.sl)**2

# I should find mean and then sqrt:
print('RMSE between straight line and closing price:')
rmse_f = np.sqrt(np.mean(sqdiffe))
print(rmse_f)

'bye'
