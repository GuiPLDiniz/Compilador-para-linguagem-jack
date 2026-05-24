# Compilador para a Linguagem Jack

Este repositório contém o desenvolvimento de um compilador para a linguagem **Jack**, como parte da disciplina de Compiladores do curso de Engenharia da Computação.

O projeto foi desenvolvido seguindo a arquitetura proposta pelo curso **nand2tetris**, evoluindo progressivamente pelas etapas de:

- Análise Léxica (Scanner)
- Análise Sintática (Parser)
- Geração de Código Intermediário (VM)

## Integrantes

- Guilherme Pessoa Lima Diniz
- Matrícula: 20260001310

## Linguagem utilizada

- Python 3

## Descrição

O compilador implementa:

- **Scanner (Analisador Léxico)**
- **Parser (Analisador Sintático)**
- **Gerador de Código VM (Compilation Engine)**
- **Tabela de Símbolos (Symbol Table)**
- **Escritor de Código VM (VMWriter)**

O compilador é capaz de:

- ler arquivos `.jack`
- ler diretórios contendo múltiplos arquivos `.jack`
- realizar compilação em lote
- identificar tokens da linguagem Jack
- validar a estrutura sintática
- gerar código intermediário `.vm`
- gerar arquivos compatíveis com o **VM Emulator oficial do nand2tetris**

## Estrutura do projeto

```
Compilador-para-linguagem-jack/
│
├── src/
│   ├── main.py
│   ├── tokenizer.py
│   ├── parser.py
│   ├── compilation_engine.py
│   ├── symbol_table.py
│   ├── vm_writer.py
│   ├── test_runner.py
│   ├── parser_test_runner.py
│   ├── vm_test_runner.py
│
├── tests/
│   ├── ArrayTest/
│   ├── ExpressionLessSquare/
│   ├── Square/
│   │
│   └── Project11/
│       ├── Seven/
│       ├── Average/
│       ├── ConvertToBin/
│       ├── ComplexArrays/
│       ├── Square/
│       └── Pong/
│
└── README.md
```

## Funcionamento interno

### Tokenizer (Scanner)

Responsável por:

- remoção de comentários → `remove_comments()`
- tokenização → `basic_tokenize()`
- classificação de tokens → `classify_token()`
- escape XML → `escape_xml()`
- geração XML léxico → `tokens_to_xml()`

### Parser

Implementado utilizando:

**Recursive Descent Parsing**

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

### Compilation Engine

Responsável pela geração do código intermediário VM.

Construções suportadas:

- variáveis locais
- argumentos
- campos (`field`)
- variáveis estáticas (`static`)
- expressões aritméticas
- expressões relacionais
- operadores unários
- strings
- arrays
- chamadas de função
- chamadas de método
- construtores
- `this`
- `true`
- `false`
- `null`
- `if`
- `while`
- `let`
- `do`
- `return`

### Symbol Table

Responsável pelo gerenciamento de:

- escopo de classe
- escopo de subrotina
- índices de variáveis
- resolução de identificadores

Tipos suportados:

- `static`
- `field`
- `arg`
- `var`

### VM Writer

Responsável pela emissão de comandos VM:

Exemplos:

```
push constant 5
pop local 0
add
call Math.multiply 2
return
```

## Execução do compilador

### Compilar arquivo único

```
python src/main.py caminho/arquivo.jack
```

Exemplo:

```
python src/main.py tests/Project11/Seven/Main.jack
```

### Compilar diretório inteiro

```
python src/main.py caminho/diretorio
```

Exemplo:

```
python src/main.py tests/Project11/Pong
```

O compilador localiza automaticamente todos os arquivos `.jack`, inclusive em subdiretórios.

## Saída gerada

Para cada arquivo:

```
Main.jack
```

é gerado:

```
Main.vm
```

Exemplo:

```
Square.jack → Square.vm
```

## Validação do Scanner

```
python src/test_runner.py
```

## Validação do Parser

```
python src/parser_test_runner.py
```

## Validação do Gerador VM

```
python src/vm_test_runner.py
```

## Estratégia de validação

Foram utilizados:

- testes automatizados
- comparação estrutural XML
- compilação automática de diretórios
- execução no VM Emulator oficial
- validação incremental do Project 11

## Programas validados (Project 11)

### Seven

Validação:

- expressões aritméticas
- operações básicas
- retorno

Status:

OK

---

### Average

Validação:

- arrays
- laços
- entrada e saída
- acumulação

Status:

OK

---

### ConvertToBin

Validação:

- operações bit a bit
- memória RAM
- manipulação binária

Status:

OK

---

### ComplexArrays

Validação:

- arrays complexos
- ponteiros
- referências
- expressões aninhadas

Status:

OK

---

### Square

Validação:

- objetos
- métodos
- construtores
- interação gráfica
- teclado

Status:

OK

---

### Pong

Validação:

- múltiplas classes
- objetos
- colisões
- interação gráfica
- execução completa

Status:

OK

## Decisão técnica relevante

O projeto utiliza **Recursive Descent Parsing**.

A estratégia implementada consiste em:

- uma função para cada não-terminal da gramática Jack
- consumo progressivo de tokens
- reutilização da estrutura do parser sintático para a geração VM

Arquitetura final:

```
Jack
 ↓
Tokenizer
 ↓
Compilation Engine
 ↓
Symbol Table
 ↓
VM Writer
 ↓
Código VM
 ↓
VM Emulator
```

Essa abordagem:

- melhora legibilidade
- facilita manutenção
- reduz acoplamento
- favorece testes incrementais

## Relato da atividade

Principais desafios enfrentados:

- implementação da gramática Jack
- integração entre scanner, parser e geração VM
- gerenciamento de escopo de variáveis
- implementação de arrays
- implementação de chamadas de método
- tratamento correto de `this`
- geração de rótulos únicos
- manipulação de memória
- validação incremental no VM Emulator

A utilização de testes automatizados e dos programas oficiais do Project 11 foi fundamental para garantir a robustez da implementação.

## Status do projeto

| Item | Status |
|-------|--------|
| Scanner | OK |
| Parser | OK |
| Symbol Table | OK |
| VM Writer | OK |
| Compilation Engine | OK |
| Compilação por diretório | OK |
| Geração VM | OK |
| Testes automatizados | OK |
| Project 11 | OK |

## Conclusão

O projeto atende integralmente aos requisitos propostos:

- implementação completa do scanner
- implementação completa do parser
- implementação do gerador de código intermediário VM
- compilação de arquivos individuais
- compilação em lote de diretórios
- integração funcional entre os módulos
- validação utilizando os programas oficiais do nand2tetris
- testes automatizados
- compatibilidade com o VM Emulator oficial

O compilador desenvolvido realiza corretamente a tradução da linguagem Jack para código VM, concluindo a implementação proposta para a disciplina.