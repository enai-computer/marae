from pinecone.grpc import PineconeGRPC as Pinecone
import os
from app.data.dal.DatabaseWriter import DatabaseWriter

class SpacesSearchEngine:

    def __init__(self):
        self.pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
        self.index = self.pc.Index("multilingual-e5-large")
        self.namespace = "marae-test-space"
        self.db_writer = DatabaseWriter()

    def search(self, query: str) -> str:
        print(f"searching for {query}")
        query_vector = self.pc.inference.embed(
            "multilingual-e5-large",
            inputs=[query],
            parameters={
                "input_type": "passage",
                "truncate": "END"
            }
        )
        results = self.index.query(
            namespace=self.namespace, 
            vector=query_vector.data[0].values,
            top_k=5,
            include_metadata=True
        )
        return self.get_context_form_response(results)
    
    def get_context_form_response(self, response) -> str:
        context = ""
        for result in response['matches']:
            split_index = result['id'].find('-')
            if split_index != -1:
                sector_nr = int(result['id'][:split_index])
                id = result['id'][split_index + 1:]
                context += self.db_writer.fetch_content(id, sector_nr) + "\n\n"
        return context
