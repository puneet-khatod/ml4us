# rpt_predictions.r

# This script should report the effectiveness of predictions in predictions.csv

# Demo:
# R -f rpt_predictions.r

# I should read predictions.csv

predictions_df = read.csv('predictions.csv')

# I should report Long-Only Effectiveness:
sum(predictions_df$pctlead)

# I should calculate Model Effectiveness
predictions_df$effectiveness = sign(predictions_df$prediction) * predictions_df$pctlead
head(predictions_df)

# I should report Model Effectiveness:
sum(predictions_df$effectiveness)

'bye'