from .dal.DatabaseWriter import DatabaseWriter
from uuid import UUID
import requests
from typing import List
from bs4 import BeautifulSoup

class Processor:

    def __init__(self):
        self.db_writer = DatabaseWriter()

    def processNote(self, id: UUID, document: dict):
        document['id'] = str(id)
        document['type'] = 'note'
        document['url'] = None
        extracted_content = self.chunk_content(document['content'])
        section_number = 0
        for content in extracted_content:
            document['content'] = content
            document['section_number'] = section_number
            self.db_writer.upsert_document(document)
            section_number += 1

    def processWebcontent(self, id: UUID, document: dict):
        document['id'] = str(id)
        document['type'] = 'webContent'
        html = self.fetch_website(document['url'])
        if html:
            extracted_content = self.extract_content(html)
            section_number = 0
            for content in extracted_content:
                document['content'] = content
                document['section_number'] = section_number
                self.db_writer.upsert_document(document)
                section_number += 1
        else:
            document['content'] = None
            document['section_number'] = 0
            self.db_writer.upsert_document(document)

    def processPdf(self, document: dict):
        print(document)

    def deleteDocument(self, document_id: str):
        self.db_writer.delete_document(document_id)

    # extraction & transformation
    def fetch_website(self, webUrl) -> str | None:
        try:
            response = requests.get(webUrl)
            if response.status_code == 200:
                return response.text
        except Exception as e:
            return None
        return None

    def extract_content(self, html: str) -> List[str]:
        soup = BeautifulSoup(html, 'html.parser')
        content = soup.get_text()
        return self.chunk_content(content)
    
    def chunk_content(self, content: str) -> List[str]:
        # split content into chunks of approximately 350 tokens
        words = content.split()
        chunks = []
        chunk = []
        word_count = 0

        for word in words:
            chunk.append(word)
            word_count += 1
            if word_count >= 350:
                chunks.append(' '.join(chunk))
                chunk = []
                word_count = 0

        if chunk:
            chunks.append(' '.join(chunk))

        return chunks
