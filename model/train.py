import pandas as pd
import numpy as np
import lightgbm as lgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import joblib

# Load dataset
def load_data(filepath):
    df = pd.read_csv(filepath)
    return preprocess_data(df)

# Preprocess data
def preprocess_data(df):
    df['latest_saledate'] = pd.to_datetime(df['latest_saledate'])
    df['sale_year'] = df['latest_saledate'].dt.year
    df['sale_month'] = df['latest_saledate'].dt.month
    df['sale_day'] = df['latest_saledate'].dt.day
    df.drop(columns=['latest_saledate'], inplace=True)

    irrelevant_columns = ['streetAddress', 'description', 'latestPriceSource', 'homeImage', 'hasGarage',
                          'sale_year', 'sale_month', 'city', 'homeType', 'zpid']
    df.drop(columns=irrelevant_columns, inplace=True)

    user_unavailable_columns = ['numPriceChanges', 'avgSchoolSize', 'avgSchoolRating', 'avgSchoolDistance',
                                'numOfPhotos', 'latest_saleyear', 'latest_salemonth', 'sale_day',
                                'MedianStudentsPerTeacher', 'numOfElementarySchools', 'numOfHighSchools', 
                                'numOfMiddleSchools', 'numOfPrimarySchools']
    df.drop(columns=user_unavailable_columns, inplace=True)

    low_importance_columns = ['numOfAccessibilityFeatures', 'numOfCommunityFeatures', 'hasCooling',
                              'hasHeating', 'numOfWindowFeatures', 'numOfSecurityFeatures', 'hasView',
                              'parkingSpaces', 'propertyTaxRate', 'hasSpa', 'numOfWaterfrontFeatures']
    df.drop(columns=low_importance_columns, inplace=True)

    # Add feature interactions
    df['PricePerSqFt'] = df['latestPrice'] / df['livingAreaSqFt']
    df['BathBedRatio'] = df['numOfBathrooms'] / df['numOfBedrooms']
    df['LotLivingRatio'] = df['lotSizeSqFt'] / df['livingAreaSqFt']
    df['GarageBedRatio'] = df['garageSpaces'] / df['numOfBedrooms']
    df['LatLonInteraction'] = df['latitude'] * df['longitude']

    df.replace([np.inf, -np.inf], np.nan, inplace=True)
    df.fillna(0, inplace=True)

    return df

# Train model
def train_model(X, y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    train_data = lgb.Dataset(X_train, label=y_train)
    test_data = lgb.Dataset(X_test, label=y_test, reference=train_data)

    params = {
        'objective': 'regression',
        'metric': 'rmse',
        'boosting_type': 'gbdt',
        'learning_rate': 0.058793153916846676,
        'num_leaves': 63,
        'max_depth': 16,
        'min_data_in_leaf': 11,
        'feature_fraction': 0.8957209852243492,
        'bagging_fraction': 0.8868935737344777,
        'bagging_freq': 7,
        'lambda_l1': 0.5825558284248297,
        'lambda_l2': 0.005388605992909206,
        'verbosity': -1
    }

    print("Training LightGBM...")
    model = lgb.train(
        params,
        train_data,
        num_boost_round=1000,
        valid_sets=[train_data, test_data],
        callbacks=[lgb.early_stopping(stopping_rounds=50), lgb.log_evaluation(50)]
    )

    # Evaluate model
    y_pred = model.predict(X_test, num_iteration=model.best_iteration)
    rmse = mean_squared_error(y_test, y_pred, squared=False)
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    print(f"LightGBM RMSE: {rmse}")
    print(f"LightGBM MAE: {mae}")
    print(f"LightGBM R^2: {r2}")

    return model

# Save the model
def save_model(model, filename):
    joblib.dump(model, filename)
    print(f"Model saved as {filename}")

if __name__ == "__main__":
    filepath = 'data/austinHousingData.csv'
    df = load_data(filepath)
    target = 'latestPrice'
    X = df.drop(columns=[target])
    y = df[target]

    model = train_model(X, y)
    save_model(model, "lightgbm_model.pkl")
