## install dependencies if needed
[Quickstart python for dataflow](https://cloud.google.com/dataflow/docs/quickstarts/quickstart-python) 

```
pip install -r requirements.txt
```

Or if you prefer **pipenv**

```
pipenv --two shell
pipenv install apache-beam[gcp]
``` 

## set up GOOGLE_APPLICATION_CREDENTIALS
Please generate a json key for the service account if needed. 
```
export GOOGLE_APPLICATION_CREDENTIALS=<svc>.json
```

## configure and set up cloud pubsub
```
./setup_pubsub.sh
```

## dataflow runners

* The DirectRunner is used for development. 
* The DataflowRunner submits the pipeline to the Google Cloud Dataflow.

## run dataflow
```
$./run_dataflow.sh
```

## testing a file upload
with size desired
```
INPUT_BUCKET=pso-victory-dev-8f039964-e2bb-11e8-b17e-1700de069414
(OSX) mkfile -n 100m 100m
gsutil cp 100m gs://${INPUT_BUCKET}

(OSX) mkfile -n 1g 1g
gsutil -o GSUtil:parallel_composite_upload_threshold=200M cp 1g gs://${INPUT_BUCKET}
```

## flush the pubsub for testing
```
INPUT_SUB="input-sub"
gcloud pubsub subscriptions pull --auto-ack ${INPUT_SUB} --limit 100
```
and wait a
## issue
When upload size is larger than 500m, beams GCS storage is broken.
```
    self.do_fn_invoker.invoke_process(windowed_value)
  File "apache_beam/runners/common.py", line 414, in apache_beam.runners.common.SimpleInvoker.invoke_process
    windowed_value, self.process_method(windowed_value.value))
  File "/Users/yongweiy/.local/share/virtualenvs/dataflow--znvn7ii/lib/python2.7/site-packages/apache_beam/transforms/core.py", line 1068, in <lambda>
  File "copier.py", line 120, in <lambda>
  File "copier.py", line 51, in parse_method
  File "copier.py", line 62, in copy
  File "/usr/local/lib/python2.7/dist-packages/apache_beam/io/gcp/gcsfilesystem.py", line 199, in copy
    raise BeamIOError("Copy operation failed", exceptions)
BeamIOError: Copy operation failed with exceptions {('gs://pso-victory-dev-8f039964-e2bb-11e8-b17e-1700de069414/500m', 'gs://pso-victory-dev-data/8f039964-e2bb-11e8-b17e-1700de069414/500m'): HttpError()}

        org.apache.beam.runners.fnexecution.control.FnApiControlClient$ResponseStreamObserver.onNext(FnApiControlClient.java:157)
        org.apache.beam.runners.fnexecution.control.FnApiControlClient$ResponseStreamObserver.onNext(FnApiControlClient.java:140)
        org.apache.beam.vendor.grpc.v1.io.grpc.stub.ServerCalls$StreamingServerCallHandler$StreamingServerCallListener.onMessage(ServerCalls.java:248)
        org.apache.beam.vendor.grpc.v1.io.grpc.ForwardingServerCallListener.onMessage(ForwardingServerCallListener.java:33)
        org.apache.beam.vendor.grpc.v1.io.grpc.Contexts$ContextualizedServerCallListener.onMessage(Contexts.java:76)
        org.apache.beam.vendor.grpc.v1.io.grpc.internal.ServerCallImpl$ServerStreamListenerImpl.messagesAvailable(ServerCallImpl.java:263)
        org.apache.beam.vendor.grpc.v1.io.grpc.internal.ServerImpl$JumpToApplicationThreadServerStreamListener$1MessagesAvailable.runInContext(ServerImpl.java:683)
        org.apache.beam.vendor.grpc.v1.io.grpc.internal.ContextRunnable.run(ContextRunnable.java:37)
        org.apache.beam.vendor.grpc.v1.io.grpc.internal.SerializingExecutor.run(SerializingExecutor.java:123)
        java.util.concurrent.ThreadPoolExecutor.runWorker(ThreadPoolExecutor.java:1142)
        java.util.concurrent.ThreadPoolExecutor$Worker.run(ThreadPoolExecutor.java:617)
        java.lang.Thread.run(Thread.java:745)
^CTraceback (most recent call last):
  File "copier.py", line 128, in <module>
    run()
  File "copier.py", line 123, in run
    p.run().wait_until_finish()
  File "/Users/yongweiy/.local/share/virtualenvs/dataflow--znvn7ii/lib/python2.7/site-packages/apache_beam/runners/dataflow/dataflow_runner.py", line 1153, in wait_until_finish
    time.sleep(5.0)
    ```