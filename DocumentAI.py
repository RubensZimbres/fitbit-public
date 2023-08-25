import os
from google.api_core.client_options import ClientOptions
from google.cloud import documentai_v1 as documentai
from google.api_core.operation import Operation
from google.cloud import storage
import vertexai
from vertexai.preview.language_models import TextGenerationModel
from vertexai.preview.language_models import TextEmbeddingModel
import re
from nltk import FreqDist
import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import time

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/home/user/key.json'

nomes=[]
sumarios=[]
embeddings=[]

# MAKE OCR

directory='/home/user/fitbit/PDF'

for filename in os.listdir(directory):
    if os.path.isfile(os.path.join(directory, filename)):
        print(filename)

project_id = 'your-project-id'
location = 'us'  # Format is 'us' or 'eu'
processor_id = '7897jbkvhjvjvjh775'  # Create processor in Cloud Console

# Format 'gs://input_bucket/directory/file.pdf'
gcs_input_uri = "gs://pdfs/"+filename
input_mime_type = "application/pdf"

# Format 'gs://output_bucket/directory'
gcs_output_uri = "gs://pdfs/output"
# iterate over all files in google cloud storage 2.0.0 / documentai 1.2.0


def batch_process_documents(
    project_id: str,
    location: str,
    processor_id: str,
    gcs_input_uri: str,
    input_mime_type: str,
    gcs_output_uri: str,
) -> Operation:
    opts = {}
    if location == "us":
        opts = {"api_endpoint": "us-documentai.googleapis.com:443"}

    # Instantiates a client
    documentai_client = documentai.DocumentProcessorServiceClient(client_options=opts)

    # projects/project-id/locations/location/processor/processor-id
    # You must create new processors in the Cloud Console first
    resource_name = documentai_client.processor_path(project_id, location, processor_id)

    # Cloud Storage URI for the Input Document
    input_document = documentai.GcsDocument(
        gcs_uri=gcs_input_uri, mime_type=input_mime_type
    )

    # Load GCS Input URI into a List of document files
    input_config = documentai.BatchDocumentsInputConfig(
        gcs_documents=documentai.GcsDocuments(documents=[input_document])
    )

    # Cloud Storage URI for Output directory
    gcs_output_config = documentai.DocumentOutputConfig.GcsOutputConfig(
        gcs_uri=gcs_output_uri
    )

    # Load GCS Output URI into OutputConfig object
    output_config = documentai.DocumentOutputConfig(gcs_output_config=gcs_output_config)

    # Configure Process Request
    request = documentai.BatchProcessRequest(
        name=resource_name,
        input_documents=input_config,
        document_output_config=output_config,
    )

    # Future for long-running operations returned from Google Cloud APIs.
    operation = documentai_client.batch_process_documents(request)

    return operation

def get_documents_from_gcs(
    gcs_output_uri: str, operation_name: str
) -> [documentai.Document]:
    """
    Download the document output from GCS.
    """

    # The GCS API requires the bucket name and URI prefix separately
    match = re.match(r"gs://([^/]+)/(.+)", gcs_output_uri)
    output_bucket = match.group(1)
    prefix = match.group(2)

    # The output files will be in a new subdirectory with the Operation ID as the name
    operation_id = re.search("operations\/(\d+)", operation_name, re.IGNORECASE).group(1)

    output_directory = f"{prefix}/{operation_id}"

    storage_client = storage.Client()

    # List of all of the files in the directory `gs://gcs_output_uri/operation_id`
    blob_list = list(storage_client.list_blobs(output_bucket, prefix=output_directory))

    output_documents = []

    for blob in blob_list:
        # Document AI should only output JSON files to GCS
        if ".json" in blob.name:
            document = documentai.types.Document.from_json(blob.download_as_bytes())
            output_documents.append(document)
        else:
            print(f"Skipping non-supported file type {blob.name}")

    return output_documents

operation = batch_process_documents(
        project_id=project_id,
        location=location,
        processor_id=processor_id,
        gcs_input_uri=gcs_input_uri,
        input_mime_type=input_mime_type,
        gcs_output_uri=gcs_output_uri,
    )

# Format: projects/PROJECT_NUMBER/locations/LOCATION/operations/OPERATION_ID
operation_name = operation.operation.name

# Continually polls the operation until it is complete.
# This could take some time for larger files
print(f"Waiting for operation {operation_name} to complete...")
result = operation.result(timeout=3000)


time.sleep(5)


document_list = get_documents_from_gcs(
        gcs_output_uri=gcs_output_uri, operation_name=operation_name
    )

out=[]

for i in range(len(document_list)):
    out.append((document_list[i].text))


with open("/home/user/fitbit/output.txt", "w") as text_file:
    text_file.write(' '.join(out))

#os.system('gsutil rm -r gs://pei-pdfs/output/*')

