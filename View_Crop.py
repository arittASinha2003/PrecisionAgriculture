# import pandas as pd
# from sklearn.ensemble import RandomForestClassifier
# from sklearn.model_selection import train_test_split
# from sklearn.metrics import accuracy_score
import pickle

# # Load the crop recommendation dataset
# crop_data = pd.read_csv('path_to_your_crop_recommendation_data.csv')  # Replace with correct path

# # Features (N, P, K, temperature, humidity, ph, rainfall)
# X = crop_data[['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']]

# # Target (crop label)
# y = crop_data['label']

# # Train-test split
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# # Initialize and train the RandomForest model
# model = RandomForestClassifier(n_estimators=100, random_state=42)
# model.fit(X_train, y_train)

# # Evaluate the model
# y_pred = model.predict(X_test)
# print(f"Accuracy: {accuracy_score(y_test, y_pred):.4f}")

# # Save the trained model to 'models/RandomForest_v2.pkl'
# with open('models/RandomForest_v2.pkl', 'wb') as f:
#     pickle.dump(model, f)

with open('models/RandomForest_v2.pkl', 'rb') as f:
    model = pickle.load(f)
    print(model)
