#!/usr/bin/env bash

set -e

# Source the bash.utils
source "${APP_BASE_DIR}/bin/bash.utils"

log.info ">> Cleaning up ${APP_NAME} build..."

log.info ">>> apt-get autoremove"
apt-get autoremove -y

log.info ">>> apt-get clean"
apt-get clean -y

log.info ">>> removing uncleaned apt files in '/var/lib/apt/lists/'"
rm -rf "/var/lib/apt/lists/*.*"
rm -rf "/var/lib/apt/lists/*"

log.info ">>> remove build files from '${APP_BASE_DIR}/build'"
rm -rf "${APP_BASE_DIR}/build/"

log.info ">> ${APP_NAME} build cleanup complete."

log.info "> ${APP_NAME} build complete."
