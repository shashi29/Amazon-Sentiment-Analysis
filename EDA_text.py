import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

data = pd.read_csv("Processed-text.csv",low_memory=False,index_col = [2], parse_dates=[2]).sort_index()
data.drop(columns=['Unnamed: 0','body'],inplace=True,axis=1)

#Sales Distribution basis on comment
monthly_order_count = data.resample('M').count()
#orders_monthly.dropna(how='any',inplace=True)
monthly_order_count = pd.DataFrame(monthly_order_count)
#plt.plot_date(x=orders_monthly.index,y=orders_monthly['rating'],fmt='o')
monthly_order_count.rename(columns={'rating':'Sales'},inplace=True)
ax = sns.lineplot(x=monthly_order_count.index , y=monthly_order_count['Sales'] , data=monthly_order_count , markers = True )

#Overall sentiment over time period
orders_monthly = data.resample('M').median()
orders_monthly = pd.DataFrame(orders_monthly)
ax = sns.lineplot(x=orders_monthly.index , y=orders_monthly['rating'] , data=orders_monthly , markers = True )

import plotly.graph_objs as go
import plotly.offline as py

actual_chart = go.Scatter(x=orders_monthly.index , y=orders_monthly['Sales'],
                          mode = 'lines+markers')
py.plot([actual_chart])