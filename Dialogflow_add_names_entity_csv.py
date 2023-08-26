import requests
import pandas as pd
from google.oauth2 import service_account
from google.cloud.dialogflowcx_v3beta1.types import entity_type
from google.auth.transport.requests import AuthorizedSession
import os

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/home/user/key.json'


data = pd.read_csv(
    "/home/user/Popular_Baby_Names.csv", header=0, sep=',')

data2=data["""Child's First Name"""].map(lambda x: x.title())

cities=data2.unique()


entity_json = []
for each in cities:
    each_entity_value = {}
    each_entity_value['value'] = each
    each_entity_value['synonyms'] = each
    entity_json.append(each_entity_value)
print(entity_json)
print('***************************************')

# download the service account json with the required permissions to call the cx agent
credentials= service_account.Credentials.from_service_account_file(
    '/home/user/key.json')
scoped_credentials=credentials.with_scopes(
    ['https://www.googleapis.com/auth/cloud-platform'])
authed_session=AuthorizedSession(scoped_credentials)
kind=entity_type.EntityType.Kind.KIND_MAP

# configure these variables before running the script
project_id='your-project-id'  # YOUR-PROJECT-ID
agent_id='yor-agent-id'  # YOUR-CX-AGENT-ID
location='us-central1'  # AGENT-LOCATION-ID
response=authed_session.post('https://us-central1-dialogflow.googleapis.com/v3/projects/' + project_id + '/locations/' + location + '/agents/' + agent_id + '/entityTypes',
                               json = {
                                   "kind": kind,
                                   "displayName": "nome",
                                   "entities": entity_json
                               }
                               )

response_txt=response.text
print(response_txt)
