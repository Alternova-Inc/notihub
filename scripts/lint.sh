#!/bin/sh

HIGHLIGHT_COLOR="\e[1;36m" # cyan
DEFAULT_COLOR="\e[0m"

CURRENT_DIRECTORY=$(pwd)

echo "\n${HIGHLIGHT_COLOR}Running black...${DEFAULT_COLOR}"
black . --config pyproject.toml

echo "\n${HIGHLIGHT_COLOR}Running ruff...${DEFAULT_COLOR}"
ruff check . --fix --config pyproject.toml

echo "\n${HIGHLIGHT_COLOR}Running bandit...${DEFAULT_COLOR}"
bandit -r ./* --configfile pyproject.toml

echo "\n${HIGHLIGHT_COLOR}Running pylint...${DEFAULT_COLOR}"
pylint --fail-under=9 ./*

cd ${CURRENT_DIRECTORY}
