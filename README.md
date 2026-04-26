# Compilador para a Linguagem Jack

Este repositório contém o desenvolvimento de um compilador para a linguagem **Jack**, como parte da disciplina de Compiladores do curso de Engenharia da Computação.

## Integrantes
- Guilherme Pessoa Lima Diniz
- Matrícula: 20260001310

## Linguagem utilizada
- Python 3

## Descrição
O projeto implementa:

- **Analisador Léxico (Scanner)**  
- **Analisador Sintático (Parser)**  

para a linguagem Jack, conforme especificações do curso **nand2tetris**.

O compilador:

- lê arquivos `.jack`
- identifica tokens da linguagem
- valida a estrutura sintática
- gera saída XML compatível com o padrão oficial

## Estrutura do projeto
O projeto está organizado de forma a separar claramente o código-fonte e os arquivos de teste, incluindo os arquivos oficiais do nand2tetris utilizados para validação.
```
Compilador-para-linguagem-jack/
│
├── src/
│   ├── main.py
│   ├── tokenizer.py
│   ├── parser.py
│   ├── test_runner.py
│   └── parser_test_runner.py
│
├── tests/
│   ├── ArrayTest/
│   ├── ExpressionLessSquare/
│   └── Square/
│
└── README.md
```
### Organização dos testes
Os testes foram organizados em pastas correspondentes aos conjuntos oficiais do Projeto 10 do nand2tetris:

- `ArrayTest`
- `ExpressionLessSquare`
- `Square`


Cada pasta contém:

- Arquivos `.jack`: código de entrada  
- Arquivos `.xml`: saída gerada pelo programa  
- Arquivos `_oficial.xml`: gabarito oficial  

### Observação importante

Os arquivos com sufixo `_oficial` representam o resultado esperado.

Os arquivos gerados pelo programa devem ser **estruturalmente idênticos** aos oficiais.

## Funcionamento interno

### Tokenizer (scanner)

Responsável por:

- remoção de comentários → `remove_comments()`
- tokenização → `basic_tokenize()`
- classificação de tokens → `classify_token()`
- escape XML → `escape_xml()`
- geração XML léxico → `tokens_to_xml()`

### Parser (analisador sintático)

Implementado com **Recursive Descent Parsing**.

Principais métodos:

- `compile_class`
- `compile_class_var_dec`
- `compile_subroutine_dec`
- `compile_parameter_list`
- `compile_subroutine_body`
- `compile_var_dec`
- `compile_statements`
- `compile_let`
- `compile_if`
- `compile_while`
- `compile_do`
- `compile_return`
- `compile_expression`
- `compile_term`
- `compile_expression_list`

## Execução do compilador

### Comando:

```
python src/main.py caminho/para/arquivo.jack
```

### Exemplo:

```
python src/main.py tests/ArrayTest/Main.jack
```

## Saída

O parser gera arquivos com sufixo:

```
P.xml
```

Exemplo:

```
Main.jack → MainP.xml
```

## Validação do Parser

### Executar testes:

```
python src/parser_test_runner.py
```

### Resultado esperado:

```
[OK] tests/ArrayTest/MainP.xml
[OK] tests/ExpressionLessSquare/MainP.xml
[OK] tests/Square/MainP.xml

Resumo:
  7/7 testes passaram
  Parser validado com sucesso
```
## Validação do Scanner

```
python src/test_runner.py
```

## Estratégia de validação

Foi utilizada:

- comparação automática de arquivos XML
- normalização de indentação (remoção de espaços à esquerda)
- validação estrutural da hierarquia de tags


## Limitações

- Não há geração de código VM
- Não há análise semântica
- O parser assume entrada válida conforme a gramática


## Decisão técnica relevante

O parser foi implementado utilizando **Recursive Descent Parsing**, com uma função para cada não-terminal da gramática Jack.

Essa abordagem:

- facilita manutenção
- melhora legibilidade
- segue o modelo teórico apresentado em aula


## Status do projeto

| Item | Status |
|------|--------|
| Scanner | OK |
| Parser | OK |
| Integração | OK |
| Validação oficial | OK |
| Testes automatizados | OK |

## Relato da atividade

Durante o desenvolvimento, os principais desafios foram:

- compreender e implementar corretamente a gramática da linguagem Jack
- estruturar o parser utilizando recursive descent parsing
- tratar corretamente expressões e chamadas de subrotinas
- garantir que a saída XML estivesse exatamente no formato esperado
- lidar com diferenças de indentação na comparação dos arquivos

A utilização de testes automatizados com normalização de XML foi fundamental para validar o funcionamento do parser e evitar erros sutis na estrutura da saída.

## Conclusão

O projeto atende integralmente aos requisitos da atividade:

- implementação completa do scanner
- implementação completa do parser
- integração funcional entre os módulos
- validação com arquivos oficiais
- testes automatizados
