from sklearn.linear_model import LogisticRegression
from sklearn.neural_network import MLPClassifier
from sklearn import tree
from sklearn.model_selection import train_test_split, cross_validate, GridSearchCV
from sklearn.metrics import confusion_matrix, accuracy_score, precision_score, recall_score

import pandas as pd
import numpy as np
import ignore_warnings

df1 = pd.read_pickle('first_two_semesters_failed_courses_v2.pkl')
df2 = pd.read_pickle('first_two_semesters_grades_v2.pkl')

logreg_param_grid = {
  'solver': ['liblinear', 'lbfgs'],
  'C': np.logspace(-2, 4, 10),
  # 'penalty': ['l1', 'l2']
}

mlpc_param_grid = {
  'solver': ['lbfgs', 'adam'],
  'alpha': np.logspace(-4, 2, 4),
  'activation': ['logistic', 'relu']
}

dtree_param_grid = {
  'criterion': ['gini', 'entropy'],
  'splitter': ['best', 'random'],
  'min_samples_split' : range(10,200,20),
  'max_depth': range(1,15,2)
}

classifiers = [
  ('LogisticRegression', LogisticRegression(max_iter=300), logreg_param_grid),
  ('MLPClassifier', MLPClassifier(max_iter=1000), mlpc_param_grid),
  ('DecisionTreeClassifier', tree.DecisionTreeClassifier(), dtree_param_grid)
]

for x in range(10):
  print('--- iteration', x)
  for index, df in enumerate([df1, df2]):
    print('Model', index+1)
    feature_cols = df.columns.difference(['StatusFinal', 'IdAluno'])
    features = df.loc[:, feature_cols] # we want all rows and the features columns
    labels = df.StatusFinal.replace({'EVADIDO': 1, 'FORMADO': 0})  # our label is StatusFinal
    X_train, X_test, y_train, y_test = train_test_split(
        features, labels, test_size=0.30, stratify=labels, random_state=42)

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

