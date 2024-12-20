# -*- coding: utf-8 -*-


**Mall Customer Segmentation Data**
**- Unsupervised ML technique (KMeans Clustering Algorithm)**
"""

# Commented out IPython magic to ensure Python compatibility.
# Import necessary libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
# %matplotlib inline
import plotly.express as px
import plotly.graph_objects as go
import warnings
warnings.filterwarnings('ignore')

#Load the dataset
file_path = "Mall_Customers.csv"
data = pd.read_csv(file_path)

data.head()

data.info()

data.describe().style.format("{:.2f}")

columns = ['Age', 'Annual Income (k$)',
       'Spending Score (1-100)']
for i in columns:
    plt.figure()
    sns.distplot(data[i], color='dodgerblue')

columns = ['Age', 'Annual Income (k$)',
       'Spending Score (1-100)']
for i in columns:
    plt.figure()
   bo sns.xplot(data=data, x='Gender', y=data[i])

# Data grouped by Gender
data.groupby(['Gender'])[['Age', 'Annual Income (k$)',
       'Spending Score (1-100)']].mean().style.format("{:.2f}").set_properties(**{'text-align': 'center'})

# Correlation
data.corr(numeric_only=True).style.format("{:.2f}").set_properties(**{'text-align': 'center'})

sns.heatmap(data.corr(numeric_only=True), annot=True, cmap="coolwarm")

# Select relevant features for clustering
# Assuming the dataset has columns like 'Age', 'Annual Income (k$)', 'Spending Score (1-100)'
features = data[['Age', 'Annual Income (k$)', 'Spending Score (1-100)']]

# Preprocess the data
scaler = StandardScaler()
scaled_features = scaler.fit_transform(features)

# Determine the optimal number of clusters using the Elbow method
inertia = []
K_range = range(1, 11)
for k in K_range:
    kmeans = KMeans(n_clusters=k, random_state=42)
    kmeans.fit(scaled_features)
    inertia.append(kmeans.inertia_)

# Plot the Elbow curve
plt.figure(figsize=(8, 5))
plt.plot(K_range, inertia, marker='o', color='blue')
plt.title('Elbow Method')
plt.xlabel('Number of Clusters')
plt.ylabel('Inertia')
plt.show()

# Apply K-means with optimal number of clusters (e.g., k=5 based on the Elbow method)
optimal_k = 5
kmeans = KMeans(n_clusters=optimal_k, random_state=42)
clusters = kmeans.fit_predict(scaled_features)

# Add cluster labels to the original dataset
data['Cluster'] = clusters

# Analyze and visualize the clusters
sns.pairplot(data, hue='Cluster', diag_kind='kde')
plt.show()

# Additional visualization (e.g., income vs. spending score)
plt.figure(figsize=(8, 6))
sns.scatterplot(
    x='Annual Income (k$)', y='Spending Score (1-100)',
    hue='Cluster', data=data, palette='Set2'
)
plt.title('Customer Segmentation')
plt.show()

#Save the clustered data
data.to_csv('clustered_customers.csv', index=False)
print("Clustered data saved to 'clustered_customers.csv'.")