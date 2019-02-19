import pandas as pd
import numpy as np

data = pd.read_csv("Processed-text.csv",low_memory=False,date_parser=[2],parse_dates=True,
                   infer_datetime_format =True)

#Drop row containg nan in reviews
data = data.dropna(how='any')

