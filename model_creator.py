import course_helper
import semester_calculator as SC
import pandas as pd

import sys

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

df1['CourseTerm'] = df1.Semester.map(str) + '_' + df1.CodigoMateria.map(str)

# remove unnecessary columns
df1 = df1.drop(columns=['SemestreIngresso', 'SemestreMateria', 'CodigoMateria', 'Semester'])

df1 = df1.pivot_table(values='Conceito', index=[
                      'IdAluno', 'StatusFinal'], columns='CourseTerm', aggfunc='sum', fill_value=0)
df1.columns.name = None
df1 = df1.reset_index()
df1.loc[df1['1_114014'] != 0, '1_114626'] = df1['1_114014']
df1.loc[df1['1_114014'] != 0, '1_114634'] = df1['1_114014']
df1.loc[df1['2_114014'] != 0, '2_114626'] = df1['2_114014']
df1.loc[df1['2_114014'] != 0, '2_114634'] = df1['2_114014']
df1.drop(columns=['1_114014', '2_114014'])
df1.to_pickle('first_two_semesters_failed_courses_v2.pkl')
print('1st model done')

#
# This is the second model, with the same idea that the first
# one but counting only the SR grades on courses.
# Data: How many times had SR grades on the courses first
# two semesters courses
#
print('2nd model start')
df2['CourseTerm'] = df2.Semester.map(str) + '_' + df2.CodigoMateria.map(str)
# remove unnecessary columns
df2 = df2.drop(columns=['SemestreIngresso', 'SemestreMateria', 'CodigoMateria', 'Semester'])

df2 = df2.pivot_table(values='Conceito', index=[
                      'IdAluno', 'StatusFinal'], columns='CourseTerm', aggfunc='last', fill_value='NC')
df2.columns.name = None
df2 = df2.reset_index()
if '1_114014' in df2: df2.loc[df2['1_114014'] != -1, '1_114626'] = df2['1_114014']
if '1_114014' in df2: df2.loc[df2['1_114014'] != -1, '1_114634'] = df2['1_114014']
if '2_114014' in df2: df2.loc[df2['2_114014'] != -1, '2_114626'] = df2['2_114014']
if '2_114014' in df2: df2.loc[df2['2_114014'] != -1, '2_114634'] = df2['2_114014']
df2.drop(columns=['1_114014', '2_114014'])

# One hot encoding the grade column
columns = df2.columns.difference(['StatusFinal', 'IdAluno']).tolist()
for column in columns:
  one_hot = pd.get_dummies(df2[column])
  df2 = df2.drop(column,axis = 1)
  one_hot.columns = map(lambda x: column + '_' + x, one_hot.columns)
  df2 = df2.join(one_hot)

df2.to_pickle('first_two_semesters_grades_v2.pkl')
print('2nd model done')
