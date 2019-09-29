## Previsor de Evasão Estudantil
Este projeto pretende identificar os estudantes da graduação da Universidade de Brasília com risco de evasão a partir do histórico acadêmico.

### Como usar
A partir de um arquivo `.csv` seguindo o formato explicado na seção [Entrada](#entrada), crie os modelos de entrada executando a linha:

`python3 model_creator.py arquivo.csv`

Serão criados arquivos `.pkl`, que serão usados pelo previsor. Para executar o previsor, execute:

`python3 predict.py`

--------------------------------------------------------------------------------

### Entrada
Cada linha do arquivo CSV de entrada deve seguir o formato a seguir:

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

Dessa forma, um exemplo de linha no arquivo `.csv` é:

| 1234 | 20101 | 20102 |  113034 | "SS" | "FORMADO" |
|------|-------|-------|---------|------|-----------|

#### Observações
+ **O algoritmo utilizará as matérias que estão nos dados de entrada. Recomenda-se usar as matérias obrigatórias dos dois primeiros semestres do curso.**
+ Alunos que vieram a falecer não devem ser usados na entrada.
+ Todos os estudantes devem estar matriculados no mesmo curso de graduação.
