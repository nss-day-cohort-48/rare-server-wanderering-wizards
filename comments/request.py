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
            com.content as comment_content,
            usr.id,
            usr.first_name,
            usr.last_name,
            usr.email,
            usr.bio,
            usr.username,
            usr.password,
            usr.profile_image_url,
            usr.created_on,
            usr.active
        FROM Comments com
        JOIN Users usr
            ON com.author_id = usr.id
        """)

        comments = []

        data = db_cursor.fetchall()

        for row in data:

            comment = Comment(row['comment_id'], row['post_id'],
                              row['author_id'], row['comment_content'])
            
            user = User(row['id'], row['first_name'], row['last_name'],
                        row['email'], row['bio'],
                        row['username'], row['password'], row['profile_image_url'], row['created_on'], row['active'],)
            
            comment.user = user.__dict__

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
            pos.approved,
            user.id,
            user.first_name,
            user.last_name,
            user.email,
            user.bio,
            user.username,
            user.password,
            user.profile_image_url,
            user.created_on,
            user.active
        FROM Comments com
        JOIN Posts pos 
            ON pos.id = com.post_id
        JOIN Users user
            ON com.author_id = user.id
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

            user = User(row['id'], row['first_name'], row['last_name'],
                        row['email'], row['bio'],
                        row['username'], row['password'], row['profile_image_url'], row['created_on'], row['active'],)

            comment.post = post.__dict__
            comment.user = user.__dict__

            comments.append(comment.__dict__)
    return json.dumps(comments)


def create_comment(new_comment):
    with sqlite3.connect("./Rare.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO Comments
            ( post_id, author_id, content  )
        VALUES
            ( ?, ?, ? );
        """, (new_comment['post_id'],
              new_comment['author_id'], new_comment['content'], ))

        id = db_cursor.lastrowid
        new_comment['id'] = id

    return json.dumps(new_comment)
