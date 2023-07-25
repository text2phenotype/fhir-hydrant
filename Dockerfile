# Use a reasonable FROM image
ARG IMAGE_FROM_TAG
FROM text2phenotype/text2phenotype-py:${IMAGE_FROM_TAG:-latest}

# Create a list of build arguments
ARG APP_ENVIRONMENT
ARG APP_GIT_SHA
ARG APP_INCLUDE_EXAMPLES
ARG APP_IS_DEBUG
ARG IMAGE_FROM_TAG

# Set environment variables
# UNIVERSE_IS_VERBOSE enables log level INFO.
ENV UNIVERSE_IS_VERBOSE=true

### Application metadata
ENV APP_ENVIRONMENT="${APP_ENVIRONMENT:-prod}"
ENV APP_GIT_SHA="${APP_GIT_SHA:-unset}"
ENV APP_NAME="fhir-hydrant"
ENV APP_IS_DEBUG="${APP_IS_DEBUG:-False}"

### File path locations
ENV APP_BASE_DIR="/app"
ENV PATH="${APP_BASE_DIR}/bin/:${PATH}"

# Set some container options
WORKDIR "${APP_BASE_DIR}"
EXPOSE 8080

# Copy the the application code.
COPY . "${APP_BASE_DIR}"

# Copy the bash.utils script.
COPY "./build-tools/bin/bash.utils" "${APP_BASE_DIR}/bin/"

# Run the scripts together so they end up as a single layer.
RUN mv ${APP_BASE_DIR}/build-resources/bin/* "${APP_BASE_DIR}/bin/" && \
    "${APP_BASE_DIR}/bin/docker-pre-build.sh" && \
    "${APP_BASE_DIR}/bin/docker-build.sh" && \
    "${APP_BASE_DIR}/bin/docker-post-build.sh"

# Do not include an ENTRYPOINT unless it is explicitly required.
# Using an ENTRYPOINT can make it difficult to get into a running container,
# or launch the container with different commands.

# This command is what launches the service by default.
CMD ["/bin/bash", "-c", "${APP_BASE_DIR}/bin/startup.sh"]
