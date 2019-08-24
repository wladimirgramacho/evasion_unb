## Previsor de Evasão Estudantil
Este projeto pretende identificar se um estudante da Universidade de Brasília irá evadir ou formar a partir do histórico do estudante nas matérias cursadas.

### Como usar
A partir de um arquivo `.csv` seguindo o formato explicado na seção [Entrada](#entrada), crie os modelos de entrada executando a linha:

`python3 model_creator.py arquivo.csv`

Serão criados arquivos `.pkl`, que serão usados pelo previsor. Para executar o previsor, execute:

`python3 predict.py`

--------------------------------------------------------------------------------

### Entrada

| IdAluno | SemestreIngresso | SemestreMateria |  CodigoMateria | Conceito | StatusFinal |
|---------|------------------|-----------------|----------------|----------|-------------|

+ **IdAluno** (*inteiro*): identificador único de um aluno
+ **SemestreIngresso** (*inteiro*): o semestre de ingresso do aluno no curso de graduação. Esse campo deve seguir o formato `AAAAS`, onde `A` é um dígito do ano e `S` é o semestre, e.g. '20101' para um aluno que ingressou no 1º semestre de 2010.
+ **SemestreMateria** (*inteiro*): o semestre no qual o aluno cursou determinada matéria. Esse campo deve seguir o formato `AAAAS`, onde `A` é um dígito do ano e `S` é o semestre.
+ **CodigoMateria** (*inteiro*): o código da matéria. Verifique os códigos das matérias no [Matrícula Web](https://matriculaweb.unb.br/).
+ **Conceito** (*string*): menção do aluno naquela matéria no semestre.
+ **StatusFinal** (*string*): o status do aluno ao final do curso. Os possíveis valores para este campo devem ser:
  + Se formado => `FORMADO`
  + Se evadido => `EVADIDO`
  + Se ainda está ativo => `ATIVO`

*Obs.: alunos que vieram a falecer não devem ser usados na entrada.*

Para melhores resultados, todos os estudantes devem estar matriculados no mesmo curso. Dessa forma, abaixo temos um exemplo de linha no arquivo `.csv`:

| 1234 | 20101 | 20102 |  113034 | "SS" | "FORMADO" |
|------|-------|-------|---------|------|-----------|
