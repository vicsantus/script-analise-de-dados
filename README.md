# Projeto de analise de dados!

## Contextualizando

Trata-se de um script em python e uma macro em vba para libreoffice. O script faz uma leitura de um arquivo especifico que pode ser pego no site https://www.gov.br/produtividade-e-comercio-exterior/pt-br/assuntos/comercio-exterior/estatisticas/base-de-dados-bruta ou jogando no google "base comercio exterior brasil" no primeiro site. São dados de importação e exportação de produtos brasileiros.

Os arquivos originais tem mais de 1 milhão de linhas cada, então nesse repositório eu fiz 2 pequenos samples desses arquivos, com muito menos dados.

O script.py pega esses dois arquivos, e divide eles em 26 arquivos com referente aos 26 estados brasileiros, e soma valores internos juntando dados de importação e exportação.

O macro.ods pega todos esses 26 arquivos em une em um unico formatando eles.

## Instalação

Instalação do projeto

```bash
  git clone git@github.com:vicsantus/script-analise-de-dados.git
  cd script-analise-de-dados
  python3 script.py
```

Para fazer o macro.ods funcionar é necessário ter instalado libreoffice no computador, abrir o arquivo macro.ods, colocar a rota dos resultados do script.py no campo de rota e clicar no botão.
