import pandas as pd
import requests
import numpy as np
from scipy.stats import pearsonr
from matplotlib import pyplot

###
### SOURCE
###

# READING FROM API SPREADSHEETS
budget = requests.get("https://api.apispreadsheets.com/data/hmSMNFPNl2MCGj7T/").json()["data"]
revenue = requests.get("https://api.apispreadsheets.com/data/Z3BNcYe1HlMhRFgV/").json()["data"]

# CONVERTING RAW DATA TO PANDAS DATAFRAME
budget_df = pd.DataFrame(budget)
revenue_df = pd.DataFrame(revenue)

###
### CLEAN
###

# LOWERCASE MOVIE NAMES
budget_df["Movie Name"] = budget_df["Movie Name"].str.lower()
revenue_df["Movie Name"] = revenue_df["Movie Name"].str.lower()

# JOIN THE DATASETS ON MOVIE NAME
movies = budget_df.merge(revenue_df, how="inner", on="Movie Name")

# CONVERT BUDGET TO NUMERICAL VALUE
movies["Budget"] = movies["Budget"].apply(lambda x: float(x.replace("$", "").replace(",", "")))

# CALCULATE RELATIVE PROFIT
movies['Profit'] = movies["Worldwide Gross Revenue ($)"] - movies["Budget"]
movies['Relative Profit'] = movies['Profit'] / movies['Budget']

###
### ANALYZE
###

# CALCULATE THE COVARIANCE MATRIX: https://www.cuemath.com/algebra/covariance-matrix/
covariance_matrix = np.cov(movies['Budget'], movies['Profit'])

# CALCULATE THE PEARSON CORRELATION COEFFICIENT: https://www.spss-tutorials.com/pearson-correlation-coefficient/
pearson_correlation, _ = pearsonr(movies['Budget'], movies['Profit'])

###
### REPORT
### 

# GRAPH OF BUDGET VS RELATIVE PROFIT
pyplot.scatter(movies['Budget'], movies['Profit'])
pyplot.show()


