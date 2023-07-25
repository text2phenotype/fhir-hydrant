#!/usr/bin/env bash

###
# Import utilities
source "./build-tools/bin/build.utils"

###
# Variables

# UNIVERSE_IS_VERBOSE enables log level INFO.
UNIVERSE_IS_VERBOSE=true

log.info "> Start unit testing..."

log.info "> No unit tests. Skipping."
unit_test_result=0

# log.info ">> Install docker-compose..."
# pip install docker-compose

# # Build any required resources
# log.info ">> docker-compose build..."
# docker-compose --file docker-compose-tests-unit.yaml build

# # Stand up the test stack
# log.info ">> docker-compose up..."
# docker-compose --file docker-compose-tests-unit.yaml up --exit-code-from nlp
# unit_test_result=$?

# # Cleanup docker-compose
# log.info ">> docker-compose down..."
# docker-compose --file docker-compose-tests-unit.yaml down

log.info "> Unit testing complete. ('${unit_test_result}')"
exit ${unit_test_result}
