# Webdashboard.pro

## O que é

Um painel web baseado no projeto django 1.10 destinado a gerar gráficos interativos a partir de arquivos `.xlsx` sem utilizar diretamente código Javascript.

## Dependências

- python==2.7.8
- django==1.10
- bokeh==0.12.6 
- pandas
- tornado>=4.4

## Como funciona?

A análise bruta dos dados é realizada pela excelente biblioteca `pandas`. Os resultados analisados são repassados a um servidor `bokeh`, que, usando a biblioteca `BokehJS`, gera gráficos interativos e visualmente impressionantes através de chamadas assíncronas próprias.

Infelizmente, o servidor `bokeh` é baseado no `Tornado`, o que dificulta a utilização das ferramentas próprias do `django`. Portanto, esta aplicação depende de um servidor `bokeh` rodando em outro endereço, de forma que o `django`, aqui, é usado primariamente pela ferramenta de templating bastante flexível.

