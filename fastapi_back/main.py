from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
import mysql.connector


app = FastAPI()


class Post(BaseModel):
    content: str


def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("MYSQL_HOST"),
        port=int(os.getenv("MYSQL_PORT", 3306)),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        database=os.getenv("MYSQL_DB"),
        autocommit=True,
    )


@app.get("/api/posts")
def get_posts():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        "SELECT id, content, created_at FROM posts ORDER BY created_at DESC"
    )
    posts = cursor.fetchall()
    cursor.close()
    conn.close()
    return posts


@app.post("/api/posts")
def create_post(post: Post):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO posts (content) VALUES (%s)",
            (post.content,),
        )
        conn.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

    return {"message": "Post created"}
