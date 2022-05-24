# plone.org.br

## Quick start

### Requirements

- Python 3.9
- Node 16 / yarn
- Docker

### Install

```shell
git clone git@github.com:plonegovbr/plone.org.br.git
cd plone.org.br
make install
make create-site
```

### Start

Start the Backend (http://localhost:8080/)

```shell
make start-backend
```

Start the Frontend (http://localhost:3000/)

```shell
make start-frontend
```

## Structure

This monorepo is composed by two distinct codebases: api and frontend.

- **backend**: API (Backend) Plone installation using pip (not buildout). Includes a policy package named ploneorgbr.core
- **frontend**: React (Volto) package named ploneorgbr

### Reasoning

- Repo contains all codebase needed to run the plone.org.br (excluding existing addons for Plone and React).
- Github Workflows are triggered based on changes on each codebase (see .github/workflows)
- Easier to create Docker images for each codebase
- Showcase Plone installation/setup without buildout

## Notes

If the site does not start correctly, it may be because of a race condition.
As a temporary workaround, stop the back ends then start them up one at a time.

Useful commands:
- `docker stack ps plone`
- `docker service scale plone_backend=0`
- `docker service scale plone_backend=1`
- `docker service scale plone_backend=2`
