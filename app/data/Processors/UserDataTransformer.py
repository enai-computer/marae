from app.data.dal.DatabaseWriter import DatabaseWriter
from uuid import UUID
import requests
from typing import List
from bs4 import BeautifulSoup
from PyPDF2 import PdfReader
import os

class UserDataTransformer:

    def __init__(self):
        self.db_writer = DatabaseWriter()

    def delete_document(self, document_id: UUID):
        self.db_writer.delete_document(str(document_id))

    def processNote(self, id: UUID, document: dict):
        document['id'] = str(id)
        document['type'] = 'note'
        document['url'] = None
        section_number = 0
        extracted_content = UserDataTransformer.chunk_content(document['content'])
        # if title is not in document
        if 'title' not in document:
            document['title'] = extracted_content[0][:100]
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

    def processPdf(self, id: UUID, document: dict):
        document['id'] = str(id)
        document['type'] = 'pdf'
        section_number = 0
        extracted_content = UserDataTransformer.extract_pdf_content(document['url'])
        for content in extracted_content:
            document['content'] = content
            document['section_number'] = section_number
            self.db_writer.upsert_document(document)
            section_number += 1

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
        return UserDataTransformer.chunk_content(content)
    
    def chunk_content(content: str) -> List[str]:
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

    # extract pdf content
    def extract_pdf_content(pdf_path: str) -> str:
        
        if not os.path.exists(pdf_path):
            return ""
        
        if pdf_path.startswith("file://"):
            pdf_path = pdf_path[7:]

        reader = PdfReader(pdf_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text
