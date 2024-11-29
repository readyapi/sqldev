#!/usr/bin/env bash

set -e
set -x

ruff check sqldev tests docs_src scripts --fix
ruff format sqldev tests docs_src scripts
