#!/usr/bin/env bash
set -euo pipefail
INPUT_BUCKET=pso-victory-dev-8f039964-e2bb-11e8-b17e-1700de069414
OUTPUT_BUCKET=pso-victory-dev-data

OUTPUT_BUCKET=${OUTPUT_BUCKET} python sub.py