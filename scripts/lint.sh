#!/usr/bin/env bash

set -e
set -x

mypy sqldev
ruff sqldev tests docs_src scripts
ruff format sqldev tests docs_src --check
