import json
import os
import pickle
from pathlib import Path
from typing import Optional

import faiss
import numpy as np
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.config import get_settings
from app.services.gemini_service import GeminiService

settings = get_settings()


class FAISSStore:
    def __init__(self):
        self.index_dir = Path(settings.faiss_index_dir)
        self.index_dir.mkdir(parents=True, exist_ok=True)
        self.index_path = self.index_dir / "index.faiss"
        self.meta_path = self.index_dir / "metadata.pkl"
        self.dimension = 768
        self.gemini = GeminiService()
        self._index: Optional[faiss.IndexFlatIP] = None
        self._metadata: list[dict] = []
        self._load()

    def _load(self):
        if self.index_path.exists() and self.meta_path.exists():
            self._index = faiss.read_index(str(self.index_path))
            with open(self.meta_path, "rb") as f:
                self._metadata = pickle.load(f)
        else:
            self._index = faiss.IndexFlatIP(self.dimension)
            self._metadata = []

    def _save(self):
        faiss.write_index(self._index, str(self.index_path))
        with open(self.meta_path, "wb") as f:
            pickle.dump(self._metadata, f)

    def _embed(self, texts: list[str]) -> np.ndarray:
        embeddings = self.gemini.embed_texts(texts)
        arr = np.array(embeddings, dtype=np.float32)
        faiss.normalize_L2(arr)
        return arr

    def add_document_chunks(
        self,
        document_id: int,
        document_title: str,
        text: str,
        page_count: int = 1,
    ) -> int:
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.chunk_size,
            chunk_overlap=settings.chunk_overlap,
        )
        chunks = splitter.split_text(text)
        if not chunks:
            return 0

        embeddings = self._embed(chunks)
        self._index.add(embeddings)

        for i, chunk in enumerate(chunks):
            page = min(page_count, max(1, int((i / len(chunks)) * page_count) + 1))
            self._metadata.append({
                "document_id": document_id,
                "document_title": document_title,
                "chunk_index": i,
                "text": chunk,
                "page": page,
            })

        self._save()
        return len(chunks)

    def search(self, query: str, top_k: int = 5) -> list[dict]:
        if self._index.ntotal == 0:
            return []

        query_emb = self._embed([query])
        scores, indices = self._index.search(query_emb, min(top_k, self._index.ntotal))

        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx < 0 or idx >= len(self._metadata):
                continue
            meta = self._metadata[idx].copy()
            meta["score"] = float(score)
            results.append(meta)
        return results

    def delete_document(self, document_id: int) -> None:
        keep_meta = [m for m in self._metadata if m["document_id"] != document_id]
        if len(keep_meta) == len(self._metadata):
            return
        self._metadata = keep_meta
        if self._metadata:
            texts = [m["text"] for m in self._metadata]
            embeddings = self._embed(texts)
            self._index = faiss.IndexFlatIP(self.dimension)
            self._index.add(embeddings)
        else:
            self._index = faiss.IndexFlatIP(self.dimension)
        self._save()

    @property
    def total_chunks(self) -> int:
        return len(self._metadata)


_faiss_store: Optional[FAISSStore] = None


def get_faiss_store() -> FAISSStore:
    global _faiss_store
    if _faiss_store is None:
        _faiss_store = FAISSStore()
    return _faiss_store
