from models import Post, User, Category, Comment
import sqlite3
import json


def get_all_comments():
    with sqlite3.connect("./Rare.db") as conn:

        # Just use these. It's a Black Box.
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT 
            com.id as comment_id,
            com.post_id,
            com.author_id,
            com.content as comment_content
        FROM Comments com
        """)

        comments = []

        data = db_cursor.fetchall()

        for row in data:

            comment = Comment(row['comment_id'], row['post_id'],
                              row['author_id'], row['comment_content'])

            comments.append(comment.__dict__)
    return json.dumps(comments)

    


def get_comments_by_post_id(id):
    with sqlite3.connect("./Rare.db") as conn:

        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT 
            com.id as comment_id,
            com.post_id,
            com.author_id,
            com.content as comment_content,
            pos.id,
            pos.user_id,
            pos.category_id,
            pos.title,
            pos.publication_date,
            pos.image_url,
            pos.content as post_content,
            pos.approved
        FROM Comments com
        JOIN Posts pos 
            ON pos.id = com.post_id
        WHERE pos.id = ?
        """, (id, ))

        comments = []

        data = db_cursor.fetchall()

        for row in data:

            comment = Comment(row['comment_id'], row['post_id'],
                              row['author_id'], row['comment_content'])

            post = Post(row['id'], row['user_id'], row['category_id'],
                        row['title'], row['publication_date'],
                        row['image_url'], row['post_content'], row['approved'],)

            comment.post = post.__dict__

            comments.append(comment.__dict__)
    return json.dumps(comments)
