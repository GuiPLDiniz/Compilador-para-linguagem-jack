# Compilador para a Linguagem Jack

Este repositório contém o desenvolvimento de um compilador para a linguagem **Jack**, como parte da disciplina de Compiladores do curso de Engenharia da Computação.

## Integrantes
- Guilherme Pessoa Lima Diniz

## Linguagem utilizada
- Python 3

## Descrição
Este projeto tem como objetivo a implementação de um analisador léxico (scanner) para a linguagem Jack, conforme especificações do curso nand2tetris.

O analisador é responsável por:
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
│   └── test_runner.py
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
- Arquivos `.xml` com sufixo `_oficial`: saída oficial fornecida pelo nand2tetris
### Observação importante

Os arquivos com sufixo `_oficial` representam o gabarito oficial e são utilizados para validação do funcionamento do analisador léxico.

Já os arquivos `.xml` sem o sufixo `_oficial` são aqueles gerados pelo programa desenvolvido, devendo ser idênticos aos oficiais para que a implementação seja considerada correta.
## Estado atual
O projeto já realiza:
- leitura de arquivos `.jack`
- geração de saída XML
- tokenização completa
- classificação de palavras reservadas (`keyword`) e identificadores (`identifier`)
- identificação de símbolos da linguagem
- reconhecimento de: `integerConstant` e `stringConstant`
- tratamento de comentários (`//`, `/* */`, `/** */`)
- escape de caracteres especiais para XML (`<`, `>`, `&`, `"`)

## Limitações Atuais

- O projeto realiza apenas análise léxica, não contemplando validação sintática (parser)

## Saída
Para cada arquivo `.jack`, o programa gera automaticamente um arquivo `.xml` correspondente com a estrutura de tokens em formato XML.

## Observações
O projeto foi desenvolvido sem o uso de geradores automáticos de analisadores léxicos e sintáticos (Lex, Flex, Yacc), conforme exigência da disciplina.

## Organização interna do código

Neste projeto, toda a lógica do analisador léxico foi implementada no arquivo:
```
src/main.py
```
Diferentemente de uma arquitetura modular, em que scanner, tokens e geração de saída são separados em arquivos distintos, optou-se por uma implementação centralizada para simplificar o desenvolvimento inicial.

Apesar de estar concentrado em um único arquivo, o código está organizado logicamente em etapas bem definidas, cada uma associada às seguintes funções:

- leitura do arquivo `.jack` e validação do caminho informado
    → função responsável: `main()`
- remoção de comentários de linha e de bloco
    → função responsável: `remove_comments()`
- classificação dos tokens em `keyword`, `integerConstant` e `identifier`
    → função responsável: `classify_token()`
- tokenização do conteúdo, com tratamento de `stringConstant`, símbolos, espaços e palavras
    → função responsável: `basic_tokenize()`
- escape de caracteres especiais exigidos pelo XML (`<`, `>`, `&`, ")
    → função responsável: `escape_xml()`
- geração da saída final no formato XML
    → função responsável: `tokens_to_xml()`
- gravação do arquivo XML de saída
    → função responsável: `main()`

Essa organização mantém a separação conceitual das responsabilidades, ainda que fisicamente estejam no mesmo arquivo.


## Instruções para utilização do analisador léxico
O programa recebe como entrada um arquivo `.jack` e gera um arquivo `.xml` com os tokens reconhecidos.

### Execução

No terminal, a partir da raiz do projeto:

```
python src/main.py caminho/para/arquivo.jack

```
### Exemplo

```
python src/main.py tests/ArrayTest/Main.jack

```

### Saída

Será gerado automaticamente um arquivo no mesmo diretório do arquivo de entrada, com o sufixo `T.xml`

### Exemplo

```
Main.jack → MainT.xml

```
### Como validar os testes

O projeto possui um script para validar automaticamente os arquivos XML gerados, comparando-os com os arquivos oficiais do nand2tetris.

Antes de executar o script de testes, é necessário gerar previamente os arquivos `.xml` correspondentes a partir dos arquivos `.jack`, pois o `test_runner.py` apenas realiza a comparação entre os arquivos gerados e os arquivos oficiais.

### Execução dos testes

```
python src/test_runner.py
```

### Resultado esperado

Se todos os arquivos estiverem corretos, a saída será semelhante a:
```
[OK] Arquivos idênticos: MainT.xml
[OK] Arquivos idênticos: SquareT.xml
[OK] Arquivos idênticos: SquareGameT.xml

Resumo:
  Testes aprovados: 7/7
  Todos os arquivos estão idênticos aos oficiais.
```
Caso haja divergência, o programa indicará a linha onde ocorreu a diferença.

### Como alterar os arquivos testados

Os testes executados pelo script estão definidos diretamente no arquivo:
```
src/test_runner.py
```
Dentro da função responsável pelos testes (geralmente ``run_all_tests``), existe uma lista contendo os caminhos dos arquivos comparados, por exemplo:
```
test_cases = [
    ("tests/ArrayTest/MainT.xml", "tests/ArrayTest/MainT_oficial.xml"),
]
```
Para adicionar, remover ou alterar testes, basta editar essa lista, incluindo os caminhos dos arquivos gerados e seus respectivos arquivos oficiais.
A simples inclusão de arquivos na pasta `tests` não os adiciona automaticamente à execução dos testes, sendo necessária a atualização manual da lista `test_cases`.
