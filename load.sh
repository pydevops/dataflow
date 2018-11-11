#!/usr/bin/env bash -x
set -euo pipefail
INPUT_BUCKET=pso-victory-dev-8f039964-e2bb-11e8-b17e-1700de069414

for i in {1..3} 
do 
 gsutil cp data/spin.pdf gs://${INPUT_BUCKET}/
 sleep 1
done

#gsutil -o GSUtil:parallel_composite_upload_threshold=150M cp 1g gs://pso-victory-dev-8f039964-e2bb-11e8-b17e-1700de069414/
