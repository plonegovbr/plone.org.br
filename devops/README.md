# Deploy do plone.org.br

O site roda como uma stack do Docker Swarm, definida em
[`stacks/stack.yml`](stacks/stack.yml), com três serviços:

- `frontend`: o Volto, com 2 réplicas;
- `backend`: o Plone, com 2 réplicas, guardando os dados por RelStorage num
  PostgreSQL gerenciado (não há banco na stack);
- `dbpack`: o pack diário do banco às 04:40, disparado pelo
  [swarm-cronjob](https://github.com/crazy-max/swarm-cronjob).

A stack não traz proxy. O Traefik do cluster lê os labels dos serviços na rede
externa `public` e emite os certificados com o resolver indicado em
`CERTRESOLVER`.

## Pré-requisitos no cluster

- Rede overlay externa `public`, compartilhada com o Traefik.
- Traefik configurado com o resolver `CERTRESOLVER`, os entrypoints `http` e
  `https` e o middleware `gzip`.
- swarm-cronjob rodando, para o serviço `dbpack`.
- Nós com o label `type` igual a `BACKEND_NODE_TYPE` e `FRONTEND_NODE_TYPE`.
- O banco `DB_NAME` criado no PostgreSQL, com o usuário `DB_USER` como dono,
  e os IPs dos nós do cluster liberados no PostgreSQL.

## Workflows

| Workflow | Quando roda | O que faz |
| --- | --- | --- |
| [`main.yml`](../.github/workflows/main.yml) | push em qualquer branch | Testa e, quando o push muda `backend/` ou `frontend/`, publica a imagem correspondente com as tags `sha-<commit>` e o nome da branch |
| [`tag-release-deploy.yml`](../.github/workflows/tag-release-deploy.yml) | push de uma tag | Constrói as imagens da tag e faz o deploy com a tag `sha-<commit>` |
| [`manual-deploy.yml`](../.github/workflows/manual-deploy.yml) | manual, escolhendo a branch ou a tag | Faz o deploy das imagens já publicadas com o nome da branch ou da tag |

Os dois workflows de deploy usam o environment `plone.org.br` do GitHub, com
um deploy por vez. As imagens em `ghcr.io/plonegovbr` são públicas, então o
deploy não faz login no registry.

## Configuração do environment `plone.org.br`

Secrets da conexão com o manager do Swarm:

| Nome | Conteúdo |
| --- | --- |
| `DEPLOY_HOST` | Endereço do manager |
| `DEPLOY_PORT` | Porta SSH |
| `DEPLOY_USER` | Usuário com acesso ao Docker |
| `DEPLOY_SSH` | Chave privada SSH desse usuário |

Valores da stack, a partir dos modelos desta pasta:

| Nome | Tipo | Modelo |
| --- | --- | --- |
| `ENV_VARS` | Variável | [`.env_vars_gha`](.env_vars_gha) |
| `ENV_SECRETS` | Secret | [`.env_secrets_gha`](.env_secrets_gha) |

Copie o modelo, troque os valores (o endereço, a porta e o banco do
PostgreSQL, as senhas, o secret do id.plone.org) e grave pela linha de
comando, a partir do arquivo:

```shell
gh variable set ENV_VARS --env plone.org.br --repo plonegovbr/plone.org.br < env_vars
gh secret set ENV_SECRETS --env plone.org.br --repo plonegovbr/plone.org.br < env_secrets
```

Não cole esses valores no formulário do GitHub: ele grava as quebras de linha
como CRLF, e cada valor, menos o último, chega à stack terminado em `\r`.

### Valores da stack

- `DB_SSLMODE` vai para o `sslmode` do libpq e vale `require` por padrão.
- `BASIC_AUTH_PASSWORD_CLASSICUI` protege o `/ClassicUI` junto com
  `BASIC_AUTH_USER`, no middleware `basicauth` do Traefik.
- `ID_PLONE_ORG_CLIENT_SECRET` habilita o login pelo id.plone.org quando o
  site é criado ou o profile é reaplicado. Vazio, o provedor fica desabilitado.
