#!/bin/bash
source venv/bin/activate
export PYTHONPATH=$(pwd)
venv/bin/python $@

