#!/usr/bin/env bash -x
set -euo pipefail

PROJECT_ID=$(gcloud config get-value project)
INPUT_SUB=input-sub
OUTPUT_TOPIC_NAME=gcs-upload-topic
OUTPUT_SUB=output-sub

## create a filter for cloud pub sub
gcloud dataflow jobs run upload-filter \
    --gcs-location gs://dataflow-templates/latest/Cloud_PubSub_to_Cloud_PubSub \
    --parameters \
inputSubscription=projects/${PROJECT_ID}/subscriptions/${INPUT_SUB},\
outputTopic=projects/${PROJECT_ID}/topics/${OUTPUT_TOPIC_NAME},\
filterKey=eventType,\
filterValue=OBJECT_FINALIZE



# Testing
#gsutil -o GSUtil:parallel_composite_upload_threshold=150M cp 1g gs://pso-victory-dev-8f039964-e2bb-11e8-b17e-1700de069414/

# RUN the wordcount example
# python -m apache_beam.examples.wordcount --input gs://dataflow-samples/shakespeare/kinglear.txt \
#                                          --output gs://pso-victory-dev-data/counts \
#                                          --runner DataflowRunner \
#                                          --project pso-victory-dev \
#                                          --temp_location gs://pso-victory-dev-data/tmp/
                                         

