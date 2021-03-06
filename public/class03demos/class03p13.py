"""
class03p13.py

This script should use Linear Algebra to find beta of a fitted line.
ref:
http://www.ml4.us/class03/pdf1.png
http://www.stat.purdue.edu/~jennings/stat514/stat512notes/topic3.pdf
"""

import pandas as pd
import numpy  as np

csvfile   = 'http://spy611.com/csv/allpredictions.csv'
cp_df     = pd.read_csv(csvfile).sort_values(['cdate'])
cp2016_sr = (cp_df.cdate > '2016') & (cp_df.cdate < '2017')
cp2016_df = cp_df[['cdate','cp']][cp2016_sr]

def colvec(arylst):
    # This should help me create column vectors from arrays or lists:
    return np.array(arylst).reshape((len(arylst),1))

# Study bottom of this image:
# http://www.ml4.us/class03/pdf1.png
# Y is easy to get, I should get Y first.
# I should transform the prices into a column vector of y-values:
yvals_a = colvec(cp2016_df.cp)
# Next I should work with X.

# I simplify; X-values are simple integers starting at 0:
x_a = colvec(range(len(cp2016_df)))
# Notice that I reshaped it into a column.
# Above pdf asks me to pre-pend a column vector of ones:

ones_l  = [1]*len(cp2016_df)
ones_a  = colvec(ones_l)

# I should build xvals_a from column of ones then integers:
xvals_a = np.hstack((ones_a,x_a))

# Now, I have X and Y, I should implement Linear Algebra with NumPy:
lhs_a = np.linalg.pinv(np.matmul(xvals_a.T,xvals_a))

rhs_a    = np.matmul(xvals_a.T,yvals_a)

beta_a   = np.matmul(lhs_a,rhs_a)
# refer to http://www.ml4.us/class03/pdf1.png

print('Beta for a line fitted to the GSPC prices is this:')
print(beta_a)

'bye'
