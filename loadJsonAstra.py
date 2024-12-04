
import os
import json
from astrapy import DataAPIClient
from dotenv import load_dotenv
from openai import OpenAI
load_dotenv()

openaiclient = OpenAI()


script_dir = os.path.dirname(__file__)  # Directory of the script
file_path = os.path.join(script_dir, 'standard-chartered-plc-full-year-2023-report.pdf.json')

with open(file_path) as user_file:
    file_contents = user_file.read()

client = DataAPIClient(os.environ["ASTRA_DB_APPLICATION_TOKEN"])
database = client.get_database(os.environ["ASTRA_DB_API_ENDPOINT"])
collection = database.get_collection("scb_report")

allpages = json.loads(file_contents)
#docdata = docdata[2:]
for page in allpages:
    pagenumber = page.get('page')
    print(pagenumber)
    content = page.get('md') + "\n\n"
    #print(content)
    while True:
        try:
            response = openaiclient.embeddings.create(
                model="text-embedding-3-large",
                input=content
            )
            response_body = response.data[0].embedding
            collection.update_one(
              {'_id': "standard-chartered-plc-full-year-2023-report_" + str(pagenumber)},
              {'$set': {
                'page': page.get('page'), 
                '$vector': response_body, 
                'content': content, 
                'metadata': { 'pagenumber': page }
              }},
              upsert=True
          )
        except Exception as ex:
            print(ex)
            print("Retrying...")
            continue
        break
  