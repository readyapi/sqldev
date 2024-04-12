#!/bin/sh -e
set -x

ruff sqldev tests docs_src scripts --fix
ruff format sqldev tests docs_src scripts
