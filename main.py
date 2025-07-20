from fastapi import FastAPI
from notion_client import Client
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()

# Notion クライアントの初期化
notion = Client(auth=os.getenv("NOTION_TOKEN"))
database_id = os.getenv("NOTION_DATABASE_ID")

@app.get("/")
def read_root():
    return {"message": "Hello, Notion-GPTs!"}

@app.get("/notion-database")
def get_database():
    try:
        response = notion.databases.query(database_id=database_id)
        return response
    except Exception as e:
        return {"error": str(e)}
