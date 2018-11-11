#!/usr/bin/env bash -x
set -euo pipefail

PROJECT_ID=$(gcloud config get-value project)
INPUT_TOPIC_NAME=input-topic
INPUT_SUB="projects/${PROJECT_ID}/subscriptions/input-sub"
OUTPUT_BUCKET=pso-victory-dev-data
TEMP_BUCKET=pso-victory-dev-tmp

PROJECT_ID=${PROJECT_ID}  OUTPUT_BUCKET=${OUTPUT_BUCKET}  python copier.py \
 --runner=DataflowRunner \
 --streaming \
 --max_num_workers=2 \
 --input_subscription=${INPUT_SUB} \
 --autoscaling_algorithm=THROUGHPUT_BASED \
 --region=us-west1 \
 --project=${PROJECT_ID} \
 --output=${OUTPUT_BUCKET} \
 --log=${TEMP_BUCKET} \
 --staging_location="gs://${TEMP_BUCKET}/binaries" \
 --temp_location="gs://${TEMP_BUCKET}/temp"

 #--runner=DataflowRunner \
#--runner=DirectRunner \


# Testing
# copy data
# gsutil -o GSUtil:parallel_composite_upload_threshold=200M cp 1g gs://pso-victory-dev-8f039964-e2bb-11e8-b17e-1700de069414/
# read pubsub
# gcloud pubsub subscriptions pull --auto-ack input-sub --limit 10


# gcloud dataflow jobs run upload-event-to-text \
#     --gcs-location gs://dataflow-templates/latest/Cloud_PubSub_to_GCS_Text \
#     --parameters \
# inputTopic=projects/${PROJECT_ID}/topics/${INPUT_TOPIC_NAME},\
# outputDirectory=gs://${OUTPUT_BUCKET}/output/,\
# outputFilenamePrefix=output-,\
# outputFilenameSuffix=.txt

## create a filter for cloud pub sub
# gcloud dataflow jobs run upload-filter \
#     --gcs-location gs://dataflow-templates/latest/Cloud_PubSub_to_Cloud_PubSub \
#     --parameters \
# inputSubscription=projects/${PROJECT_ID}/subscriptions/${INPUT_SUB},\
# outputTopic=projects/${PROJECT_ID}/topics/${OUTPUT_TOPIC_NAME},\
# filterKey=eventType,\
# filterValue=OBJECT_FINALIZE


# RUN the wordcount example
# python -m apache_beam.examples.wordcount --input gs://dataflow-samples/shakespeare/kinglear.txt \
#                                          --output gs://pso-victory-dev-data/counts \
#                                          --runner DataflowRunner \
#                                          --project pso-victory-dev \
#                                          --temp_location gs://pso-victory-dev-data/tmp/
                                         
