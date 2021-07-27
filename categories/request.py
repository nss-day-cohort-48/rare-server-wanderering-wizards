import categories
import sqlite3
import json
from models import Category

def create_category(new_category):
    with sqlite3.connect("./Rare.db") as conn:
        db_cursor = conn.cursor()
        db_cursor.execute("""
        INSERT INTO Categories
            (label)
        VALUES
            (?);
        """, (new_category['label'],))
        
    return json.dumps(new_category)

def get_categories():
    with sqlite3.connect("./Rare.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        db_cursor.execute("""
        SELECT
            c.id,
            c.label
        FROM Categories c
        """)
        categories = []
        dataset = db_cursor.fetchall()
        for row in dataset:
            category = Category(row['id'], row['label'])
            categories.append(category.__dict__)

    return json.dumps(categories)