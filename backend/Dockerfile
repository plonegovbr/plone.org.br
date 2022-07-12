ARG PLONE_VERSION=6.0.0a6
FROM plone/plone-backend:${PLONE_VERSION}

LABEL maintainer="PloneGov-BR <gov@plone.org.br>" \
      org.label-schema.name="site-backend" \
      org.label-schema.description="Plone.org.br backend image." \
      org.label-schema.vendor="PloneGov-BR"

# Add local code
COPY . .

# Install local requirements and fix permissions
RUN ./bin/pip install -r requirements.txt \
    && chown -R plone: /app
