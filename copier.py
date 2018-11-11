# Copyright 2018 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""copier.py is a Dataflow pipeline which reads Cloud PubSub events and 
copy the data from bucket to bucket.
This example does not do any transformation on the data. 
"""

from __future__ import absolute_import
from __future__ import print_function
import argparse
import logging
import re
import json
import os
import apache_beam as beam
from apache_beam.io import WriteToText
from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam.options.pipeline_options import SetupOptions
from apache_beam.options.pipeline_options import StandardOptions
# Use beam's GCSFileSystem
from apache_beam.io.gcp.gcsfilesystem import GCSFileSystem

# Use google cloud storage
#from google.cloud import storage

class DataCopier:
    """A helper class which contains the logic to translate the file into 
    a format BigQuery will accept."""

    def parse_method(self,message, project_id,filesystem,output_bucket_name):
        """This method translates a GCS load event        
        Args:
            message: GCS upload event in JSON        
        Returns:
            [src_data_gcs,dest_data_gcs]
         """
        message_dict=json.loads(message)
        return self.copy(project_id=project_id,filesystem=filesystem,input_bucket_name=message_dict['bucket'], \
        input_blob_name=message_dict['name'],output_bucket_name=output_bucket_name)

        
    def copy(self,project_id='',filesystem=None,input_bucket_name='',input_blob_name='',output_bucket_name=''):
       
        # figure out input and output bucket name, object (blob) path
        # parse out customer_id
        customer_id=input_bucket_name.split(project_id+'-')[1]

        src_data=['gs://{}/{}'.format(input_bucket_name,input_blob_name)]
        dest_data=['gs://{}/{}/{}'.format(output_bucket_name,customer_id,input_blob_name)]
        filesystem.copy(src_data,dest_data)
        return zip(src_data,dest_data)
        


def run(argv=None):
    """The main function which creates the pipeline and runs it."""
    parser = argparse.ArgumentParser()
    # Here we add some specific command line arguments we expect.
    # Specifically we have the input file to load and the output table to
    # This is the final stage of the pipeline, where we define the destination
    # of the data.  In this case we are writing to BigQuery.

    parser.add_argument(
      '--input_subscription', required=True,
      help=('Input PubSub subscription of the form '
            '"projects/<PROJECT>/subscriptions/<SUBSCRIPTION>."'))
   
    parser.add_argument('--output', required=True,
                        help='Output bucket for data',
                        default='')
    parser.add_argument('--log', required=True,
                        help='log bucket',
                        default='')

    # Parse arguments from the command line.
    known_args, pipeline_args = parser.parse_known_args(argv)
    #import pprint
    #pprint.pprint(known_args)
    #pprint.pprint(pipeline_args)
    #pprint.pprint(pipeline_options.get_all_options())
    
    # We use the save_main_session option because one or more DoFn's in this
     # workflow rely on global context (e.g., a module imported at module level).
    pipeline_options = PipelineOptions(pipeline_args)
    pipeline_options.view_as(SetupOptions).save_main_session = True
    pipeline_options.view_as(StandardOptions).streaming = True

    # get options
    project_id=pipeline_options.get_all_options()['project']
    output_bucket_name=known_args.output
    log_bucket_name=known_args.log
    log_file_path='gs://{}/logs'.format(log_bucket_name)

    fs = GCSFileSystem(pipeline_options=pipeline_options)
    
    # DataIngestion is a class we built in this script to hold the logic for
    # transforming the file into a BigQuery table.
    data_copier = DataCopier()
    # Initiate the pipeline using the pipeline arguments passed in from the
    # command line.  This includes information including where Dataflow should
    # store temp files, and what the project id is
  
    p = beam.Pipeline(options=pipeline_options)

    (p | beam.io.ReadFromPubSub(
        subscription=known_args.input_subscription)
         | 'Copying customer data to the final data-bucket/customer-id' >> beam.Map(lambda m:
            data_copier.parse_method(m,project_id,fs,output_bucket_name))
          | 'Write results to the output bucket' >> WriteToText(file_path_prefix=log_file_path))

    p.run().wait_until_finish()


if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    run()

        # storage_client = storage.Client()
        # input_bucket = storage_client.get_bucket(input_bucket_name)
        # output_bucket = storage_client.get_bucket(output_bucket_name)
    
        # #blob_string=input_blob.download_as_string()
        # #input_blob.download_to_filename('foo.pdf')

        # output_blob = output_bucket.blob(output_blob_name,encryption_key=None)
        #output_blob.upload_from_string(blob_string)

        # input_bucket = storage_client.get_bucket(input_bucket_name)
        # input_blob = input_bucket.get_blob(input_blob_name)
        # output_blob_name='{}/{}'.format(customer_id,input_blob_name)
        # output_blob = output_bucket.blob(output_blob_name)

        # output_blob = output_bucket.blob(output_blob_name,encryption_key=None)
        # output_blob.rewrite(source=input_blob)

        # token = None
        # while True:
        #     token, bytes_rewritten, total_bytes = output_blob.rewrite(
        #         input_blob, token=token)
        #     if token is None:
        #         break