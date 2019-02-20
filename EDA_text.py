import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

data = pd.read_csv("Processed-text.csv",low_memory=False,index_col = [2], parse_dates=[2]).sort_index()
data.drop(columns=['Unnamed: 0','body'],inplace=True,axis=1)

#Sales Distribution basis on comment
orders_monthly = data.resample('M').count()
#orders_monthly.dropna(how='any',inplace=True)
orders_monthly = pd.DataFrame(orders_monthly)
#plt.plot_date(x=orders_monthly.index,y=orders_monthly['rating'],fmt='o')
orders_monthly.rename(columns={'rating':'Sales'},inplace=True)
ax = sns.lineplot(x=orders_monthly.index , y=orders_monthly['Sales'] , data=orders_monthly , markers = True )

#Overall sentiment over time period
orders_monthly = data.resample('M').mean()
orders_monthly = pd.DataFrame(orders_monthly)
ax = sns.lineplot(x=orders_monthly.index , y=orders_monthly['rating'] , data=orders_monthly , markers = True )

