import sqlite3
import os
from data.tables.DocumentTable import DocumentTable
import threading

class DatabaseWriter:
    def __init__(self, db_path='appData/USERID/marae_spaces.db'):
        self.db_path = db_path
        self.connect_to_db()
        self.initDB()

    def connect_to_db(self):
        try:
            # Ensure the directory exists
            db_dir = os.path.dirname(self.db_path)
            if db_dir and not os.path.exists(db_dir):
                os.makedirs(db_dir)
            
            self.db_connection = sqlite3.connect(self.db_path, check_same_thread=False, autocommit=True)
            self.db_cursor = self.db_connection.cursor()
        except sqlite3.Error as e:
            print(f"Error connecting to database: {e}")

    def initDB(self):
        DocumentTable.create_table(self.db_cursor)
        self.db_connection.commit()

    def upsert_document(self, document: dict):
        DocumentTable.upsert_document(self.db_cursor, document)
        self.db_connection.commit()

    def delete_document(self, document_id: str):
        DocumentTable.delete_document(self.db_cursor, document_id)
        self.db_connection.commit()

    def fetch_non_processed_documents(self, limit: int = 10):
        return DocumentTable.fetch_non_processed_documents(self.db_cursor, limit)

    def mark_documents_as_processed(self, document_ids: list[tuple[str, int]]):
        DocumentTable.mark_documents_as_processed(self.db_cursor, document_ids)
        self.db_connection.commit()

    def close(self):
        self.db_connection.close()