import pandas as pd
import numpy as np

# Load dataset
file_path = '../data/austinHousingData.csv'
df = pd.read_csv(file_path)

# Drop irrelevant columns
irrelevant_columns = [
    'streetAddress', 'description', 'latestPriceSource', 'homeImage', 'hasGarage', 'zpid',
    'city', 'homeType', 'latest_saledate'
]

df.drop(columns=irrelevant_columns, inplace=True, errors='ignore')

# Drop low-importance columns
low_importance_columns = ['numOfAccessibilityFeatures', 'numOfCommunityFeatures', 
                          'hasCooling', 'hasHeating', 'numOfWindowFeatures', 
                          'numOfSecurityFeatures', 'hasView', 'parkingSpaces', 
                          'propertyTaxRate', 'hasSpa', 'numOfWaterfrontFeatures']
df.drop(columns=low_importance_columns, inplace=True)

# Drop columns users aren't likely to have access to
user_unavailable_columns = ['numPriceChanges', 'avgSchoolSize', 'avgSchoolRating', 'avgSchoolDistance',
                                'numOfPhotos', 'latest_saleyear', 'latest_salemonth', 'numOfParkingFeatures',
                                'MedianStudentsPerTeacher', 'numOfElementarySchools', 'numOfHighSchools', 
                                'numOfMiddleSchools', 'numOfPrimarySchools']
df.drop(columns=user_unavailable_columns, inplace=True)

# Drop rows with missing values
df.dropna(inplace=True)

# Save the cleaned dataset for future steps
cleaned_file_path = '../data/austinHousingData_cleaned.csv'
df.to_csv(cleaned_file_path, index=False)
print(f"Cleaned dataset saved at {cleaned_file_path}")
