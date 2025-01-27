import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt
import seaborn as sns

# Input data files are available in the read-only "../input/" directory
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))
      
cus_data= pd.read_csv('/kaggle/input/customerzeotap/Customers.csv')
prod_data= pd.read_csv('/kaggle/input/customerzeotap/Products.csv')
trans_data= pd.read_csv('/kaggle/input/customerzeotap/Transactions.csv')


print(cus_data.head())
print(prod_data.head())
print(trans_data.head())

# Check data structure
print(cus_data.info())
print(prod_data.info())
print(trans_data.info())

# Check for missing values
print(cus_data.isnull().sum())
print(prod_data.isnull().sum())
print(trans_data.isnull().sum())

# Check for duplicates
print(cus_data.duplicated().sum())
print(prod_data.duplicated().sum())
print(trans_data.duplicated().sum())

print(cus_data.describe())
print(prod_data.describe())
print(trans_data.describe())

# Unique values in categorical columns
for col in cus.data.select_dtypes(include='object').columns:
    print(f"{col}: {cus_data[col].nunique()} unique values")

import matplotlib.pyplot as plt
data['CustomerID'].hist()
plt.show()

import matplotlib.pyplot as plt
data['ProductID'].hist()
plt.show()

import matplotlib.pyplot as plt
data['TransactionID'].hist()
plt.show()
