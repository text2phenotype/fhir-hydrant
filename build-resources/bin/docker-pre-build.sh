#!/usr/bin/env bash

set -e

# Source the bash.utils
source "${APP_BASE_DIR}/bin/bash.utils"

log.info "> Starting ${APP_NAME} build..."

log.info ">> Installing ${APP_NAME} dependencies..."

apt-get update -y

apt-get install -y nginx

log.info ">> ${APP_NAME} dependency installation complete."
