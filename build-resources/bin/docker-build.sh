#!/usr/bin/env bash

set -e

# Source the bash.utils
source "${APP_BASE_DIR}/bin/bash.utils"

log.info ">> Installing ${APP_BASE_DIR}/requirements.txt ..."
pip install --no-cache-dir -r "${APP_BASE_DIR}/requirements.txt"

log.info "> Installing ${APP_NAME}..."

pip install -e "${APP_BASE_DIR}"

log.info ">> Setting up nginx config..."
cp -v "${APP_BASE_DIR}/build-resources/config/nginx.conf" "/etc/nginx/nginx.conf"
log.info ">> Done removing default nginx site"

log.info ">> Removing default nginx site..."
rm -f "/etc/nginx/sites-available/default"
log.info ">> Done removing default nginx site"

log.info "> ${APP_NAME} installation complete."
