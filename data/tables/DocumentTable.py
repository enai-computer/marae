from sqlite3 import Cursor
import time

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
                processed_at REAL,
                PRIMARY KEY (id, section_number)
            )
        """)
    
    def upsert_document(cursor: Cursor, document: dict):
        if not document['content']:
            return
        
        cursor.execute("""
            INSERT INTO document (id, section_number, space_id, type, title, content, url, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(id, section_number) DO UPDATE SET
                title = excluded.title,
                content = excluded.content,
                url = excluded.url,
                updated_at = excluded.updated_at,
                processed_at = null
        """, (document['id'], document['section_number'], document['spaceId'], document['type'], document['title'], document['content'], document['url'], document['updatedAt']))

    def delete_document(cursor: Cursor, document_id: str):
        cursor.execute("""
            DELETE FROM document WHERE id = ?
        """, (document_id,))

    def fetch_non_processed_documents(cursor: Cursor, limit: int = 10) -> list[dict]:
        cursor.execute("""
            SELECT section_number, id, content, space_id, type, title FROM document WHERE processed_at IS NULL LIMIT ?
        """, (limit,))
        rows = cursor.fetchall()
        return [
            {
                'section_number': row[0],
                'id': row[1],
                'content': row[2],
                'space_id': row[3],
                'type': row[4],
                'title': row[5]
            }
            for row in rows
        ]
    
    def mark_documents_as_processed(cursor: Cursor, document_ids: list[(str, int)]):
        for doc_id in document_ids:
            cursor.execute("""
                UPDATE document SET processed_at = ? WHERE id = ? AND section_number = ?
            """, (time.time(), doc_id[0], doc_id[1]))   

    def fetch_all_id_section_numbers(cursor: Cursor, document_id: str) -> list[str]:
        cursor.execute("""
            SELECT section_number, id FROM document WHERE id = ?
        """, (document_id,))
        rows = cursor.fetchall()
        return [
            str(row[0]) + "-" + str(row[1])
            for row in rows
        ]