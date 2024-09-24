from .dal.DatabaseWriter import DatabaseWriter

class Processor:

    def __init__(self):
        self.db_writer = DatabaseWriter()

    def processNote(self, document: dict):
        # self.db_writer.insert_document(document)
        print(document)

