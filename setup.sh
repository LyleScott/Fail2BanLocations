#!/usr/bin/env bash
# Lyle Scott, III  // lyle@digitalfoo.net // Copyright 2013

virtualenv --no-site-packages venv
source venv/bin/activate
pip install -r venv/requirements.txt
