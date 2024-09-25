from .dal.DatabaseWriter import DatabaseWriter
from uuid import UUID

class Processor:

    def __init__(self):
        self.db_writer = DatabaseWriter()

    def processNote(self, id: UUID, document: dict):
        document['id'] = str(id)
        document['type'] = 'note'
        document['url'] = None
        document['section_number'] = 0
        self.db_writer.upsert_document(document)
        print(document)

    def processWebcontent(self, document: dict):
        print(document)

    def processPdf(self, document: dict):
        print(document)

    def deleteDocument(self, document_id: str):
        self.db_writer.delete_document(document_id)
