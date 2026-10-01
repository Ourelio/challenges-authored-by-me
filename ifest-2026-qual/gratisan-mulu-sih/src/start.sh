#!/bin/sh
set -eu

docker compose up --build --force-recreate -d
