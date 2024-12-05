import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import skew

# Load cleaned dataset
file_path = '../data/austinHousingData_cleaned.csv'
df = pd.read_csv(file_path)

# Summary statistics
print("Summary Statistics:")
print(df.describe())

# Check for missing values
print("\nMissing Values:")
print(df.isnull().sum())

# Check for skewness
print("\nSkewness of Numerical Features:")
numerical_features = df.select_dtypes(include=['float64', 'int64']).columns
skewness = df[numerical_features].apply(lambda x: skew(x.dropna())).sort_values(ascending=False)
print(skewness)

# Heatmap of correlations
plt.figure(figsize=(12, 8))
correlation_matrix = df.corr()
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f", linewidths=0.5)
plt.title("Correlation Matrix")
plt.show()

# Feature importance using a simple Random Forest
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

target = 'latestPrice' 
X = df.drop(columns=[target])
y = df[target]

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train Random Forest for feature importance
rf = RandomForestRegressor(random_state=42, n_estimators=100)
rf.fit(X_train, y_train)

# Feature importance
feature_importances = pd.DataFrame({
    'Feature': X.columns,
    'Importance': rf.feature_importances_
}).sort_values(by='Importance', ascending=False)

print("\nFeature Importances:")
print(feature_importances)

# Plot feature importance
plt.figure(figsize=(12, 6))
sns.barplot(data=feature_importances, x='Importance', y='Feature')
plt.title("Feature Importance")
plt.xlabel("Importance")
plt.ylabel("Feature")
plt.tight_layout()
plt.show()
