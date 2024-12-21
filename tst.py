import pickle
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder

# Load the dataset (replace with your dataset path or URL)
dataset_url = "insurance.csv"  # Update to your actual file path
df = pd.read_csv(dataset_url)

# Preprocess data (same as training)
X = df.drop(columns=['expenses'])
y = df['expenses']

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Apply the same preprocessing to the test data
preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), ['age', 'bmi', 'children']),
        ('cat', OneHotEncoder(), ['sex', 'smoker', 'region'])
    ]
)

# Fit the preprocessor on the training data and transform both training and test data
X_train_processed = preprocessor.fit_transform(X_train)
X_test_processed = preprocessor.transform(X_test)

# Load the pre-trained model
with open('xgb_model.pkl', 'rb') as f:
    model = pickle.load(f)

# Make predictions on the test data
predictions = model.predict(X_test_processed)

# Calculate evaluation metrics
mse = mean_squared_error(y_test, predictions)
r2 = r2_score(y_test, predictions)

# Output the results
print(f"MSE: {mse}")
print(f"R² Score: {r2}")
