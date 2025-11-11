import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix

df = pd.read_csv("data/clean/collisions_clean.csv")

df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

print(df.head())
print(df.info())
fig, axes = plt.subplots(1, 2, figsize=(16, 6)) 

# Collisions per year
sns.countplot(data=df, x='year', ax=axes[0])
axes[0].set_title("Collisions per Year")
axes[0].set_xlabel("Year")
axes[0].set_ylabel("Count")

# Accident severity distribution
sns.countplot(data=df, x='accident_severity', ax=axes[1])
axes[1].set_title("Accident Severity")
axes[1].set_xlabel("Severity")
axes[1].set_ylabel("Count")


plt.tight_layout()
plt.show()

df['datetime'] = pd.to_datetime(df['datetime'])
df['hour'] = df['datetime'].dt.hour
df['is_weekend'] = df['day_of_week'].isin([5,6]).astype(int)

# Plot weekend vs weekday crashes
plt.figure(figsize=(6,5))
sns.countplot(data=df, x='is_weekend', hue='accident_severity', palette='Set2')
plt.xticks([0,1], ['Weekday', 'Weekend'])
plt.title("Number of Crashes: Weekday vs Weekend")
plt.xlabel("Day Type")
plt.ylabel("Number of Crashes")
plt.legend(title='Accident Severity')
plt.show()

X = df[['hour','road_type','urban_or_rural_area','junction_control']]
y = df['accident_severity']

# One-hot encode categorical features
X = pd.get_dummies(X, drop_first=True)

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# -----------------------------
# Random Forest Model Training and Evaluation
# -----------------------------

# Create a Random Forest classifier with 100 trees, a fixed random seed for reproducibility,
# and balanced class weights to handle class imbalance (e.g., Fatal accidents are rare)
rf = RandomForestClassifier(n_estimators=100, random_state=42, class_weight='balanced')

# Train the Random Forest model on the training data
rf.fit(X_train, y_train)

# Use the trained model to make predictions on the test set
y_pred = rf.predict(X_test)

# Print a detailed classification report showing precision, recall, F1-score for each class
print("Classification Report:")
print(classification_report(y_test, y_pred, digits=3))

# Compute the confusion matrix to see the number of correct and incorrect predictions per class
labels = ['Slight', 'Serious', 'Fatal']
cm = confusion_matrix(y_test, y_pred, labels=labels)

# Visualize the confusion matrix as a heatmap
# Rows = actual labels, Columns = predicted labels
# Diagonal values = correct predictions, off-diagonal = misclassifications
plt.figure(figsize=(6,5))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=labels, yticklabels=labels)
plt.title("Confusion Matrix")
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.show()