from abc import ABC, abstractmethod
from typing import Any


class VectorDB(ABC):
    def search(self, question: str, k: int = 3) -> list[str]:
        method = "similarity"
        return self._search(question, method, k=k)

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
        self._upsert(content, id, metadata)

    def delete(self, id: str | list[str] | None, **kwargs) -> None:
        if isinstance(id, str):
            id = [id]
        self._delete(id, **kwargs)

    @abstractmethod
    def _search(self, question: str, method: str, k: int = 3) -> list[str]:
        pass

    @abstractmethod
    def _upsert(
        self,
        content: list[str],
        id: list[str],
        metadata: list[dict[str, Any]],
    ) -> None:
        pass

    @abstractmethod
    def _delete(self, id: list[str], **kwargs) -> None:
        pass


class ChromaVectorDB(VectorDB):
    def __init__(self, collection_name, embeddings) -> None:
        from langchain_chroma import Chroma

        self.vector_store = Chroma(
            collection_name=collection_name,
            embedding_function=embeddings,
            persist_directory="./.chromadb",
        )

    def _search(self, question: str, method: str, k: int = 3) -> list[str]:
        return [
            doc.page_content
            for doc in self.vector_store.search(question, method, k=k)
        ]

    def _upsert(
        self,
        content: list[str],
        id: list[str] | None = None,
        metadata: list[dict[str, Any]] | None = None,
    ) -> None:
        self.vector_store.add_texts(
            texts=content,
            ids=id,
            metadatas=metadata,
        )
    def _delete(self, id: list[str] | None, **kwargs) -> None:
        self.vector_store.delete(ids=id, **kwargs)

    def get(self, id: str) -> dict[str, Any]:
        result = self.vector_store.get_by_ids([id])[0]
        return {
            "id": result.id,
            "page_content": result.page_content,
            "metadata": result.metadata,
        }


class AzureVectorDB(VectorDB):
    pass
