# get_predictions.r

# This script should use a function and a loop to get many predictions.
# This script depends on genf.r to create feat.csv
# This script depends on hr_model.r to create modelYYYY.csv

# Ref:
# http://www.ml4.us/cclasses/class07#hr

# Demo:
# R -f get_predictions.r

get_prediction = function(dt_s,feat_df){
  # This function should get a prediction after I pass it a date string.
  # First, I should get value of YYYY so I can locate modelYYYY.csv
  yr_s     = format(as.Date(dt_s),"%Y")
  csv_s    = paste('model',yr_s,'.csv', sep='')
  # I should get value of pctlag, moydow from feat_df using dt_s.
  row_v    = (feat_df$cdate == dt_s)
  pctlag_f = feat_df[row_v,]$pctlag
  moydow_s = feat_df[row_v,]$moydow
  # I should use moydow to get a row from model:
  model_df = read.csv(csv_s)
  pred_v   = (moydow_s == model_df$moydow)

  # I should use pctlag_f to pick which column in the model csv I want:
  if (pctlag_f > 0){
    return(model_df[pred_v , ]$pctlead_after_up_pctlag)
  } else {
    return(model_df[pred_v , ]$pctlead_after_down_pctlag)
  }
}

# I should fill this vector with predictions:
predictions_v = c()

# I should use feat.csv to give me dates:
feat0_df = read.csv('feat.csv')

# I should constrain the dates:
pred_v = (as.Date(feat0_df$cdate) > as.Date('2000-01-01'))
feat1_df = feat0_df[pred_v , ]

for (dt_s in feat1_df$cdate){
  predictions_v = c(predictions_v,  get_prediction(dt_s,feat1_df))
}

# I should write the predictions to CSV:
feat1_df$prediction = predictions_v
write.csv(feat1_df, 'predictions.csv', row.names=FALSE)

# For 2016,
# after I pick 4 random days in oct,
# I should see these predictions:

# day, moydow, prediction
# 10-24,10_1,  3.51  
# 10-25,10_2, -8.79 
# 10-26,10_3,  4.71  
# 10-27,10_4,  8.49

'bye'
