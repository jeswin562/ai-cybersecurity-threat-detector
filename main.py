import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

# Step 1: Load the dataset
df=pd.read_csv("CICIDS2017_sample.csv")

# Step 2: Preview the data
print("Dataset preview:")
print(df.head())

# Step 3: Select features and label
X=df.drop(columns=["Label"])  # All columns except the label
y=df["Label"]  # The target

# Handle missing and infinite values
X=X.replace([float('inf'),-float('inf')],float('nan'))  # Replace inf with nan
X=X.fillna(0)  # Replace nan with 0 (you can also use mean or drop rows)

# Step 4: Split the data
X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.2)

# Step 5: Train the model
model=RandomForestClassifier()
model.fit(X_train,y_train)


# Step 6: Make predictions
y_pred=model.predict(X_test)

# Step 7: Show results
print("\nModel Results:")
print(classification_report(y_test, y_pred))

#This is to save the model
import joblib
joblib.dump(model,"model.pkl")
