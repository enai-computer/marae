import os
from pinecone import Pinecone
from app.data.dal.DatabaseWriter import DatabaseWriter
import time
from uuid import UUID

class Transform2VectorDB:

    def __init__(self):
        # load pinecone credentials from env vars
        self.pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
        self.index = self.pc.Index("multilingual-e5-large")
        self.namespace = "marae-test-space"
        self.db_writer = DatabaseWriter()

    def delete_document(self, document_id: UUID):
        vector_db_ids = self.db_writer.fetch_vector_db_ids(str(document_id))
        self.index.delete(ids=vector_db_ids, namespace=self.namespace)
        self.db_writer.delete_document(str(document_id))

    def sync_all_to_vector_db(self):
        print("[INFO]: starting sync")
        start_time = time.time()
        total_synced_count = 0
        synced_count = self.sync_to_vector_db()
        total_synced_count += synced_count
        while 0 < synced_count:
            synced_count = self.sync_to_vector_db()
            total_synced_count += synced_count
            wait_time = 0.1
            time.sleep(wait_time)
        print("[INFO]: finished sync, uploaded ", total_synced_count, " documents. After ", time.time() - start_time, " seconds")

        
    def sync_to_vector_db(self) -> int:

        documents = self.db_writer.fetch_non_processed_documents(limit=40)
        if len(documents) == 0:
            return 0
        
        print(f"[INFO]: started embedding process at: {time.time()}")        
        embeddings = self.transform_to_vectors(documents)
        print(f"[INFO]: uploading vectors at: {time.time()}")

        vectors = []
        for d, e in zip(documents, embeddings):
            vectors.append({
                "id": str(d['section_number']) + "-" + d['id'],
                "values": e['values'],
                "metadata": {'title': d['title'], 'space': d['space_id'], 'type': d['type']}
            })
        self.index.upsert(
            vectors=vectors,
            namespace=self.namespace
        )
        self.db_writer.mark_documents_as_processed(document_ids=[(d['id'], d['section_number']) for d in documents])
        print(f"[INFO]: finished uploading embedds at: {time.time()}, uploaded {len(documents)} documents")
        return len(documents)
    
    def transform_to_vectors(self, documents) -> list[dict]:
        embeddings = self.pc.inference.embed(
            "multilingual-e5-large",
            inputs=[d['content'] for d in documents],
            parameters={
                "input_type": "passage",
                 "truncate": "END"
            }
        )
        return embeddings
