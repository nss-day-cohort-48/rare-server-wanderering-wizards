import sqlite3
import json
from models import Login


def login_auth(email, password):
	with sqlite3.connect("./Rare.db") as conn:

		conn.row_factory = sqlite3.Row
		db_cursor = conn.cursor()

		db_cursor.execute("""
		SELECT
			u.id,
			u.email,
			u.password
		FROM Users u
		WHERE u.email = ?
		AND u.password = ?
		""", (email, password))

		data = db_cursor.fetchone()
		try:
			user = Login(data['email'], data['id'], True)
		except:
			print("nah man, you ain't init")
			user = Login("", "", False)

		return json.dumps(user.__dict__)


def register_user(new_user):
		with sqlite3.connect("./Rare.db") as conn:
				db_cursor = conn.cursor()

				db_cursor.execute("""
				INSERT INTO Users
						( first_name, last_name, email, password, created_on, active )
				VALUES
						( ?, ?, ?, ?, ?, ? );
				""", (new_user['first_name'], new_user['last_name'],
							new_user['email'], new_user['password'], new_user['created_on'], new_user['active'] ))

				# The `lastrowid` property on the cursor will return
				# the primary key of the last thing that got added to
				# the database.
				id = db_cursor.lastrowid

				# Add the `id` property to the animal dictionary that
				# was sent by the client so that the client sees the
				# primary key in the response.
				new_user['id'] = id

				#? NO WORKING, why?
				#? new_user['active'] = True

		return json.dumps(new_user)
