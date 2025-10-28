import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
import pickle

df = pd.read_csv("penguins_raw.csv", usecols=[2, 4, 9, 10, 11, 12, 13])
df['Species'] = df['Species'].str.replace(r"\s*\(.*?\)", "", regex=True)
df.dropna(inplace=True)
output = df['Species']
features = df.iloc[:, 1:]
features = pd.get_dummies(features)
label_codes, label_uniques = pd.factorize(output)
x_train, x_test, y_train, y_test = train_test_split(features, label_codes, train_size = 0.8)
print(label_uniques)

model = RandomForestClassifier()
model.fit(x_train, y_train)
y_pred = model.predict(x_test)

acc = accuracy_score(y_test, y_pred)
with open('rfc_model.pkl', 'wb') as f:
    pickle.dump(model, f)

with open('label_uniques.pkl', 'wb') as f:
    pickle.dump(label_uniques, f)