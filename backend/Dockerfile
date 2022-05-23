ARG PLONE_VERSION=6.0.0a4
FROM plone/plone-backend:${PLONE_VERSION}

LABEL maintainer="PloneGov-BR <gov@plone.org.br>" \
      org.label-schema.name="site-backend" \
      org.label-schema.description="Plone.org.br backend image." \
      org.label-schema.vendor="PloneGov-BR"

# Add local code
COPY . .
RUN ./bin/pip install -r requirements.txt
