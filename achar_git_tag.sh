#!/usr/bin/env bash

git tag \
| sort --version-sort \
| awk '{ save=$0 } END { print save }'