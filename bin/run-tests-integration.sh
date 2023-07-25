#!/usr/bin/env bash

###
# Import utilities
source "./build-tools/bin/build.utils"

###
# Variables

# UNIVERSE_IS_VERBOSE enables log level INFO.
UNIVERSE_IS_VERBOSE=true

log.info "> Start integration testing..."

log.info "> No integration tests. Skipping."
integration_test_result=0

# log.info ">> Install docker-compose..."
# pip install docker-compose

# # Build any required resources
# log.info ">> docker-compose build..."
# docker-compose --file docker-compose-tests-integration.yaml build

# # Stand up the test stack
# log.info ">> docker-compose up..."
# docker-compose --file docker-compose-tests-integration.yaml up --exit-code-from nlp
# integration_test_result=$?

# # Cleanup docker-compose
# log.info ">> docker-compose down..."
# docker-compose --file docker-compose-tests-integration.yaml down

log.info "> Integration testing complete. ('${integration_test_result}')"
exit ${integration_test_result}
