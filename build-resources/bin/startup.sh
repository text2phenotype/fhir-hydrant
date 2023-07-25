#!/usr/bin/env bash

# Source the bash.utils
source "${APP_BASE_DIR}/bin/bash.utils"

log.info "> Starting ${APP_NAME}..."

case "${APP_ENVIRONMENT}" in
  dev*)
    export FLASK_ENV='development'
  ;;

  test)
    export FLASK_ENV='test'
  ;;

  *)
    export FLASK_ENV='production'
  ;;

esac


declare nginx_default_conf="/etc/nginx/sites-available/default"

log.info ">>> Installing nginx proxy config..."
j2 "${APP_BASE_DIR}/build-resources/config/nginx-proxy.conf.j2" > "${nginx_default_conf}"
log.info ">> nginx configuration complete."

log.info ">> Starting nginx..."
nginx

log.info ">> Launching guincorn workers..."
declare timeout="${GUNICORN_TIMEOUT:-90}"
# Calculate workers based on number of cores.
declare multiplier="${GUNICORN_WORKER_MULTIPLIER:-2}"
declare cores=$(( $(lscpu | awk '/^Socket/{ print $2 }') * $(lscpu | awk '/^Core/{ print $4 }') ))
declare workers=$(( ( ${cores} * ${multiplier} ) + 1 ))

log.info ">>> Cores:      ${cores}"
log.info ">>> Multiplier: ${multiplier}"
log.info ">>> Workers:    ${workers}"
log.info ">>> Timeout:    ${timeout}"

time gunicorn --timeout "${timeout}" --workers "${workers}" --bind "unix:${APP_BASE_DIR}/fhir-hydrant.sock" fhirhydrant.fhir_server.__main__:app

log.warn "> ${APP_NAME} stopped!"
