import pandas as pd
from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
import pickle

dataset_url = "insurance.csv" 
df = pd.read_csv(dataset_url)
X = df.drop(columns=['expenses'])  
y = df['expenses']
categorical_features = ['sex', 'smoker', 'region']
numerical_features = ['age', 'bmi', 'children']
preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), numerical_features),
        ('cat', OneHotEncoder(drop='first'), categorical_features)
    ]
)
X_preprocessed = preprocessor.fit_transform(X)
with open('preprocessor.pkl', 'wb') as preprocessor_file:
    pickle.dump(preprocessor, preprocessor_file)
X_train, X_test, y_train, y_test = train_test_split(X_preprocessed, y, test_size=0.2, random_state=42)
model = XGBRegressor(random_state=42)
model.fit(X_train, y_train)
with open('xgb_model.pkl', 'wb') as model_file:
    pickle.dump(model, model_file)
print("Training complete. Model and preprocessor saved.")
