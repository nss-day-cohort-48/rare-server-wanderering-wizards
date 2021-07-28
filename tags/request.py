import tags
import sqlite3
import json
from models import Tag

def create_tag(new_tag):
    with sqlite3.connect("./Rare.db") as conn:
        db_cursor = conn.cursor()
        db_cursor.execute("""
        INSERT INTO Tags
            (label)
        VALUES
            (?);
        """, (new_tag['label'],))
        
    return json.dumps(new_tag)

def get_tags():
    with sqlite3.connect("./Rare.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        db_cursor.execute("""
        SELECT
            c.id,
            c.label
        FROM tags c
        """)
        tags = []
        dataset = db_cursor.fetchall()
        for row in dataset:
            tag = Tag(row['id'], row['label'])
            tags.append(tag.__dict__)

    return json.dumps(tags)