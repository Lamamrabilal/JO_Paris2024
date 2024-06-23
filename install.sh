#!/bin/zsh
poetry export --without-hashes -f requirements.txt --output requirements.txt
PIP_NO_BUILD_ISOLATION=1 pip install psycopg2-binary
