#!/usr/bin/env bash
for f in tests/*.py
do
    python3 -m unittest $f
done

