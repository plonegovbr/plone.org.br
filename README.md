# plone.org.br

## Quick start

### Dependências

- Python 3.9
- Node 16
- yarn
- Docker

### Instalação

```shell
git clone git@github.com:plonegovbr/plone.org.br.git
cd plone.org.br
make install
make create-site
```

### Inicio

Para iniciar o Backend (http://localhost:8080/)

```shell
make start-backend
```

Para iniciar o Frontend (http://localhost:3000/)

```shell
make start-frontend
```

## Estrutura

Este é um monorepo composto por dois ambientes: API (backend) e frontend.

- **backend**: API (Backend) com instalação do Plone usando pip (sem buildout). Incluindo o pacote de policy - ploneorgbr.core.
- **frontend**: Pacote React (Volto).

## Motivação

- Este repositório contém todos os códigos necessários para rodar o site plone.org.br (excluindo os complementos padrões para Plone e React);
- Github Workflows são acionados com base nas alterações de códigos no repositório (veja .github/workflows);
- Facilidade de criar imagens Docker para cada código;
- Apresentar a instalação do Plone sem buildout.

## Notas

Se o site não funcionar corretamente, podem ser alguns componentes que não tenham iniciados corretamente. Para tentar resolver, restart o backend e o frontend.

Comandos úteis:
- `docker stack ps plone`
- `docker service scale plone_backend=0`
- `docker service scale plone_backend=1`
- `docker service scale plone_backend=2`
