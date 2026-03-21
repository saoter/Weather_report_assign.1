"""
store_vector.py - Optional: Vector embeddings for semantic search
(Advanced feature - stores embeddings for future AI queries)
"""

import sqlite3
from config import DB_PATH

class VectorStore:
    """Store weather data as vector embeddings"""
    
    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path
    
    def initialize_vector_table(self):
        """Create vector store table"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS weather_embeddings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                location TEXT,
                date TEXT,
                embedding TEXT,  -- JSON array as string
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        conn.commit()
        conn.close()
    
    def store_embedding(self, location, date, embedding, description):
        """Store weather embedding"""
        import json
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        embedding_json = json.dumps(embedding)
        
        cursor.execute("""
            INSERT INTO weather_embeddings
            (location, date, embedding, description)
            VALUES (?, ?, ?, ?)
        """, (location, date, embedding_json, description))
        
        conn.commit()
        conn.close()

if __name__ == "__main__":
    vs = VectorStore()
    vs.initialize_vector_table()
    print("✅ Vector store initialized!")