import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.metrics import davies_bouldin_score, silhouette_score
import matplotlib.pyplot as plt
import seaborn as sns

# Step 1: Load Datasets
cus = pd.read_csv('/kaggle/input/customerzeotap/Customers.csv')
trans = pd.read_csv('/kaggle/input/customerzeotap/Transactions.csv')

# Step 2: Merge Datasets
data = pd.merge(trans, cus, on='CustomerID')

# Step 3: Feature Engineering
# Aggregate transaction data for each customer
cus_metrics = data.groupby('CustomerID').agg({
    'TotalValue': 'sum',       # Total spend
    'TransactionID': 'count',  # Frequency of transactions
    'Price': 'mean',           # Average transaction value
}).rename(columns={'TransactionID': 'TransactionFrequency'})

# Add customer profile features (e.g., Region)
cus_metrics = pd.merge(cus_metrics, cus[['CustomerID', 'Region']], on='CustomerID')

# One-hot encode categorical variables
cus_metrics = pd.get_dummies(cus_metrics, columns=['Region'], drop_first=True)

# Step 4: Data Normalization
scaler = StandardScaler()
normalized_data = scaler.fit_transform(cus_metrics.drop(columns=['CustomerID']))

# Step 5: Apply Clustering
# Choose optimal number of clusters using Elbow Method
inertia = []
range_clusters = range(2, 11)

for k in range_clusters:
    kmeans = KMeans(n_clusters=k, random_state=42)
    kmeans.fit(normalized_data)
    inertia.append(kmeans.inertia_)
# Plot the Elbow Curve
plt.figure(figsize=(8, 5))
plt.plot(range_clusters, inertia, marker='o')
plt.title('Elbow Method')
plt.xlabel('Number of Clusters')
plt.ylabel('Inertia')
plt.show()

# Final KMeans Clustering with chosen K (e.g., 4)
kmeans = KMeans(n_clusters=4, random_state=42)
clusters = kmeans.fit_predict(normalized_data)
# Step 6: Evaluate Clustering
db_index = davies_bouldin_score(normalized_data, clusters)
sil_score = silhouette_score(normalized_data, clusters)

print(f"Davies-Bouldin Index: {db_index}")
print(f"Silhouette Score: {sil_score}")

# Add cluster labels to the dataset
cus_metrics['Cluster'] = clusters

# Step 7: Visualize Clusters
# Reduce dimensions with PCA
pca = PCA(n_components=2)
reduced_data = pca.fit_transform(normalized_data)
cus_metrics['PCA1'] = reduced_data[:, 0]
cus_metrics['PCA2'] = reduced_data[:, 1]

# Plot clusters
plt.figure(figsize=(10, 6))
sns.scatterplot(
    x='PCA1', y='PCA2', hue='Cluster', data=customer_metrics, palette='viridis', s=50
)
plt.title('Customer Clusters (PCA Reduced)')
plt.show()

# Step 8: Save Results
cus_metrics.to_csv('Customer_Segments.csv', index=False
