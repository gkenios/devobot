from abc import ABC, abstractmethod
from enum import Enum
from typing import Any

from langchain_core.embeddings.embeddings import Embeddings


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
        if isinstance(id, str):
            id = [id]
        if isinstance(metadata, dict):
            metadata = [metadata]
        self._upsert(content, id, metadata)

    def delete(self, id: str | list[str] | None, **kwargs: Any) -> None:
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
        id: list[str] | None,
        metadata: list[dict[str, Any]] | None = None,
    ) -> None:
        pass

    @abstractmethod
    def _delete(self, id: list[str] | None, **kwargs: Any) -> None:
        pass


class ChromaVectorDB(VectorDB):
    def __init__(
        self,
        embeddings: Embeddings,
        collection: str,
        endpoint: str,
    ) -> None:
        from langchain_chroma import Chroma

        self.vector_store = Chroma(
            embedding_function=embeddings,
            persist_directory=endpoint,
            collection_name=collection,
        )

    def _search(self, question: str, method: str, k: int = 3) -> list[str]:
        return [
            doc.page_content
            for doc in self.vector_store.search(question, method, k=k)
        ]

    def _upsert(
        self,
        content: list[str],
        id: list[str] | None,
        metadata: list[dict[str, Any]] | None = None,
    ) -> None:
        self.vector_store.add_texts(
            texts=content,
            ids=id,
            metadatas=metadata,
        )

    def _delete(self, id: list[str] | None, **kwargs: Any) -> None:
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


class GCPVectorDB(VectorDB):
    pass


class VectorDBFactory(Enum):
    local = ChromaVectorDB
    azure = AzureVectorDB
    gcp = GCPVectorDB
