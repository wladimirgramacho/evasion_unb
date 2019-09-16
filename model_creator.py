import course_helper
import semester_calculator as SC
import pandas as pd

import sys

def transform_dataframe(dataframe, aggfunc, fill_value):
  dataframe['CourseTerm'] = dataframe.Semester.map(str) + '_' + dataframe.CodigoMateria.map(str)
  dataframe = dataframe.drop(columns=['SemestreIngresso', 'SemestreMateria', 'CodigoMateria', 'Semester'])

  dataframe = dataframe.pivot_table(values='Conceito', index=[
                        'IdAluno', 'StatusFinal'], columns='CourseTerm', aggfunc=aggfunc, fill_value=fill_value)
  dataframe.columns.name = None
  dataframe = dataframe.reset_index()
  if '1_114014' in dataframe: dataframe.loc[dataframe['1_114014'] != 0, '1_114626'] = dataframe['1_114014']
  if '1_114014' in dataframe: dataframe.loc[dataframe['1_114014'] != 0, '1_114634'] = dataframe['1_114014']
  if '2_114014' in dataframe: dataframe.loc[dataframe['2_114014'] != 0, '2_114626'] = dataframe['2_114014']
  if '2_114014' in dataframe: dataframe.loc[dataframe['2_114014'] != 0, '2_114634'] = dataframe['2_114014']
  dataframe.drop(columns=['1_114014', '2_114014'])

  return dataframe


df = pd.read_csv(sys.argv[1])

# calculate semester
df['Semester'] = df.apply(lambda x: SC.calculate(x['SemestreIngresso'], x['SemestreMateria']), axis=1)
df = df[(df.Semester > 0) & (df.Semester <= 2)]

# filter for courses of two first semesters
df = df[df.CodigoMateria.isin(course_helper.COURSE_CODES.values())]

df1 = df.copy()
df2 = df.copy()

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
df1.to_pickle('first_two_semesters_failed_courses_v2.pkl')
print('1st model done')

#
# This is the second model, with the same idea that the first
# one but counting only the SR grades on courses.
# Data: How many times had SR grades on the courses first
# two semesters courses
#
print('2nd model start')

df2 = transform_dataframe(df2, 'last', 'NC')
df2.drop(columns=['1_114014', '2_114014'])

# One hot encoding the grade column
columns = df2.columns.difference(['StatusFinal', 'IdAluno']).tolist()
for column in columns:
  one_hot = pd.get_dummies(df2[column])
  df2 = df2.drop(column,axis = 1)
  one_hot.columns = map(lambda x: column + '_' + x, one_hot.columns)
  df2 = df2.join(one_hot)

import pdb; pdb.set_trace()
df2.to_pickle('first_two_semesters_grades_v2.pkl')
print('2nd model done')
