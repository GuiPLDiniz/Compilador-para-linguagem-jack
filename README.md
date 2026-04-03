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
- `src/`: código fonte
- `tests/`: arquivos de teste

## Estado atual
O projeto já realiza:
- leitura de arquivos `.jack`
- geração de arquivo XML de saída
- tokenização inicial de símbolos e palavras simples

## Saída
Para cada arquivo `.jack`, o programa gera automaticamente um arquivo `.xml` correspondente com a estrutura inicial de tokens.

## Observações
O projeto será desenvolvido sem o uso de geradores automáticos de analisadores léxicos e sintáticos (Lex, Flex, Yacc), conforme exigência da disciplina.