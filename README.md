Have a DataStax Astra account, create a vector database, create a collection with Bring your own L Embedding model, set the dimesions to 3072

Create a openai account and have a key

Run the below commands

pip install -r requirements.txt

set ENV properties 

ASTRA_DB_APPLICATION_TOKEN
ASTRA_DB_API_ENDPOINT
OPENAI_API_KEY
ASTRA_DB_KEYSPACE

Modify the collection name in the loadJsonAstra.py

python loadJsonAstra.py