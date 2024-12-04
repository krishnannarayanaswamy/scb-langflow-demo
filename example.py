from openai import OpenAI
import json
client = OpenAI()

response = client.embeddings.create(
    model="text-embedding-3-large",
    input="The food was delicious and the waiter..."
)
#response_body = json.loads(response.get('body').read())
print(response.data[0].embedding)