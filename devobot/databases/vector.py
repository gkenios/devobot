from abc import ABC
from typing import Any


class VectorDB(ABC):
    pass


class ChromaVectorDB(VectorDB):
    def __init__(self, collection_name, embeddings) -> None:
        from langchain_chroma import Chroma

        self.vector_store = Chroma(
            collection_name=collection_name,
            embedding_function=embeddings,
            persist_directory="./.chromadb",
        )

    def upsert(
        self,
        content: str | list[str],
        id: str | list[str] | None = None,
        metadata: dict[str, Any] | list[dict[str, Any]] | None = None,
    ) -> None:
        if isinstance(content, str):
            content = [content]
            id = [id]
            metadata = [metadata]
        for i in range(len(content)):
            self.vector_store.add_texts(
                texts=content,
                ids=id,
                metadata=metadata,
            )

    def delete(self, id: str | list[str] | None, **kwargs) -> None:
        if isinstance(id, str):
            id = [id]
        self.vector_store.delete(ids=id, **kwargs)

    def get(self, id: str) -> dict[str, Any]:
        result = self.vector_store.get_by_ids([id])[0]
        return {
            "id": result.id,
            "page_content": result.page_content,
            "metadata": result.metadata,
        }

    def search(self, question: str, k: int = 3) -> list[str]:
        method = "similarity"
        return [
            doc.id for doc in self.vector_store.search(question, method, k=k)
        ]


class AzureVectorDB(VectorDB):
    pass
