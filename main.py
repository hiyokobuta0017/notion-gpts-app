import os
from fastapi import FastAPI
from notion_client import Client
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

NOTION_TOKEN = os.getenv("NOTION_TOKEN")
DATABASE_ID = os.getenv("DATABASE_ID")

notion = Client(auth=NOTION_TOKEN)

@app.get("/")
def read_root():
    return {"message": "Hello, Notion-GPTs!"}

@app.get("/notion-database")
def get_database():
    try:
        response = notion.databases.query(database_id=DATABASE_ID)
        return response
    except Exception as e:
        return {"error": str(e)}
