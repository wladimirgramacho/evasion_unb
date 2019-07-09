## Student Evasion Predictor
This project intends to predict if a student from Universidade de Brasília will evade or graduate. This prediction is made from the student's academic record.

--------------------------------------------------------------------------------

### Input

These are the values and the format for the inputs:

| IdAluno | SemestreIngresso | SemestreMateria |  CodigoMateria | Conceito | StatusFinal |
|---------|------------------|-----------------|----------------|----------|-------------|

+ **IdAluno** (*integer*): this is just an id for the student and must correspond to the student's registration number
+ **SemestreIngresso** (*integer*): the semester where the student enrolled in the graduation course. It must follow the format `AAAAS`, where `A` is a year digit and `S` is the semester.
+ **SemestreMateria** (*integer*) the semester where the student enrolled in the course. It must follow the format `AAAAS`, where `A` is a year digit and `S` is the semester.
+ **CodigoMateria** (*string*): the code for the course. Check the course codes at [Matricula Web](https://matriculaweb.unb.br/).
+ **Conceito** (*string*): the grade for the course.
+ **StatusFinal** (*string*): the status for the student. The values for this field shall be one of the following:
  + If graduated => `FORMATURA`
  + If evaded => `EVADIDO`
  + If still active => `ATIVO`

*Obs.: students who have passed away should not be used as input.*

All the students used as input shall be enrolled in the same course. Here is an example of row for input:

| 1234 | 20101 | 20102 |  "113034" | "SS" | "FORMATURA" |
|------|-------|-------|-----------|------|-------------|
