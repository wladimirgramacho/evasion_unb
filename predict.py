import pandas as pd
import numpy as np
import ignore_warnings

from sklearn.linear_model import LogisticRegression
from sklearn.neural_network import MLPClassifier
from sklearn import tree
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import accuracy_score, recall_score

df1 = pd.read_pickle('first_two_semesters_failed_courses.pkl')
df2 = pd.read_pickle('first_two_semesters_grades.pkl')
df3 = pd.read_pickle('first_two_semesters_grades_workload.pkl')

logreg_param_grid = {
  'solver': ['liblinear', 'lbfgs'],
  'C': np.logspace(-2, 4, 10),
  # 'penalty': ['l1', 'l2']
}

mlpc_param_grid = {
  'hidden_layer_sizes': [(50,50,50), (50,100,50), (100,)],
  'activation': ['tanh', 'relu'],
  'solver': ['sgd', 'adam'],
  'alpha': [0.0001, 0.05],
  'learning_rate': ['constant','adaptive'],
}

dtree_param_grid = {
  'criterion': ['gini', 'entropy'],
  'splitter': ['best', 'random'],
  'min_samples_split': np.linspace(0.1, 1.0, 10, endpoint=True)
}

rf_param_grid = {
  'criterion': ['gini', 'entropy'],
  'n_estimators': range(10,200,20),
  'max_features': ['auto', 'sqrt']
}

classifiers = [
  ('LogisticRegression', LogisticRegression(max_iter=300), logreg_param_grid),
  # ('MLPClassifier', MLPClassifier(max_iter=100), mlpc_param_grid),
  ('DecisionTreeClassifier', tree.DecisionTreeClassifier(), dtree_param_grid),
  ('RandomForestClassifier', RandomForestClassifier(), rf_param_grid)
]

for index, df in enumerate([df1, df2, df3]):
  feature_cols = df.columns.difference(['StatusFinal', 'IdAluno'])
  features = df.loc[:, feature_cols] # we want all rows and the features columns
  labels = df.StatusFinal.replace({'EVADIDO': 1, 'FORMADO': 0})  # our label is StatusFinal
  test_size = 0.30
  X_train, X_test, y_train, y_test = train_test_split(
      features, labels, test_size=test_size, stratify=labels, random_state=42)

  print('Model', index+1)
  print('Dataset - number of columns:', feature_cols.size)
  print('Dataset - number of rows:', len(features))
  print('Training size:', len(X_train))
  print('Test size:', len(X_test))
  print('\n')


  for classifier in classifiers:
    print(classifier[0])
    grid_search = GridSearchCV(classifier[1], classifier[2], scoring='recall',
                            cv=10, return_train_score=True)
    grid_search.fit(X_train.values, y_train.values)

    y_pred = grid_search.predict(X_test.values)
    print('Best params for recall', grid_search.best_params_)
    print("recall = %0.4f" % recall_score(y_test, y_pred))
    print("accuracy = %0.4f" % accuracy_score(y_test, y_pred))
    # file_name = 'tree' + str(index+1) + '.dot'
    # tree.export_graphviz(grid_search.best_estimator_, max_depth=1, out_file=file_name, feature_names=list(feature_cols), class_names=['FORMADO', 'EVADIDO'], filled=True, label='root', impurity=False)

  print('\n')

