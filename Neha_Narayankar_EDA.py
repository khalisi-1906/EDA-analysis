import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Input data files are available in the read-only "../input/" directory
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))
      
customers_df = pd.read_csv('Customers.csv')
products_df = pd.read_csv('Products.csv')
transactions_df = pd.read_csv('Transactions.csv')

#TASK 1:
    customers_df['SignupDate'] = pd.to_datetime(customers_df['SignupDate'])
    transactions_df['TransactionDate'] = pd.to_datetime(transactions_df['TransactionDate'])
    
    merged_df = transactions_df.merge(customers_df, on='CustomerID')\
                             .merge(products_df, on='ProductID')
merged_df.shape

merged_df.info()
merged_df.isnull().sum()
merged_df.describe()
merged_df.corr(numeric_only = True)

customer_purchase_freq = merged_df.groupby('CustomerID').size()\
                                    .describe()
    
customer_total_spend = merged_df.groupby('CustomerID')['TotalValue']\
                                  .sum().describe()
    
region_analysis = merged_df.groupby('Region')\
                             .agg({
                                 'TransactionID': 'count',
                                 'TotalValue': 'sum'
                             }).reset_index()

product_performance = merged_df.groupby('Category')\
                                 .agg({
                                     'TransactionID': 'count',
                                     'TotalValue': 'sum',
                                     'Quantity': 'sum'
                                 }).reset_index()

monthly_sales = merged_df.groupby(merged_df['TransactionDate'].dt.to_period('M'))\
                           .agg({
                               'TotalValue': 'sum',
                               'TransactionID': 'count'
                           })

customer_lifetime = merged_df.groupby('CustomerID').agg({
        'TotalValue': 'sum',
        'TransactionID': 'count',
        'TransactionDate': lambda x: (x.max() - x.min()).days
    }).reset_index()

plt.figure(figsize=(15, 10))
    
    # Plot 1: Monthly Sales Trend
plt.subplot(2, 2, 1)
monthly_sales['TotalValue'].plot()
plt.title('Monthly Sales Trend')
    
    # Plot 2: Region-wise Sales
plt.subplot(2, 2, 2)
sns.barplot(data=region_analysis, x='Region', y='TotalValue')
plt.title('Sales by Region')
    
    # Plot 3: Category Performance
plt.subplot(2, 2, 3)
sns.barplot(data=product_performance, x='Category', y='TotalValue')
plt.xticks(rotation=45)
plt.title('Sales by Category')
    
    # Plot 4: Customer Purchase Distribution
plt.subplot(2, 2, 4)
sns.histplot(customer_lifetime['TotalValue'])
plt.title('Customer Spending Distribution')
    
plt.tight_layout()
plt.show()

customer_lifetime

customer_purchase_freq,

category_region_sales = merged_df.pivot_table(
    values='TotalValue',
    index='Category',
    columns='Region',
    aggfunc='sum'
).round(2)


category_total_sales = category_region_sales.sum(axis=1)
category_region_sales = category_region_sales.loc[category_total_sales.sort_values(ascending=False).index]


plt.figure(figsize=(15, 8))

# Create bar plot
ax = category_region_sales.plot(kind='bar', width=0.8)


plt.title('Total Sales Value by Category and Region', pad=20, size=14)
plt.xlabel('Category', size=12)
plt.ylabel('Total Sales Value', size=12)
plt.legend(title='Region', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.xticks(rotation=45, ha='right')


for container in ax.containers:
    ax.bar_label(container, fmt='%.0f', rotation=0, padding=3)


plt.tight_layout()


plt.show()

print("\nTotal Sales by Category and Region:")
print(category_region_sales)

print("\nPercentage Contribution by Region:")
percentage_contribution = (category_region_sales.div(category_region_sales.sum()) * 100).round(2)
print(percentage_contribution)

merged_df.sample(10)
merged_df['TransactionDate'] = pd.to_datetime(merged_df['TransactionDate'])


merged_df['Month-Year'] = merged_df['TransactionDate'].dt.to_period('M')

monthly_category_sales = merged_df.pivot_table(
    values='TotalValue',
    index='Month-Year',
    columns='Category',
    aggfunc='sum'
).fillna(0)

monthly_category_sales.index = monthly_category_sales.index.astype(str)
monthly_category_sales = monthly_category_sales.sort_index()

plt.figure(figsize=(15, 8))

for category in monthly_category_sales.columns:
    plt.plot(monthly_category_sales.index, 
            monthly_category_sales[category], 
            marker='o', 
            label=category,
            linewidth=2,
            markersize=6)

plt.title('Monthly Sales Trends by Category', pad=20, size=14)
plt.xlabel('Month-Year', size=12)
plt.ylabel('Total Sales Value', size=12)
plt.legend(title='Category', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(True, linestyle='--', alpha=0.7)

plt.xticks(rotation=45, ha='right')

plt.tight_layout()

plt.show()

print("\nSummary Statistics by Category:")
summary_stats = monthly_category_sales.agg(['mean', 'min', 'max', 'std']).round(2)
print(summary_stats)

print("\nMonth-over-Month Growth Rates:")
growth_rates = monthly_category_sales.pct_change() * 100
average_growth = growth_rates.mean().round(2)
print("\nAverage Monthly Growth Rate by Category:")
print(average_growth)

print("\nPeak Sales Months by Category:")
for category in monthly_category_sales.columns:
    peak_month = monthly_category_sales[category].idxmax()
    peak_value = monthly_category_sales[category].max()
    print(f"{category}: {peak_month} (${peak_value:,.2f})")

#Month-over-Month Growth Rates:

""Average Monthly Growth Rate by Category:
Category
Books             inf
Clothing        88.97
Electronics     73.44
Home Decor     382.90
dtype: float64

Peak Sales Months by Category:
Books: 2024-05 ($21,793.32)
Clothing: 2024-09 ($18,906.19)
Electronics: 2024-07 ($22,096.51)
Home Decor: 2024-12 ($16,549.64)""









