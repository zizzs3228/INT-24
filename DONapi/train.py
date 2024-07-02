import os
import warnings

import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split

warnings.filterwarnings("ignore")


MODEL_PATH = 'models'




df = pd.read_csv('dataset.csv')

obfuscated_features = ['OF1','OF2', 'OF3', 'OF4', 'OF5', 'OF6', 'OF7', 'OF8', 'OF9', 'OF10', 'OF11',
       'OF12', 'OF13', 'OF14', 'OF15', 'OF16', 'OF17', 'OF18', 'OF19', 'OF20',
       'OF21', 'OF22', 'OF23', 'OF24', 'OF25', 'OF26', 'OF27']
obfuscated_y = ['obfuscated']
behavior_features = ['R1', 'R2', 'R3', 'R4', 'R5', 'R6', 'R7', 'R8', 'UF10',
        'UF1', 'UF2', 'UF3', 'UF4', 'UF5', 'UF6', 'UF7', 'UF8', 'UF9',
        'BF1', 'BF2', 'BF3', 'BF4', 'BF5', 'BF6', 'BF7', 'BF8', 'BF9', 'BF10', 'BF11', 'BF12']
behavior_y = ['malicious behavior']

decision_features = ['obfuscated_predict', 'obfuscated_0_proba', 'obfuscated_1_proba',
                     'behavior_predict', 'behavior_0_proba', 'behavior_1_proba']
decision_y = ['malicious']


X = df[obfuscated_features + behavior_features]
y = df[obfuscated_y + behavior_y + decision_y]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.5, shuffle=True, stratify=y[decision_y])


class_weights = {0: 0.25, 1: 0.75}
obfuscated_model = RandomForestClassifier(class_weight=class_weights)
obfuscated_model.fit(X_train[obfuscated_features], y_train[obfuscated_y])
y_pred = obfuscated_model.predict(X_test[obfuscated_features])
print('_'*50)
print('Obfuscated Model report:')
print(classification_report(y_test[obfuscated_y], y_pred))


class_weights={0: 0.05, 1: 0.95}
behavior_model = RandomForestClassifier(class_weight=class_weights)
behavior_model.fit(X_train[behavior_features], y_train[behavior_y])
y_pred = behavior_model.predict(X_test[behavior_features])
print('_'*50)
print('Behavior Model report:')
print(classification_report(y_test[behavior_y], y_pred))

X_test['obfuscated_predict'] = obfuscated_model.predict(X_test[obfuscated_features])
X_test[['obfuscated_0_proba', 'obfuscated_1_proba']] = obfuscated_model.predict_proba(X_test[obfuscated_features])
X_test['behavior_predict'] = behavior_model.predict(X_test[behavior_features])
X_test[['behavior_0_proba', 'behavior_1_proba']] = behavior_model.predict_proba(X_test[behavior_features])


X = X_test[decision_features]
y = y_test[decision_y]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.5, shuffle=True, stratify=y[decision_y])


class_weights = {0: 0.25, 1: 0.75}
decision_model = RandomForestClassifier(class_weight=class_weights)
decision_model.fit(X_train, y_train)
y_pred = decision_model.predict(X_test)
print('_'*50)
print('Decision Model report:')
print(classification_report(y_test, y_pred))


if not os.path.exists(MODEL_PATH):
    os.makedirs(MODEL_PATH)

obfuscated_model_path = os.path.join(MODEL_PATH, 'obfuscated_model.pkl')
behavior_model_path = os.path.join(MODEL_PATH, 'behavior_model.pkl')
decision_model_path = os.path.join(MODEL_PATH, 'decision_model.pkl')
    
joblib.dump(obfuscated_model, obfuscated_model_path)
joblib.dump(behavior_model, behavior_model_path)
joblib.dump(decision_model, decision_model_path)