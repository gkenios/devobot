from devobot.services.database_vector import ChromaVectorDB
from devobot.init.yaml_processing import embeddings


page_content = "Parking is open at the Devoteam office from 08:00 to 21:00. Please visit our interanet to book a parking space."
metadata = {"title": "Parking"}
id = "Parking"


vector_db = ChromaVectorDB("faq", embeddings)
vector_store = vector_db.vector_store
vector_db.upsert(page_content, id, metadata)
results = vector_db.get("Parking")
print(results)

d = vector_store.search("book a parking space", "similarity", k=3)
print(d)
