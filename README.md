# Compilador para a Linguagem Jack

Este repositório contém o desenvolvimento de um compilador para a linguagem **Jack**, como parte da disciplina de Compiladores do curso de Engenharia da Computação.

## Integrantes
- Guilherme Pessoa Lima Diniz

## Linguagem utilizada
- Python 3

## Descrição
Este projeto tem como objetivo a implementação de um analisador léxico (scanner) para a linguagem Jack, conforme especificações do curso nand2tetris.

O analisador será responsável por:
- ler arquivos `.jack`
- identificar os tokens da linguagem
- gerar saída em formato XML compatível com o padrão oficial

## Estrutura do projeto
O projeto está organizado de forma a separar claramente o código-fonte e os arquivos de teste, incluindo os arquivos oficiais do nand2tetris utilizados para validação.
```
Compilador-para-linguagem-jack/
│
├── src/
│   ├── main.py
│   └── test_utils.py
│
├── tests/
│   ├── ArrayTest/
│   │   ├── Main.jack
│   │   ├── MainT.xml
│   │   └── MainT_oficial.xml
│   │
│   ├── ExpressionLessSquare/
│   │   ├── Main.jack
│   │   ├── Square.jack
│   │   ├── SquareGame.jack
│   │   ├── MainT.xml
│   │   ├── MainT_oficial.xml
│   │   ├── SquareT.xml
│   │   ├── SquareT_oficial.xml
│   │   ├── SquareGameT.xml
│   │   └── SquareGameT_oficial.xml
│   │
│   └── Square/
│       ├── Main.jack
│       ├── Square.jack
│       ├── SquareGame.jack
│       ├── MainT.xml
│       ├── MainT_oficial.xml
│       ├── SquareT.xml
│       ├── SquareT_oficial.xml
│       ├── SquareGameT.xml
│       └── SquareGameT_oficial.xml
│
└── README.md
```
### Organização dos testes
Os testes foram organizados em pastas correspondentes aos conjuntos oficiais do Projeto 10 do nand2tetris:

- `ArrayTest`
- `ExpressionLessSquare`
- `Square`

Cada pasta contém:

- Arquivos `.jack`: código-fonte de entrada
- Arquivos `.xml` (sem sufixo): saída gerada pelo analisador léxico
- Arquivos `.xml` com sufixo _oficial: saída oficial fornecida pelo nand2tetris
### Observação importante

Os arquivos com sufixo `_oficial` representam o gabarito oficial e são utilizados para validação do funcionamento do analisador léxico.

Já os arquivos `.xml` sem o sufixo `_oficial` são aqueles gerados pelo programa desenvolvido, devendo ser idênticos aos oficiais para que a implementação seja considerada correta.
## Estado atual
O projeto já realiza:
- leitura de arquivos `.jack`
- geração de saída XML
- tokenização inicial
- classificação de palavras reservadas (`keyword`) e identificadores (`identifier`)
- Identificação de símbolos da linguagem
- Reconhecimento de: `integerConstant` e `stringConstant`
- tratamento de comentários (`//`, `/* */`, `/** */`)
- escape de caracteres especiais para XML (`<`, `>`, `&`)

## Limitações Atuais

- A validação sintática não é realizada (apenas análise léxica)

## Saída
Para cada arquivo `.jack`, o programa gera automaticamente um arquivo `.xml` correspondente com a estrutura inicial de tokens.

## Observações
O projeto será desenvolvido sem o uso de geradores automáticos de analisadores léxicos e sintáticos (Lex, Flex, Yacc), conforme exigência da disciplina.