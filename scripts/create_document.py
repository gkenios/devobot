from devobot.services.database_vector import ChromaVectorDB
from devobot.init.yaml_processing import embeddings
from devobot.utils import read_file


faq = read_file("faq.yml")
vector_db = ChromaVectorDB("faq", embeddings)
vector_store = vector_db.vector_store

for document in faq:
    id = document["title"]
    page_content = (
        f"Source: {document['source']}\n"
        f"Title: {document['title']}\n"
        f"Question: {document['question']}\n"
        f"Answer: {document['answer']}"
    )
    metadata = {
        "title": document["title"],
        "category": document["category"],
        "source": document["source"],
        "question": document["question"],
    }
    vector_db.upsert(page_content, id, metadata)

search = vector_store.search("Parking", "similarity", k=3)
print(search)
