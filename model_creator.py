import course_helper
import semester_calculator as SC
import pandas as pd

import sys

def remove_old_courses(dataframe):
  if '1_114014' in dataframe: dataframe.loc[dataframe['1_114014'] != 0, '1_114626'] = dataframe['1_114014']
  if '1_114014' in dataframe: dataframe.loc[dataframe['1_114014'] != 0, '1_114634'] = dataframe['1_114014']
  if '2_114014' in dataframe: dataframe.loc[dataframe['2_114014'] != 0, '2_114626'] = dataframe['2_114014']
  if '2_114014' in dataframe: dataframe.loc[dataframe['2_114014'] != 0, '2_114634'] = dataframe['2_114014']
  dataframe.drop(columns=['1_114014', '2_114014'])

  return dataframe

def transform_dataframe(dataframe, aggfunc, fill_value):
  dataframe['CourseTerm'] = dataframe.Semester.map(str) + '_' + dataframe.CodigoMateria.map(str)
  dataframe = dataframe.drop(columns=['SemestreIngresso', 'SemestreMateria', 'CodigoMateria', 'Semester'])

  dataframe = dataframe.pivot_table(values='Conceito', index=[
                        'IdAluno', 'StatusFinal'], columns='CourseTerm', aggfunc=aggfunc, fill_value=fill_value)
  dataframe.columns.name = None
  dataframe = dataframe.reset_index()
  remove_old_courses(dataframe)

  return dataframe

def failed_workload(row, semester=None):
  failed_workload = 0

  for code, workload in course_helper.COURSE_CODES_WORKLOAD.items():
    if semester == None:
      failed_workload += row['1_' + code] * workload
      failed_workload += row['2_' + code] * workload
    else:
      failed_workload += row[semester + '_' + code] * workload

  return failed_workload


df = pd.read_csv(sys.argv[1])

# calculate semester
df['Semester'] = df.apply(lambda x: SC.calculate(x['SemestreIngresso'], x['SemestreMateria']), axis=1)
df = df[(df.Semester > 0) & (df.Semester <= 2)]

df1 = df.copy()
df2 = df.copy()
df4 = df.copy()

#
# This is the first model I'll be testing and the idea is
# to see how accurate we can get just with the info from
# the first two semesters and the number of  failed courses
# on those semesters
# Data: How many times they failed courses from 1st two semesters
#
print('1st model start')

# discretize course grade

df1.Conceito = df1.Conceito.replace(['SR', 'II', 'MI'], 1)
df1.Conceito = df1.Conceito.replace(['SS', 'MS', 'MM', 'CC', 'DP', 'TR', 'TJ'], 0)

df1 = transform_dataframe(df1, 'sum', 0)
df1.to_pickle('first_two_semesters_failed_courses.pkl')
print('1st model done')

#
# This is the second model, with the same idea that the first
# one but counting only the SR grades on courses.
# Data: How many times had SR grades on the courses first
# two semesters courses
#
print('2nd model start')

df2 = transform_dataframe(df2, 'last', 'NC')

# One hot encoding the grade column
columns = df2.columns.difference(['StatusFinal', 'IdAluno']).tolist()
for column in columns:
  one_hot = pd.get_dummies(df2[column])
  df2 = df2.drop(column,axis = 1)
  one_hot.columns = map(lambda x: column + '_' + x, one_hot.columns)
  df2 = df2.join(one_hot)

df2.to_pickle('first_two_semesters_grades.pkl')
print('2nd model done')

#
# Third model: first model + failed workload
#
print('3rd model start')

# discretize course grade

df3 = df2.copy()

# Failed workload is calculated from the first model (df1)
# df3['Creditos_Reprovados'] = df1.apply(lambda row: failed_workload(row), axis=1)
# df3['Creditos_Reprovados_1'] = df1.apply(lambda row: failed_workload(row, '1'), axis=1)
df3['Creditos_Reprovados_2'] = df1.apply(lambda row: failed_workload(row, '2'), axis=1)
df3.to_pickle('first_two_semesters_grades_workload.pkl')
print('3rd model done')

#
# Fourth model: model for apriori rule association with grades
#

print('4th model start')
df4 = df4.drop(columns=['SemestreIngresso', 'SemestreMateria'])
df4 = df4.applymap(str)

df5 = df4.copy()

df4['TermCourseGrade'] = df4.Semester + '_' + df4.CodigoMateria + '_' + df4.Conceito
df4 = df4.drop(columns=['Conceito', 'CodigoMateria', 'Semester'])

grouped = df4.groupby(['IdAluno', 'StatusFinal'])
df4 = grouped['TermCourseGrade'].apply(lambda x: pd.Series(x.values)).unstack()
df4 = df4.reset_index()

df4 = df4.drop(columns=['IdAluno'])
df4.to_pickle('association_rules_grades.pkl')
print('4th model done')

#
# Fifth model: model for apriori rule association with only approvals and failures
#

print('5th model start')
df5.Conceito = df5.Conceito.replace(['SR', 'II', 'MI', 'TR', 'TJ'], 'RP')
df5.Conceito = df5.Conceito.replace(['SS', 'MS', 'MM', 'CC', 'DP'], 'AP')

df5['TermCourseGrade'] = df5.Semester + '_' + df5.CodigoMateria + '_' + df5.Conceito
df5 = df5.drop(columns=['Conceito', 'CodigoMateria', 'Semester'])

grouped = df5.groupby(['IdAluno', 'StatusFinal'])
df5 = grouped['TermCourseGrade'].apply(lambda x: pd.Series(x.values)).unstack()
df5 = df5.reset_index()

df5 = df5.drop(columns=['IdAluno'])
df5.to_pickle('association_rules_approved_failed.pkl')

print('5th model done')
