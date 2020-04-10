import pyspark as ps
from pyspark.sql.types import *
from pyspark.sql import functions as func
from pyspark.sql.window import Window
import pandas as pd
import numpy as np
import scipy.stats
import matplotlib.pyplot as plt
import seaborn as sns
#plt.style.use('ggplot')
import requests 
import pprint
import json
import scipy.stats as stats
from sklearn.utils import resample



# Removing statistical outliers
def subset_by_iqr(df,col):
    
    q1 = df[col].quantile(0.25)
    q3 = df[col].quantile(0.75)
    iqr = q3 - q1
    
    filt_condition = (df[col] >= q1 - 1.5 * iqr) & (df[col] <= q3 + 1.5 * iqr)
    
    return df[filt_condition][col]

## Dealing with 50% percentile and above

def percentile(df):

    percentile_num = df.quantile(0.5)
    
    filtering = (df >= percentile_num)
    return df[filtering]

