import psycopg2
import os

DB_URL = os.environ.get("DB_URL")

def db_insert_users_pb(dc_id, dc_username, record):
        conn = psycopg2.connect(DB_URL)

        cursor = conn.cursor()
        cursor.execute("INSERT INTO UserScore(discord_id, username, wpm) VALUES ('{dc_id}','{dc_username}','{wpm}') ON CONFLICT (discord_id) DO UPDATE SET wpm=EXCLUDED.wpm WHERE UserScore.wpm < {wpm}".format(dc_id=dc_id, dc_username=dc_username, wpm=record["wpm"]))
       
        conn.commit()

        conn.close()

def db_view_topten():

        conn = psycopg2.connect(DB_URL)

        cursor = conn.cursor()
        cursor.execute("SELECT * FROM TopTen")
       
        data = cursor.fetchall()

        conn.close()

        return data


def db_view_user_pb(dc_id):

        conn = psycopg2.connect(DB_URL)


        cursor = conn.cursor()
        cursor.execute("SELECT wpm FROM UserScore WHERE discord_id = %s", (dc_id, ))
       
        data = cursor.fetchone()

        conn.close()

        return None if data == None else data[0]

def db_get_paragraph():

        conn = psycopg2.connect(DB_URL)


        cursor = conn.cursor()
        cursor.execute("SELECT * FROM paragraph OFFSET floor(random()*(select count(*) from paragraph)) LIMIT 1;")

        data = cursor.fetchone()
       

        conn.close()

        return {"paragraph": data[1], "img": data[2]}







