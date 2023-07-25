#!/usr/bin/env bash

# Source the bash.utils
source "${APP_BASE_DIR}/bin/bash.utils"

log.info "> Running integration tests..."

# TODO: Add logic for integration tests

log.info "> No integration tests. Skipping."
exit_code=0

log.info "> Integration tests complete. Exited ('${exit_code}')"
exit ${exit_code}
