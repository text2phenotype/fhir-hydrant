#!/usr/bin/env bash

# Source the bash.utils
source "${APP_BASE_DIR}/bin/bash.utils"

log.info "> Running unit tests..."

log.info "> Installing python ${APP_BASE_DIR}/requirements-test.txt..."
pip install --no-cache-dir -r "${APP_BASE_DIR}/requirements-test.txt"

python -m pytest "${APP_BASE_DIR}/tests"
exit_code=$?

log.info "> Unit tests complete. Exited ('${exit_code}')"
exit ${exit_code}
