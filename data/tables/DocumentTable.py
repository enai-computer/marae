from sqlite3 import Cursor

class DocumentTable:
    def create_table(cursor: Cursor):
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS document (
                id TEXT NOT NULL,
                section_number INTEGER NOT NULL DEFAULT 0,
                space_id TEXT NOT NULL,
                type TEXT NOT NULL,
                title TEXT,
                content TEXT NOT NULL,
                url TEXT,
                updated_at REAL NOT NULL,
                PRIMARY KEY (id, section_number)
            )
        """)
    
    def upsert_document(cursor: Cursor, document: dict):
        cursor.execute("""
            INSERT INTO document (id, section_number, space_id, type, title, content, url, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(id, section_number) DO UPDATE SET
                title = excluded.title,
                content = excluded.content,
                url = excluded.url,
                updated_at = excluded.updated_at
        """, (document['id'], document['section_number'], document['spaceId'], document['type'], document['title'], document['content'], document['url'], document['updatedAt']))

    def delete_document(cursor: Cursor, document_id: str):
        cursor.execute("""
            DELETE FROM document WHERE id = ?
        """, (document_id,))
