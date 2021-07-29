from models import Post, User, Category, Comment
import sqlite3
import json


def get_posts_by_id(id):
    # Open a connection to the database
    with sqlite3.connect("./Rare.db") as conn:

        # Just use these. It's a Black Box.
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        SELECT
            p.id,
            p.user_id,
            p.category_id,
            p.title,
            p.publication_date,
            p.image_url,
            p.content,
            p.approved,
            c.id,
            c.label,
            u.id,
            u.first_name,
            u.last_name,
            u.email,
            u.bio,
            u.username,
            u.password,
            u.profile_image_url,
            u.created_on,
            u.active
        FROM posts p 
        JOIN Users u 
            ON u.id = p.user_id
        JOIN Categories c 
            ON c.id = p.category_id
        WHERE u.id = ?
        
        """, (id,))

        posts = []

        dataset = db_cursor.fetchall()

        for row in dataset:

            post = Post(row['id'], row['user_id'], row['category_id'],
                        row['title'], row['publication_date'],
                        row['image_url'], row['content'], row['approved'],)
            category = Category(row['id'], row['label'])

            user = User(row['id'], row['first_name'], row['last_name'],
                        row['email'], row['bio'],
                        row['username'], row['password'], row['profile_image_url'], row['created_on'], row['active'],)

            post.category = category.__dict__
            post.user = user.__dict__

            posts.append(post.__dict__)

    # Use `json` package to properly serialize list as JSON
    return json.dumps(posts)


def get_all_posts():
    with sqlite3.connect("./Rare.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        db_cursor.execute("""
        SELECT
            p.id,
            p.user_id,
            p.category_id,
            p.title,
            p.publication_date,
            p.image_url,
            p.content,
            p.approved,
            c.id,
            c.label,
            u.id,
            u.first_name,
            u.last_name,
            u.email,
            u.bio,
            u.username,
            u.password,
            u.profile_image_url,
            u.created_on,
            u.active
        FROM posts p 
        JOIN Categories c 
        ON c.id = p.category_id
        JOIN Users u 
        ON u.id = p.user_id
        
        """)

        posts = []

        dataset = db_cursor.fetchall()

        for row in dataset:

            post = Post(row['id'], row['user_id'], row['category_id'],
                        row['title'], row['publication_date'],
                        row['image_url'], row['content'], row['approved'],)
            category = Category(row['id'], row['label'])

            user = User(row['id'], row['first_name'], row['last_name'],
                        row['email'], row['bio'],
                        row['username'], row['password'], row['profile_image_url'], row['created_on'], row['active'],)

            post.category = category.__dict__
            post.user = user.__dict__

            db_cursor.execute("""
                SELECT
                    t.id,
                    t.label
                FROM Tags t
                JOIN PostTags pt on t.id = pt.tag_id
                JOIN Posts p on p.id = pt.post_id
                WHERE p.id = ?
            """,(post.id, ))

            tag_rows = db_cursor.fetchall()

            for tag_row in tag_rows:
                tag = {
                    'id': tag_row['id'],
                    'label': tag_row['label']
                }
                post.tags.append(tag)

            posts.append(post.__dict__)

    return json.dumps(posts)


def get_post_details(id):
    with sqlite3.connect("./Rare.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Use a ? parameter to inject a variable's value
        # into the SQL statement.
        db_cursor.execute("""
        SELECT
            p.id,
            p.user_id,
            p.category_id,
            p.title,
            p.publication_date,
            p.image_url,
            p.content,
            p.approved,
            c.id,
            c.label,
            u.id,
            u.first_name,
            u.last_name,
            u.email,
            u.bio,
            u.username,
            u.password,
            u.profile_image_url,
            u.created_on,
            u.active
        FROM posts p 
        JOIN Users u 
            ON u.id = p.user_id
        JOIN Categories c 
            ON c.id = p.category_id
        WHERE p.id = ?
        """, (id, ))

        # Load the single result into memory
        data = db_cursor.fetchone()

        # Create an animal instance from the current row
        post = Post(data['id'], data['user_id'], data['category_id'],
                    data['title'], data['publication_date'],
                    data['image_url'], data['content'], data['approved'],)

        category = Category(data['id'], data['label'])

        user = User(data['id'], data['first_name'], data['last_name'],
                    data['email'], data['bio'],
                    data['username'], data['password'], data['profile_image_url'], data['created_on'], data['active'],)

        post.category = category.__dict__
        post.user = user.__dict__

        db_cursor.execute("""
                SELECT
                    t.id,
                    t.label
                FROM Tags t
                JOIN PostTags pt on t.id = pt.tag_id
                JOIN Posts p on p.id = pt.post_id
                WHERE p.id = ?
            """,(post.id, ))

        tag_rows = db_cursor.fetchall()

        for tag_row in tag_rows:
            tag = {
                'id': tag_row['id'],
                'label': tag_row['label']
            }
            post.tags.append(tag)

        db_cursor.execute("""
            SELECT
                com.id as comment_id,
                com.post_id,
                com.author_id,
                com.content as comment_content
            FROM Comments com
            JOIN Posts pos
                ON com.post_id = pos.id
            WHERE pos.id = ?
        """, ( post.id, ))

        comment_rows = db_cursor.fetchall()

        for comment_row in comment_rows:
            comment = {
                'id': comment_row['comment_id'],
                'post_id': comment_row['post_id'],
                'author_id': comment_row['author_id'],
                'content': comment_row['comment_content']
            }
            post.comments.append(comment)

    return json.dumps(post.__dict__)

# TODO Join comments on to postsDetail query
        # JOIN Comments com
        # ON p.id = com.post_id


def delete_post(id):
    with sqlite3.connect("./Rare.db") as conn:
        db_cursor = conn.cursor()
        db_cursor.execute("""
        DELETE FROM posts
        WHERE id = ?
        """, (id, ))


def create_post(new_post):
    with sqlite3.connect("./Rare.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO Posts
            ( user_id, category_id, title, publication_date, image_url, content, approved )
        VALUES
            ( ?, ?, ?, ?, ?, ?, ?);
        """, (new_post['user_id'], new_post['category_id'],
              new_post['title'], new_post['publication_date'],
              new_post['image_url'], new_post['content'], new_post['approved']))

        id = db_cursor.lastrowid
        new_post['id'] = id

        for tag in new_post['tags']:
            db_cursor.execute("""
            INSERT INTO PostTags
                (post_id, tag_id)
            VALUES (?,?)
            """, (new_post['id'], tag['id']))

    return json.dumps(new_post)


def update_post(id, update_post):
    with sqlite3.connect("./Rare.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        UPDATE Posts
            SET
                category_id = ?,
                title = ?,
                image_url = ?,
                content = ?
        WHERE id = ?
        """, (update_post['category_id'], update_post['title'],
              update_post['image_url'], update_post['content'], id, ))

        # Were any rows affected?
        # Did the client send an `id` that exists?
        rows_affected = db_cursor.rowcount

    if rows_affected == 0:
        # Forces 404 response by main module
        return False
    else:
        # Forces 204 response by main module
        return True
