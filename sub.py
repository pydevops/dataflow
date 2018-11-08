#!/usr/bin/env python

# Copyright 2018 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from google.cloud import storage
from google.cloud import pubsub_v1
import os

def copy(project_id='',input_bucket_name='',object_name=''):

    # figure out input and output bucket name, object (blob) path
    output_bucket_name=os.environ['OUTPUT_BUCKET']
    # parse out customer_id
    customer_id=input_bucket_name.split(project_id+'-')[1]
    output_blob_path='{}/{}'.format(customer_id,object_name)
    print('output_blob_path={}'.format(output_blob_path))

    storage_client = storage.Client()
    input_bucket = storage_client.get_bucket(input_bucket_name)
    output_bucket = storage_client.get_bucket(output_bucket_name)

    input_blob = input_bucket.get_blob(object_name)
    blob_string=input_blob.download_as_string()
    output_blob = output_bucket.blob(output_blob_path)
    output_blob.upload_from_string(blob_string)


def receive_messages(project_id='', subscription_name=''):
    """Receives messages from a pull subscription."""

    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = 'projects/{project_id}/subscriptions/{sub}'.format(
        project_id=project_id,
        sub=subscription_name,  # Set this to something appropriate.
    )
 
    def callback(message):
        #print('Received message: {}'.format(message.attributes))
        if message.attributes:
            event_data={}
            print('Attributes:')
            for key in message.attributes:
                value = message.attributes.get(key)
                #print('{}: {}'.format(key, value))
                event_data[key]=value
            print(event_data)
            if event_data['eventType']=='OBJECT_FINALIZE':
                print('Bucket: {}'.format(event_data['bucketId']))
                print('File: {}'.format(event_data['objectId']))
                copy(project_id=project_id,input_bucket_name=event_data['bucketId'],object_name=event_data['objectId'])
        message.ack()

    future = subscriber.subscribe(subscription_path, callback)
    try:
        future.result()
    except KeyboardInterrupt:
        future.cancel()

if __name__ == '__main__':
    receive_messages(project_id='pso-victory-dev',subscription_name='copierSub')