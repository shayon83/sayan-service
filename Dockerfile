##
# base
#
# The `minimal` image creates a minimal runtime container.
#
# Note: Images based on this image will be built without superuser privileges.
# http://github.com/syapse/docker-service
#
FROM 141380700111.dkr.ecr.us-west-2.amazonaws.com/service:1.1.1 as prod

LABEL service="sayan-service" \
    team="cloudeng"

# Copy required project files into the WORKDIR.
COPY --chown=user:user setup.py setup.cfg /srv/

# Create a dummy service directory for the dependency installation.
# Install the package with pip.
RUN mkdir -p /srv/sayan_service \
    && pip install /srv[prod]

# Copy the project directory (https://github.com/moby/moby/issues/29211)
COPY --chown=user:user sayan_service /srv/sayan_service

# Copy the entrypoint files for booting the application.
COPY --chown=user:user autoapp.py structlogger.py gunicorn_config.py /srv/

# Copy migrations for upgrades
COPY --chown=user:user migrations /srv/migrations


##
# dev
#
# The `dev` image creates the runtime container for local development
# environments, where the code can be updated on the fly.
#
FROM prod as dev

# Configure gunicorn to reload on code changes.
ENV GUNICORN_CMD_ARGS="$GUNICORN_CMD_ARGS --reload"

# Install the package with pip.
RUN pip install /srv[dev,test]

# Copy the rest of the project into the WORKDIR.
COPY --chown=user:user . /srv/

# Mount a volume at `/srv`
VOLUME /srv


##
# utils
#
# The `utils` image provides utility applications for diagnostics and troubleshooting.
#
FROM prod as utils

# Install common system packages needed for utilities.
# Note: The mkdir commands resolve an issue with postgresql-client config.
USER root
RUN apt-get update \
 && mkdir -p /usr/share/man/man1 \
 && mkdir -p /usr/share/man/man7 \
 && apt-get install -y --no-install-recommends \
      bash \
      tmux \
      curl \
      vim  \
      htop \
      less \
      postgresql-client
USER user

# Copy bin scripts locally
COPY --chown=user:user bin /srv/bin


##
# test
#
# The `test` image provides a dedicated container for running the application
# test suite. It is based on the `utils` image so that a developer will have
# diagnostic tools available in the event of a failure.
#
FROM utils as test

# Copy test configuration(s)
COPY --chown=user:user .coveragerc /srv/.coveragerc

# Copy the test suite
COPY --chown=user:user tests /srv/tests

# Install the test reporter for code climate
ENV CC_REPORTER_URL=https://codeclimate.com/downloads/test-reporter/test-reporter-latest-linux-amd64
ADD --chown=user:user "$CC_REPORTER_URL" /srv/cc-test-reporter

# Install the package with pip.
RUN pip install /srv[test]
