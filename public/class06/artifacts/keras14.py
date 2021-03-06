# keras14.py

# This script should classify observations of S&P500 one-day percent gain.
# The two classes are above average and below average.
# Demo:
# ./keras_theano.bash keras14.py

import matplotlib.pyplot as plt
from keras.models import Sequential
from keras.layers.core import Dense, Activation
import pandas as pd
import numpy  as np
import pdb

# I should get prices:
prices_df = pd.read_csv('http://ichart.finance.yahoo.com/table.csv?s=%5EGSPC')[['Date','Close']]
prices_df.columns = ['cdate','cp']

# I should sort by cdate, ascending.
data_df = prices_df.copy().sort_values(by=['cdate'])

# I should compute pctlead:
data_df['pctlead'] = (100.0 * (data_df.cp.shift(-1) - data_df.cp) / data_df.cp).fillna(0)

# ref:
# http://www.ml4.us/cclasses/class03pd41
# http://pandas.pydata.org/pandas-docs/stable/computation.html#rolling-windows
# http://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.rolling.html#pandas.DataFrame.rolling

# I should declare which price-based, mvgavg-slope features I want:
slopes_a  = [2,3,4,5,6,7,8,9]

for slope_i in slopes_a:
  rollx          = data_df.rolling(window=slope_i)
  col_s          = 'slope'+str(slope_i)
  slope_sr       = 100.0 * (rollx.mean().cp - rollx.mean().cp.shift(1))/rollx.mean().cp
  data_df[col_s] = slope_sr

# I should generate Date features:
dt_sr = pd.to_datetime(data_df.cdate)
dow_l = [float(dt.strftime('%w' ))/100.0 for dt in dt_sr]
moy_l = [float(dt.strftime('%-m'))/100.0 for dt in dt_sr]
data_df['dow'] = dow_l
data_df['moy'] = moy_l

# I should split data_df into train_df and test_df
trainsize     = 25
testyear_i    = 2016
train_end_i   = testyear_i
train_end_s   = str(train_end_i)
train_start_i = train_end_i - trainsize
train_start_s = str(train_start_i)
# train and test observations should not overlap:
test_start_i  = train_end_i
test_start_s  = str(test_start_i)
test_end_i    = test_start_i+1
test_end_s    = str(test_end_i)

train_sr = (data_df.cdate > train_start_s) & (data_df.cdate < train_end_s)
test_sr  = (data_df.cdate > test_start_s)  & (data_df.cdate < test_end_s)
train_df = data_df[train_sr]
test_df  = data_df[test_sr]
# I should now have split data_df into train_df and test_df

# I should convert df to np-array:
x_train_a = np.array(train_df)[:,3:]
y_train_a = np.array(train_df.pctlead)

# I should 1-hot-encode class from y_train_a:
class_train_a = (y_train_a > np.mean(y_train_a))
y1h_l = [[0,1] if y_b else [1,0] for y_b in class_train_a]

# I should learn:

# I should use Keras API to create a neural network model:
model    = Sequential()
xshape_i = len(x_train_a[0])
yshape_i = len(y1h_l[0])
model.add(Dense(xshape_i, input_shape=(xshape_i,)))

# model.add(Activation('relu'))
model.add(Activation('sigmoid'))
model.add(Dense(yshape_i))
model.add(Activation('softmax'))

model.compile(loss='categorical_crossentropy', optimizer='adam')
model.fit(x_train_a, y1h_l, verbose=0, batch_size=1)

# I should get test data:
x_test_a = np.array(test_df)[:,3:]
y_test_a = np.array(test_df.pctlead)
# I should 1-hot-encode class from y_train_a:
class_test_a = (y_test_a > np.mean(y_train_a))
ytest1h_l = [[0,1] if y_b else [1,0] for y_b in class_test_a]

accuracy = model.evaluate(x_test_a, ytest1h_l, verbose=0)
print('accuracy:')
print(accuracy)

predictions_a  = model.predict(x_test_a)[:,1]
predictions_df = test_df.copy()
predictions_df['pred_keras14'] = predictions_a.reshape(len(predictions_a),1)

# I should report long-only-effectiveness:
eff_lo_f = np.sum(predictions_df.pctlead)
print('Long-Only-Effectiveness:')
print(eff_lo_f)

# I should report keras14-Effectiveness:
eff_sr     = predictions_df.pctlead * np.sign(predictions_df.pred_keras14 - 0.5)
predictions_df['eff_keras14'] = eff_sr
eff_keras14_f                 = np.sum(eff_sr)
print('keras14-Effectiveness:')
print(eff_keras14_f)

# I should try to save the model to be used later:
model.save_weights('model.hdf5')
with open('model.json', 'w') as f:
  f.write(model.to_json())
'bye'
  
