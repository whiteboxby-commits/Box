from fastapi import FastAPI
import sqlite3

app = FastAPI()

@app.get("/search")
def search(query: str):
    conn = sqlite3.connect("your_database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM your_table WHERE your_table MATCH ?", (query,))
    results = cursor.fetchall()
    conn.close()
    return {"results": results}
