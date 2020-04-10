import os, io
import re #regular expression module
from google.cloud import vision
from google.cloud import storage
from google.protobuf import json_format  #must be call for json format in my bucket
"""
# all library installed
"""
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'fourth-elixir-273216-06b58e3308db.json' #mera service account #
client = vision.ImageAnnotatorClient()
batch_size = 1   #pdf ke pages  
mime_type = 'application/pdf' #file type
feature = vision.types.Feature(
type=vision.enums.Feature.Type.DOCUMENT_TEXT_DETECTION) #


gcs_source_uri = 'gs://greenertronics-42/test.pdf'
gcs_source = vision.types.GcsSource(uri=gcs_source_uri)#mere source
input_config = vision.types.InputConfig(gcs_source=gcs_source, mime_type=mime_type)



gcs_destination_uri = 'gs://greenertronics-42/pdf_result'#mere destination
gcs_destination = vision.types.GcsDestination(uri=gcs_destination_uri)



output_config = vision.types.OutputConfig(gcs_destination=gcs_destination, batch_size=batch_size)#function for destination and pages required in batch
async_request = vision.types.AsyncAnnotateFileRequest(      #An offline file annotation request. feature=document ki detection or source or destination ka function
features=[feature], input_config=input_config, output_config=output_config)
operation = client.async_batch_annotate_files(requests=[async_request])
operation.result(timeout=180)
storage_client = storage.Client()
match = re.match(r'gs://([^/]+)/(.+)', gcs_destination_uri)  #link ka slash dhonde ga
bucket_name = match.group(1)#link ka slash dhonde ga
prefix = match.group(2)#ye . ka
bucket = storage_client.get_bucket(bucket_name)


# List object with the given prefix
blob_list = list(bucket.list_blobs(prefix=prefix))
print('Output files:')
for blob in blob_list: #loop jo words recognized word print krae ga
    print(blob.name)


output = blob_list[0]
json_string = output.download_as_string()
response = json_format.Parse(
json_string, vision.types.AnnotateFileResponse())
first_page_response = response.responses[0]
annotation = first_page_response.full_text_annotation
print(u'Full text:')
print(annotation.text)