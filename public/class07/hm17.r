# hm17.r

# This script should show a nice demo of a heatmap in R.

# Demo:
# R -f hm17.r

# ref:
# http://stackoverflow.com/questions/24621070/heatmap-2-with-color-key-on-top

# I should do this once (similar to pip install):
# install.packages("gplots", repos="http://cran.us.r-project.org")

# # I should get GSPC dates and prices:
# gspc0_df = read.csv('http://ichart.finance.yahoo.com/table.csv?s=%5EGSPC')
# 
# # I should identify each row by Date instead of an integer:
# # row.names(gspc0_df) = gspc0_df$Date
# 
# # I should order by Date:
# gspc1_df = gspc0_df[order(gspc0_df$Date),]
# 
# head(gspc1_df)
# 
# # I should write the df to a csv:
# write.csv(gspc1_df,'gspc1_df.csv', row.names=FALSE)

gspc2_df           = read.csv('gspc1_df.csv')
gspc3_df           = data.frame(gspc2_df$Date,gspc2_df$Close)
colnames(gspc3_df) = c('cdate','cp')

# I should compute pctlead,pctlag1 from cp
len_i            = length(gspc3_df$cp)
last_f           = gspc3_df$cp[len_i]
leadp_v          = c(gspc3_df$cp, last_f)[1:len_i+1]
gspc3_df$pctlead = 100 * (leadp_v - gspc3_df$cp) / gspc3_df$cp
gspc3_df$pctlag1 = c(0, gspc3_df$pctlead)[1:len_i]

# I should get Month-of-Year, Day-of-Week from cdate.
# I should get a column like this: 01_2 which corresponds to January_Tuesday.
gspc3_df$moydow = format(as.Date(gspc3_df$cdate),"%m_%w")

# I should get rows after 1990-01-01:
pred_v   = (as.Date(gspc3_df$cdate) > '1990-01-01')
gspc4_df = gspc3_df[ pred_v , ]

# I should get rows where pctlag1 < 0:
down_v = (gspc4_df$pctlag1 < 0)

# I should get rows where pctlag1 >= 0:
up_v = (gspc4_df$pctlag1 >=0)

# I should use aggregate() to sum(pctlead) groupby Month-of-Year, Day-of-Week:
moydow0_d_df = aggregate(pctlead ~ moydow, gspc4_df[down_v,], sum)
moydow0_u_df = aggregate(pctlead ~ moydow, gspc4_df[up_v,  ], sum)

# I should order by moydow descending:
moydow1_d_df   = moydow0_d_df[order(moydow0_d_df$moydow),]
moydow1_u_df   = moydow0_u_df[order(moydow0_u_df$moydow),]

# I should hstack them:
d_pctlead = moydow1_d_df$pctlead
u_pctlead = moydow1_u_df$pctlead
moydow_df = data.frame(d_pctlead,u_pctlead)

# I should prepare df for feeding it to heatmap():
row.names(moydow_df) = moydow1_d_df$moydow
moydow_x             = data.matrix(moydow_df)

# I should report:
moydow_x

# I should create vectors full of color strings:
library(gplots)
row_i = nrow(moydow_x)
col5_v  = rainbow(5, start=0, end=2/6)
col60_v = rainbow(row_i, start=0, end=2/6)

# I should prep the layout for the heatmap.

# A default heatmap layout has 4 things:
# - Color Key, which is like a legend
# - Column Dendrogram, which I usually dont want
# - Row Dendrogram,    which I usually dont want
# - Heatmap,           which I always want
# A default heatmap layout is controlled by 4 integers: 4,3,2,1
# I use variables instead of integers:
colorKey_i  = 4
colDendro_i = 3
rowDendro_i = 2
heatmap_i   = 1
# I like to add margins and each margin needs an integer:
margin_left5_i = 5
margin_left6_i = 6

# I want the layout to look like this:
# -----------------------------------------------
# | margin_left5 | colorKey | colDendro(unused) |
# | margin_left6 | heatmap  | rowDendro(unused) |
# -----------------------------------------------

# I should use above integers to create a layout_matrix:
lmat_x = rbind(c(margin_left5_i, colorKey_i, colDendro_i)
              ,c(margin_left6_i, heatmap_i,  rowDendro_i))

lmat_x

# The above layout has 2 rows and 3 columns.
# I should specify height of each row:
row1height_f = 0.8
row2height_f = 5.0
lhei_v       = c(row1height_f,row2height_f)
# I should specify width of each column:
col1width_f = 1.0
col2width_f = 10.0
col3width_f = 1.0
lwid_v      = c(col1width_f, col2width_f, col3width_f)

# I should specify available colors and how they sort:
#color_v = rev(rainbow(20*10, start = 0/6, end = 4/6))
color_v = rev(rainbow(30, start = 0/6, end = 4/6))
# I should write the heatmap to png file:

png('hm17.png',width=800,height=2900)
heatmap.2(x=moydow_x, Rowv=NULL,Colv=NULL
  ,col = color_v
  ,scale="none"
  ,margins=c(19.0,0.0) # ("margin.Y", "margin.X")
  ,trace='none' 
  ,symkey=FALSE 
  ,symbreaks=FALSE 
  ,dendrogram='none'
  ,density.info='histogram' 
  ,denscol="black"
  ,keysize=1
  # For color-key at the top:
  #( "bottom.margin", "left.margin", "top.margin", "right.margin" )
  ,key.par=list(mar=c(3.5,0,3,0))
  ,lmat=lmat_x, lhei=lhei_v, lwid=lwid_v
  ,cexCol=4.0
  ,cexRow=2.0
)
dev.off()

'bye'
